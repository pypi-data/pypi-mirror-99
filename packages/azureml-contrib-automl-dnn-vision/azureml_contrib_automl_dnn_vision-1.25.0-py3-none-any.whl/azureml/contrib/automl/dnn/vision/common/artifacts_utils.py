# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Functions to help save the artifacts at the end of the training."""

import os
import json
import time

import torch

from azureml.contrib.automl.dnn.vision.common.constants import ArtifactLiterals
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionValidationException
from azureml.contrib.automl.dnn.vision.common.model_export_utils import prepare_model_export
from azureml.contrib.automl.dnn.vision.common.utils import logger, \
    _set_train_run_properties, _distill_run_from_experiment


def write_artifacts(model_wrapper, best_model_weights, labels, output_dir,
                    run, best_metric, task_type, device=None, enable_onnx_norm=False,
                    model_settings=None, is_yolo=False):
    """Export onnx model and write artifacts at the end of training.

    :param model_wrapper: Model wrapper or model
    :type model_wrapper: Union[CommonObjectDetectionModelWrapper, Model]
    :param best_model_weights: weights of the best model
    :type best_model_weights: dict
    :param labels: list of classes
    :type labels: list
    :param output_dir: Name of dir to save model files. If it does not exist, it will be created.
    :type output_dir: String
    :param run: azureml run object
    :type run: azureml.core.run.Run
    :param best_metric: best metric value to store in properties
    :type best_metric: float
    :param task_type: task type
    :type task_type: str
    :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
    :type device: str
    :param enable_onnx_norm: enable normalization when exporting onnx
    :type enable_onnx_norm: bool
    :param model_settings: Settings for the model
    :type model_settings: dict
    :param is_yolo: flag that indicates if the model is a yolo model
    :type is_yolo: bool
    """
    os.makedirs(output_dir, exist_ok=True)

    model_wrapper.load_state_dict(best_model_weights)

    # Export and save the torch onnx model.
    onnx_file_path = os.path.join(output_dir, ArtifactLiterals.ONNX_MODEL_FILE_NAME)
    model_wrapper.export_onnx_model(file_path=onnx_file_path, device=device, enable_norm=enable_onnx_norm)

    # Explicitly Save the labels to a json file.
    if labels is None:
        raise AutoMLVisionValidationException('No labels is found in dataset wrapper', has_pii=False)
    label_file_path = os.path.join(output_dir, ArtifactLiterals.LABEL_FILE_NAME)
    with open(label_file_path, 'w') as f:
        json.dump(labels, f)

    _set_train_run_properties(run, model_wrapper.model_name, best_metric)

    folder_name = os.path.basename(output_dir)
    run.upload_folder(name=folder_name, path=output_dir)

    prepare_model_export(run=run,
                         output_dir=output_dir,
                         task_type=task_type,
                         model_settings=model_settings,
                         is_yolo=is_yolo)


def save_model_checkpoint(epoch, model_name, number_of_classes, specs,
                          model_state, optimizer_state, lr_scheduler_state,
                          output_dir, model_file_name_prefix='',
                          model_file_name=ArtifactLiterals.MODEL_FILE_NAME):
    """Saves a model checkpoint to a file.

    :param epoch: the training epoch
    :type epoch: int
    :param model_name: Model name
    :type model_name: str
    :param number_of_classes: number of classes for the model
    :type number_of_classes: int
    :param specs: model specifications
    :type specs: dict
    :param model_state: model state dict
    :type model_state: dict
    :param optimizer_state: optimizer state dict
    :type optimizer_state: dict
    :param lr_scheduler_state: lr scheduler state
    :type lr_scheduler_state: dict
    :param output_dir: output folder for the checkpoint file
    :type output_dir: str
    :param model_file_name_prefix: prefix to use for the output file
    :type model_file_name_prefix: str
    :param model_file_name: name of the output file that contains the checkpoint
    :type model_file_name: str
    """
    checkpoint_start = time.time()

    os.makedirs(output_dir, exist_ok=True)
    model_location = os.path.join(output_dir, model_file_name_prefix + model_file_name)

    torch.save({
        'epoch': epoch,
        'model_name': model_name,
        'number_of_classes': number_of_classes,
        'specs': specs,
        'model_state': model_state,
        'optimizer_state': optimizer_state,
        'lr_scheduler_state': lr_scheduler_state,
    }, model_location)

    checkpoint_creation_time = time.time() - checkpoint_start
    logger.info('Model checkpoint creation ({}) took {:.2f}s.'
                .format(model_location, checkpoint_creation_time))


def _download_model_from_artifacts(experiment_name, run_id):
    logger.info("Start fetching model from artifacts")
    run = _distill_run_from_experiment(run_id, experiment_name)
    run.download_file(os.path.join(ArtifactLiterals.OUTPUT_DIR, ArtifactLiterals.MODEL_FILE_NAME),
                      ArtifactLiterals.MODEL_FILE_NAME)
    logger.info("Finished downloading files from artifacts")
