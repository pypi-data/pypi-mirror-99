# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Classes that wrap training steps"""
import copy
import itertools
import json
import os
import time
import torch
from contextlib import nullcontext

from azureml.contrib.automl.dnn.vision.object_detection.eval import cocotools
from azureml.contrib.automl.dnn.vision.object_detection.eval.utils import prepare_bounding_boxes_for_eval
from azureml.contrib.automl.dnn.vision.object_detection.eval.vocmap import VocMap
from azureml.contrib.automl.dnn.vision.object_detection.common import boundingbox, masktools
from azureml.contrib.automl.dnn.vision.object_detection.common.constants import TrainingParameters, \
    ValidationMetricType
from azureml.contrib.automl.dnn.vision.object_detection.common.object_detection_utils import compute_metrics
from azureml.contrib.automl.dnn.vision.common import distributed_utils
from azureml.contrib.automl.dnn.vision.common.constants import ArtifactLiterals, TrainingCommonSettings
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionSystemException
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.system_meter import SystemMeter
from azureml.contrib.automl.dnn.vision.common.trainer.lrschedule import LRSchedulerUpdateType
from azureml.contrib.automl.dnn.vision.common.utils import _data_exception_safe_iterator, \
    log_end_training_stats, log_verbose_metrics_to_rh
from azureml.contrib.automl.dnn.vision.common.artifacts_utils import save_model_checkpoint, write_artifacts
from azureml.contrib.automl.dnn.vision.common.average_meter import AverageMeter
from azureml.contrib.automl.dnn.vision.object_detection.writers.score_script_utils import write_scoring_script

logger = get_logger(__name__)


class TrainSettings:
    """Settings for training."""

    def __init__(self, **kwargs):
        """
        :param kwargs: Optional training parameters. Currently supports
          -number_of_epochs: Number of epochs to train for (int)
          -max_patience_iterations: Number of epochs with no validation
          improvement before stopping.
          -primary_metric: Metric that is evaluated and logged by AzureML run object.
          -early_stop_delay_iterations: Number of epochs to wait before tracking validation
          improvement for early stopping.
        :type kwargs: dict
        """

        self._number_of_epochs = kwargs.get(
            "number_of_epochs", TrainingParameters.DEFAULT_NUMBER_EPOCHS)
        self._max_patience_iterations = kwargs.get(
            "max_patience_iterations", TrainingParameters.DEFAULT_PATIENCE_ITERATIONS)
        self.primary_metric = kwargs.get(
            "primary_metric", TrainingParameters.DEFAULT_PRIMARY_METRIC)
        self._early_stop_delay_iterations = kwargs.get(
            "early_stop_delay_iterations", TrainingParameters.DEFAULT_EARLY_STOP_DELAY_ITERATIONS)

    @property
    def number_of_epochs(self):
        """Get number of epochs

        :return: number_of_epochs
        :rtype: int
        """
        return self._number_of_epochs

    @property
    def max_patience_iterations(self):
        """Get number of patience iterations

        :return: max_patience_iterations
        :rtype: int
        """
        return self._max_patience_iterations

    @property
    def early_stop_delay_iterations(self):
        """Get number of iterations to wait before early stop logic is executed.

        :return: early_stop_delay_iterations
        :rtype: int
        """
        return self._early_stop_delay_iterations


def move_images_to_device(images, device):
    """Convenience function to move images to device (gpu/cpu).

    :param images: Batch of images
    :type images: Pytorch tensor
    :param device: Target device
    :type device: Pytorch device
    """

    return [image.to(device) for image in images]


def move_targets_to_device(targets, device):
    """Convenience function to move training targets to device (gpu/cpu)

    :param targets: Batch Training targets (bounding boxes and classes)
    :type targets: Dictionary
    :param device: Target device
    :type device: Pytorch device
    """

    return [{k: v.to(device) for k, v in target.items()} for
            target in targets]


def train_one_epoch(model, optimizer, scheduler, train_data_loader,
                    device, criterion, epoch, print_freq, system_meter):
    """Train a model for one epoch

    :param model: Model to be trained
    :type model: Pytorch nn.Module
    :param optimizer: Optimizer used in training
    :type optimizer: Pytorch optimizer
    :param scheduler: Learning Rate Scheduler wrapper
    :type scheduler: BaseLRSchedulerWrapper (see common.trainer.lrschedule)
    :param train_data_loader: Data loader for training data
    :type train_data_loader: Pytorch data loader
    :param device: Target device
    :type device: Pytorch device
    :param criterion: Loss function wrapper
    :type criterion: Object derived from BaseCriterionWrapper (see object_detection.train.criterion)
    :param epoch: Current training epoch
    :type epoch: int
    :param print_freq: How often you want to print the output
    :type print_freq: int
    :param system_meter: A SystemMeter to collect system properties
    :type system_meter: SystemMeter
    """

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()

    model.train()

    end = time.time()
    uneven_batches_context_manager = model.join() if distributed_utils.dist_available_and_initialized() \
        else nullcontext()

    with uneven_batches_context_manager:
        for i, (images, targets, info) in enumerate(_data_exception_safe_iterator(iter(train_data_loader))):
            # measure data loading time
            data_time.update(time.time() - end)

            images = move_images_to_device(images, device)
            targets = move_targets_to_device(targets, device)

            loss_dict = criterion.evaluate(model, images, targets)
            loss = sum(loss_dict.values())
            loss_value = loss.item()

            optimizer.zero_grad()
            loss.backward()

            # grad clipping to prevent grad exploding
            # especially to avoid NaN/infinite values resulted from corrupted model/input_data or high learning rate
            torch.nn.utils.clip_grad_value_(model.parameters(),
                                            clip_value=TrainingCommonSettings.GRADIENT_CLIP_VALUE)
            optimizer.step()

            if scheduler.update_type == LRSchedulerUpdateType.BATCH:
                scheduler.lr_scheduler.step()

            # record loss and measure elapsed time
            losses.update(loss_value, len(images))
            batch_time.update(time.time() - end)
            end = time.time()

            # delete tensors which have a valid grad_fn
            del loss, loss_dict

            if i % print_freq == 0 or i == len(train_data_loader) - 1:
                mesg = "Epoch: [{0}][{1}/{2}]\t" "lr: {3}\t" "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t"\
                       "Data {data_time.value:.4f} ({data_time.avg:.4f})\t" "Loss {loss.value:.4f} " \
                       "({loss.avg:.4f})\t".format(epoch, i, len(train_data_loader), optimizer.param_groups[0]["lr"],
                                                   batch_time=batch_time, data_time=data_time, loss=losses)

                mesg += system_meter.get_gpu_stats()
                logger.info(mesg)
                system_meter.log_system_stats(True)

    if scheduler.update_type == LRSchedulerUpdateType.EPOCH:
        scheduler.lr_scheduler.step()


def validate(model, val_data_loader, device, val_index_map, system_meter):
    """Gets model results on validation set.

    :param model: Model to score
    :type model: Pytorch nn.Module
    :param val_data_loader: Data loader for validation data
    :type val_data_loader: Pytorch Data Loader
    :param device: Target device
    :type device: Pytorch device
    :param val_index_map: Map from numerical indices to class names
    :type val_index_map: List of strings
    :returns: List of detections
    :rtype: List of ImageBoxes (see object_detection.common.boundingbox)
    :param system_meter: A SystemMeter to collect system properties
    :type system_meter: SystemMeter
    """

    batch_time = AverageMeter()

    model.eval()

    bounding_boxes = []
    end = time.time()
    with torch.no_grad():
        for i, (images, targets, info) in enumerate(_data_exception_safe_iterator(iter(val_data_loader))):
            images = move_images_to_device(images, device)

            labels = model(images)

            for info, label in zip(info, labels):
                image_boxes = boundingbox.ImageBoxes(
                    info["filename"], val_index_map)

                # encode masks as rle to save memory
                masks = label.get("masks", None)
                if masks is not None:
                    masks = masks.cpu()
                    masks = (masks > 0.5)
                    rle_masks = []
                    for mask in masks:
                        rle = masktools.encode_mask_as_rle(mask)
                        rle_masks.append(rle)

                # move predicted labels to cpu
                image_boxes.add_boxes(label["boxes"].cpu(),
                                      label["labels"].cpu(),
                                      label["scores"].cpu(),
                                      rle_masks if masks is not None else None)

                bounding_boxes.append(image_boxes)

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if i % 100 == 0 or i == len(val_data_loader) - 1:
                mesg = "Test: [{0}/{1}]\t" \
                       "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t".format(i, len(val_data_loader),
                                                                                     batch_time=batch_time)
                mesg += system_meter.get_gpu_stats()
                logger.info(mesg)
                system_meter.log_system_stats(collect_only=True)

    return bounding_boxes


def train(model, optimizer, scheduler,
          train_data_loader, device, criterion,
          train_settings, val_data_loader, val_dataset,
          val_metric_type, task_type, val_index_map=None,
          azureml_run=None, log_verbose_metrics=False,
          save_checkpoints=False, output_dir=None,
          enable_onnx_norm=False):
    """Train a model

    :param model: Model to train
    :type model: Object derived from BaseObjectDetectionModelWrapper (see object_detection.models.base_model_wrapper)
    :param optimizer: Model Optimizer
    :type optimizer: Pytorch Optimizer
    :param scheduler: Learning Rate Scheduler wrapper.
    :type scheduler: BaseLRSchedulerWrapper (see common.trainer.lrschedule)
    :param train_data_loader: Data loader with training data
    :type train_data_loader: Pytorch data loader
    :param device: Target device (gpu/cpu)
    :type device: Pytorch Device
    :param criterion: Loss function
    :type criterion: Object derived from CommonCriterionWrapper (see object_detection.train.criterion)
    :param train_settings: Settings for training.
    :type train_settings: TrainSettings object
    :param val_data_loader: Data loader with validation data.
    :type val_data_loader: Pytorch data loader
    :param val_dataset: Validation dataset.
    :type val_dataset: CommonObjectDetectionDatasetWrapper (see object_detection.data.datasets)
    :param val_metric_type: Validation metric evaluation type.
    :type val_metric_type: ValidationMetricType.
    :param task_type: task type
    :type task_type: str
    :param val_index_map: Map from class indices to class names
    :type val_index_map: List of strings
    :param azureml_run: azureml run object
    :type azureml_run: azureml.core.run.Run
    :param log_verbose_metrics: Whether to log verbose metrics to Run History
    :type log_verbose_metrics: bool
    :param save_checkpoints: If True, the checkpoints from each epoch are saved. If False, only the best one.
    :type save_checkpoints: bool
    :param output_dir: Output directory to write checkpoints to
    :type output_dir: str
    :param enable_onnx_norm: enable onnx normalization in the exported model
    :type enable_onnx_norm: bool
    :returns: Trained model
    :rtype: Object derived from CommonObjectDetectionModelWrapper
    """
    epoch_time = AverageMeter()

    base_model = model.model

    distributed = distributed_utils.dist_available_and_initialized()
    master_process = distributed_utils.master_process()

    best_score = 0.0
    best_model = copy.deepcopy(model.state_dict())
    no_progress_counter = 0

    # Setup evaluation tools
    val_coco_index = None
    val_vocmap = None
    if val_metric_type in ValidationMetricType.ALL_COCO:
        val_coco_index = cocotools.create_coco_index(val_dataset)
    if val_metric_type in ValidationMetricType.ALL_VOC:
        val_vocmap = VocMap(val_dataset)

    label_metrics = {}

    epoch_end = time.time()
    train_start = time.time()
    coco_metric_time = AverageMeter()
    voc_metric_time = AverageMeter()
    train_sys_meter = SystemMeter()
    valid_sys_meter = SystemMeter()
    specs = {
        'model_specs': model.specs,
        'classes': model.classes
    }
    for epoch in range(train_settings.number_of_epochs):
        logger.info("Training epoch {}.".format(epoch))

        if distributed:
            if train_data_loader.distributed_sampler is None:
                msg = "train_data_loader.distributed_sampler is None in distributed mode. " \
                      "Cannot shuffle data after each epoch."
                logger.error(msg)
                raise AutoMLVisionSystemException(msg, has_pii=False)
            train_data_loader.distributed_sampler.set_epoch(epoch)

        train_one_epoch(base_model, optimizer, scheduler,
                        train_data_loader, device, criterion, epoch,
                        print_freq=100, system_meter=train_sys_meter)
        # save_checkpoints to be added as a runner param when exposed
        if save_checkpoints and master_process:
            save_model_checkpoint(epoch=epoch,
                                  model_name=model.model_name,
                                  number_of_classes=model.number_of_classes,
                                  specs=specs,
                                  model_state=model.state_dict(),
                                  optimizer_state=optimizer.state_dict(),
                                  lr_scheduler_state=scheduler.lr_scheduler.state_dict(),
                                  output_dir=output_dir,
                                  model_file_name_prefix=str(epoch) + '_')

        bounding_boxes = validate(base_model, val_data_loader, device, val_index_map, valid_sys_meter)
        eval_bounding_boxes = prepare_bounding_boxes_for_eval(bounding_boxes)

        if distributed:
            # Gather eval bounding boxes from all processes.
            eval_bounding_boxes_list = distributed_utils.all_gather(eval_bounding_boxes)
            eval_bounding_boxes = list(itertools.chain.from_iterable(eval_bounding_boxes_list))

            logger.info("Gathered {} eval bounding boxes from all processes.".format(len(eval_bounding_boxes)))

        if not eval_bounding_boxes:
            logger.info("no detected bboxes for evaluation")

        if val_metric_type != ValidationMetricType.NONE:
            map_score = compute_metrics(eval_bounding_boxes, val_metric_type,
                                        val_coco_index, val_vocmap, val_index_map, label_metrics,
                                        coco_metric_time, voc_metric_time, master_process, azureml_run)

            if epoch >= train_settings.early_stop_delay_iterations:
                # Start incrementing no progress counter only after early_stop_delay_iterations.
                no_progress_counter += 1

            # Save best model
            if map_score >= best_score and master_process:
                save_model_checkpoint(epoch=epoch,
                                      model_name=model.model_name,
                                      number_of_classes=model.number_of_classes,
                                      specs=specs,
                                      model_state=model.state_dict(),
                                      optimizer_state=optimizer.state_dict(),
                                      lr_scheduler_state=scheduler.lr_scheduler.state_dict(),
                                      output_dir=output_dir)
                best_model = copy.deepcopy(model.state_dict())

            if map_score > best_score:
                no_progress_counter = 0
                best_score = map_score

            if master_process and azureml_run is not None:
                azureml_run.log(train_settings.primary_metric, round(map_score, 3))
        else:
            logger.info("val_metric_type is None. Not computing metrics.")
            if master_process:
                save_model_checkpoint(epoch=epoch,
                                      model_name=model.model_name,
                                      number_of_classes=model.number_of_classes,
                                      specs=specs,
                                      model_state=model.state_dict(),
                                      optimizer_state=optimizer.state_dict(),
                                      lr_scheduler_state=scheduler.lr_scheduler.state_dict(),
                                      output_dir=output_dir)
                best_model = copy.deepcopy(model.state_dict())

        # measure elapsed time
        epoch_time.update(time.time() - epoch_end)
        epoch_end = time.time()
        msg = "Epoch-level: [{0}]\t" \
              "Epoch-level Time {epoch_time.value:.4f} ({epoch_time.avg:.4f})".format(epoch, epoch_time=epoch_time)
        logger.info(msg)

        if no_progress_counter > train_settings.max_patience_iterations:
            break

    # measure total training time
    train_time = time.time() - train_start
    log_end_training_stats(train_time, epoch_time, train_sys_meter, valid_sys_meter)

    if log_verbose_metrics:
        log_verbose_metrics_to_rh(train_time, epoch_time, train_sys_meter, valid_sys_meter, azureml_run)

    if master_process:
        write_scoring_script(output_dir, task_type=task_type)

        # Write label metrics to output file.
        label_metrics_file_path = os.path.join(output_dir, ArtifactLiterals.LABEL_METRICS_FILE_NAME)
        with open(label_metrics_file_path, 'w') as f:
            json.dump(label_metrics, f)

        model_settings = {} if model.model_settings is None else model.model_settings.get_settings_dict()

        write_artifacts(model_wrapper=model,
                        best_model_weights=best_model,
                        labels=model.classes,
                        output_dir=output_dir,
                        run=azureml_run,
                        best_metric=best_score,
                        task_type=task_type,
                        device=device,
                        enable_onnx_norm=enable_onnx_norm,
                        model_settings=model_settings)
