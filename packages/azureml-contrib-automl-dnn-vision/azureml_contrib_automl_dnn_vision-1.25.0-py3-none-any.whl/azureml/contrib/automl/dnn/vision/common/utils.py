# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Common utilities across classification and object detection."""
import functools
import json
import logging
import numbers
import os
import random
import shutil
import subprocess
import sys
import time
from argparse import ArgumentParser
from typing import Dict, Optional

import cv2
import numpy as np
import torch
from PIL import Image

from azureml._common._error_definition import AzureMLError
from azureml._common.exceptions import AzureMLException
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.inference.inference import AutoMLInferenceArtifactIDs, _get_model_name
from azureml.automl.core.shared import log_server, logging_utilities
from azureml.automl.core.shared.exceptions import ClientException
from azureml.automl.core.shared.logging_fields import TELEMETRY_AUTOML_COMPONENT_KEY
from azureml.automl.core.shared.logging_utilities import _CustomStackSummary, _get_pii_free_message

from azureml.core.experiment import Experiment
from azureml.core.run import Run, _OfflineRun
from azureml.exceptions import ServiceException as AzureMLServiceException
from azureml.telemetry import INSTRUMENTATION_KEY, get_diagnostics_collection_info
from azureml.train.automl import constants
from azureml.train.automl._logging import set_run_custom_dimensions
from azureml.train.automl.constants import ComputeTargets, Tasks

from azureml.contrib.automl.dnn.vision.classification.common.constants import LoggingLiterals
from azureml.contrib.automl.dnn.vision.common import distributed_utils
from azureml.contrib.automl.dnn.vision.common.average_meter import AverageMeter
from azureml.contrib.automl.dnn.vision.common.constants import (ArtifactLiterals, MetricsLiterals, RunPropertyLiterals,
                                                                SettingsLiterals, SystemSettings, Warnings)
from azureml.contrib.automl.dnn.vision.common.errors import AutoMLVisionInternal
from azureml.contrib.automl.dnn.vision.common.exceptions import (AutoMLVisionDataException,
                                                                 AutoMLVisionTrainingException)
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.system_meter import SystemMeter


logger = get_logger(__name__)


def _accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res


def _set_train_run_properties(run, model_name, best_metric):
    """Adds properties to the run that set the score and enable UI export buttons."""

    if run is None:
        raise ClientException('run is None', has_pii=False)

    model_id = _get_model_name(run.id)
    properties_to_add = {
        RunPropertyLiterals.PIPELINE_SCORE: best_metric,
        AutoMLInferenceArtifactIDs.ModelName: model_id,
        "runTemplate": "automl_child",
        "run_algorithm": model_name
    }
    run.add_properties(properties_to_add)


def _get_default_device():
    return torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class AzureAutoMLSettingsStub:
    """Stub for AzureAutoMLSettings class to configure logging."""
    is_timeseries = False
    task_type = None
    compute_target = None
    name = None
    subscription_id = None
    region = None
    verbosity = None
    telemetry_verbosity = None
    send_telemetry = None
    azure_service = None


def _set_logging_parameters(task_type: constants.Tasks,
                            settings: Dict,
                            output_dir: Optional[str] = None,
                            azureml_run: Optional[Run] = None):
    """Sets the logging parameters so that we can track all the training runs from
    a given project.

    :param task_type: The task type for the run.
    :type task_type: str
    :param settings: All the settings for this run.
    :type settings: Dict
    :param output_dir: The output directory.
    :type Optional[str]
    :param azureml_run: The run object.
    :type Optional[Run]
    """
    log_server.update_custom_dimensions({LoggingLiterals.TASK_TYPE: task_type})

    if LoggingLiterals.PROJECT_ID in settings:
        project_id = settings[LoggingLiterals.PROJECT_ID]
        log_server.update_custom_dimensions({LoggingLiterals.PROJECT_ID: project_id})

    if LoggingLiterals.VERSION_NUMBER in settings:
        version_number = settings[LoggingLiterals.VERSION_NUMBER]
        log_server.update_custom_dimensions({LoggingLiterals.VERSION_NUMBER: version_number})

    _set_automl_run_custom_dimensions(task_type, output_dir, azureml_run)


def _set_automl_run_custom_dimensions(task_type: Tasks,
                                      output_dir: Optional[str] = None,
                                      azureml_run: Optional[Run] = None):
    if output_dir is None:
        output_dir = SystemSettings.LOG_FOLDER
    os.makedirs(output_dir, exist_ok=True)

    if azureml_run is None:
        azureml_run = Run.get_context()

    name = "not_available_offline"
    subscription_id = "not_available_offline"
    region = "not_available_offline"
    parent_run_id = "not_available_offline"
    child_run_id = "not_available_offline"
    if not isinstance(azureml_run, _OfflineRun):
        # If needed in the future, we can replace with a uuid5 based off the experiment name
        # name = azureml_run.experiment.name
        name = "online_scrubbed_for_compliance"
        subscription_id = azureml_run.experiment.workspace.subscription_id
        region = azureml_run.experiment.workspace.location
        parent_run_id = azureml_run.parent.id if azureml_run.parent is not None else None
        child_run_id = azureml_run.id

    # Build the automl settings expected by the logger
    send_telemetry, level = get_diagnostics_collection_info(component_name=TELEMETRY_AUTOML_COMPONENT_KEY)
    automl_settings = AzureAutoMLSettingsStub
    automl_settings.is_timeseries = False
    automl_settings.task_type = task_type
    automl_settings.compute_target = ComputeTargets.AMLCOMPUTE
    automl_settings.name = name
    automl_settings.subscription_id = subscription_id
    automl_settings.region = region
    automl_settings.telemetry_verbosity = level
    automl_settings.send_telemetry = send_telemetry

    log_server.set_log_file(os.path.join(output_dir, SystemSettings.LOG_FILENAME))
    if send_telemetry:
        log_server.enable_telemetry(INSTRUMENTATION_KEY)
    log_server.set_verbosity(level)

    set_run_custom_dimensions(
        automl_settings=automl_settings,
        parent_run_id=parent_run_id,
        child_run_id=child_run_id)

    # Add console handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    log_server.add_handler('stdout', stdout_handler)


def _data_exception_safe_iterator(iterator):
    while True:
        try:
            yield next(iterator)
        except AutoMLVisionDataException:
            mesg = "Got AutoMLVisionDataException as all images in the current batch are invalid. Skipping the batch."
            logger.warning(mesg)
            pass
        except StopIteration:
            break


def _read_image(ignore_data_errors, image_url, use_cv2=False):
    try:
        if use_cv2:
            # cv2 can return None in some error cases
            img = cv2.imread(image_url)  # BGR
            if img is None:
                raise AutoMLVisionDataException("cv2.imgread returned None")
            return img
        else:
            return Image.open(image_url).convert('RGB')
    except Exception as ex:
        if ignore_data_errors:
            msg = '{}: since ignore_data_errors is True, file will be ignored.'.format(__file__)
            logger.warning(msg)
        else:
            raise AutoMLVisionDataException(str(ex), has_pii=True)
        return None


def _exception_handler(func, fail_run=True):
    """This decorates a function to handle uncaught exceptions and fail the run with System Error.

    :param fail_run: if True, fail the run. If False, just log the exception and raise it further.
        Note: This is useful when an exception is raised from a child process, because the exception details might not
        reach the parent process, so it's safer to log the contents directly in the child process.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging_utilities.log_traceback(e, logger)

            if not fail_run:
                raise

            if isinstance(e, (AzureMLException, AzureMLServiceException)):
                interpreted_exception = e
            else:
                # This is an unknown exception - try to log as much non PII info in telemetry
                # in case logging is not yest initialized or not working
                error_msg_without_pii = _get_pii_free_message(e)
                traceback_obj = e.__traceback__ if hasattr(e, "__traceback__") else None or sys.exc_info()[2]
                traceback_msg_without_pii = _CustomStackSummary.get_traceback_message(traceback_obj)

                interpreted_exception = ClientException._with_error(
                    AzureMLError.create(AutoMLVisionInternal,
                                        error_details=str(e),
                                        traceback=traceback_msg_without_pii,
                                        pii_safe_message=error_msg_without_pii,
                                        **kwargs),
                    inner_exception=e
                ).with_traceback(traceback_obj)

            run = Run.get_context()
            run_lifecycle_utilities.fail_run(run, interpreted_exception, is_aml_compute=True)
            raise

    return wrapper


def _exception_logger(func):
    """Logs exceptions raised by the wrapped method if they don't have user content.
    This is used in the child processes and the exceptions are raised after logging.
    """
    return _exception_handler(func, fail_run=False)


def _make_arg(arg_name: str) -> str:
    return "--{}".format(arg_name)


def _merge_settings_args_defaults(automl_settings: dict, args_dict: dict, defaults: dict) -> dict:
    """Creates a dictionary that is a superset of the automl_settings, args and defaults.
    The priority is  automl_settings > args > defaults

    :param automl_settings: automl settings object to fill
    :type automl_settings: dict
    :param args_dict: command line arguments dictionary
    :type args_dict: dict
    :param defaults: default values
    :type defaults: dict
    :return: automl settings dictionary with all settings filled in
    :rtype: dict
    """
    merged_settings = {}
    merged_settings.update(defaults)
    merged_settings.update(args_dict)
    merged_settings.update(automl_settings)

    return merged_settings


def add_model_arguments(parser: ArgumentParser) -> ArgumentParser:
    """Add either model or model_name arguments to the parser.

    :param parser: Argument parser
    :type parser: argparse.ArgumentParser
    """
    mutex_group = parser.add_mutually_exclusive_group()
    mutex_group.add_argument(_make_arg(SettingsLiterals.MODEL_NAME), type=str,
                             help="model name")
    mutex_group.add_argument(_make_arg(SettingsLiterals.MODEL), type=str,
                             help="model name and hyperparameter dictionary")


def parse_model_conditional_space(args_dict: dict) -> dict:
    """Parse conditional hyperparameter space in the 'model' argument if present.

    :param args_dict: Dictionary containing the command line arguments
    :type args_dict: dict
    :return: Updated command line arguments dictionary
    :rtype: dict
    """
    if SettingsLiterals.MODEL in args_dict and args_dict[SettingsLiterals.MODEL]:
        model_dict = json.loads(args_dict[SettingsLiterals.MODEL])
        for key, value in model_dict.items():
            args_dict[key] = value

    return args_dict


def _save_image_df(train_df=None, val_df=None, train_index=None, val_index=None, output_dir=None):
    """Save train and validation label info from AMLdataset dataframe in output_dir

    :param train_df: training dataframe
    :type train_df: pandas.core.frame.DataFrame class
    :param val_df: validation dataframe
    :type val_df: pandas.core.frame.DataFrame class
    :param train_index: subset indices of train_df for training after train_val_split()
    :type train_index: <class 'numpy.ndarray'>
    :param val_index: subset indices of train_df for validation after train_val_split()
    :type val_index: <class 'numpy.ndarray'>
    :param output_dir: where to save
    :type output_dir: str
    """
    os.makedirs(output_dir, exist_ok=True)

    train_file = os.path.join(output_dir, 'train_df.csv')
    val_file = os.path.join(output_dir, 'val_df.csv')

    if train_df is not None:
        if train_index is not None and val_index is not None:
            train_df[train_df.index.isin(train_index)].to_csv(train_file, columns=['image_url', 'label'],
                                                              header=False, sep='\t', index=False)
            train_df[train_df.index.isin(val_index)].to_csv(val_file, columns=['image_url', 'label'],
                                                            header=False, sep='\t', index=False)
        elif val_df is not None:
            train_df.to_csv(train_file, columns=['image_url', 'label'], header=False, sep='\t', index=False)
            val_df.to_csv(val_file, columns=['image_url', 'label'], header=False, sep='\t', index=False)


def _extract_od_label(dataset=None, output_file=None):
    """Extract label info from a target dataset from label-file for object detection

    :param dataset: target dataset to extract label info
    :type dataset: <class 'object_detection.data.datasets.CommonObjectDetectionWrapper'>
    :param output_file: output filename
    :type output_file: str
     """
    if dataset is not None:
        image_infos = []
        for idx in dataset._indices:
            fname = dataset._image_urls[idx]
            annotations = dataset._annotations[fname]
            for annotation in annotations:
                ishard = True if annotation.iscrowd else False
                image_dict = {"imageUrl": fname,
                              "label": {"label": annotation.label,
                                        "topX": annotation._x0_percentage,
                                        "topY": annotation._y0_percentage,
                                        "bottomX": annotation._x1_percentage,
                                        "bottomY": annotation._y1_percentage,
                                        "isCrowd": str(ishard)}}
                image_infos.append(image_dict)

        with open(output_file, 'w') as of:
            for info in image_infos:
                json.dump(info, of)
                of.write("\n")


def _save_image_lf(train_ds=None, val_ds=None, output_dir=None):
    """Save train and validation label info from label-files or
    from (object detection) dataset with specific indices in output_dir

    :param train_ds: train file or dataset
    :type train_ds: str
    :param val_ds: validation file or dataset
    :type val_ds: str
    :param output_dir: where to save
    :type output_dir: str
    """
    os.makedirs(output_dir, exist_ok=True)

    train_file = os.path.join(output_dir, ArtifactLiterals.TRAIN_SUB_FILE_NAME)
    val_file = os.path.join(output_dir, ArtifactLiterals.VAL_SUB_FILE_NAME)

    # Check if this is a subset of a Dataset
    if hasattr(train_ds, '_indices') and train_ds._indices is not None:
        _extract_od_label(dataset=train_ds, output_file=train_file)
        _extract_od_label(dataset=val_ds, output_file=val_file)
    else:
        if not os.path.exists(train_file):
            shutil.copy(train_ds, os.path.join(output_dir, os.path.basename(train_file)))
        if not os.path.exists(val_file):
            shutil.copy(val_ds, os.path.join(output_dir, os.path.basename(val_file)))


def _set_random_seed(seed):
    """Set randomization seed

    :param seed: randomization seed
    :type seed: int
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        logger.info('Random number generator initialized with seed={}'.format(seed))


def _set_deterministic(deterministic):
    """Set cuDNN settings for deterministic training

    :param deterministic: flag to enable deterministic training
    :type deterministic: bool
    """
    if deterministic and torch.cuda.is_available():
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        logger.warning('You have chosen to turn on the CUDNN deterministic setting, which can '
                       'slow down your training considerably! You may see '
                       'unexpected behavior when restarting from checkpoints.')


def log_all_metrics(computed_metrics, azureml_run):
    """Logs all metrics passed in the dictionary to the run history of the given run.

    :param computed_metrics: Dictionary with metrics and respective values to be logged to Run History.
    :type computed_metrics: dict
    :param azureml_run: The run object.
    :type azureml_run: azureml.core.run
    """
    if azureml_run is None:
        raise AutoMLVisionTrainingException("Cannot log metrics to Run History since azureml_run is None",
                                            has_pii=False)

    for metric_name, value in computed_metrics.items():
        azureml_run.log(metric_name, value)


def log_verbose_metrics_to_rh(train_time, epoch_time, train_sys_meter, valid_sys_meter, azureml_run):
    """Logs verbose metrics to run history at the end of training.

    :param train_time: Training duration in seconds
    :type train_time: float
    :param epoch_time: Epoch time average meter
    :type epoch_time: AverageMeter
    :param train_sys_meter: SystemMeter for GPU/MEM during training
    :type train_sys_meter: SystemMeter
    :param valid_sys_meter: SystemMeter for GPU/MEM during validation
    :type valid_sys_meter: SystemMeter
    :param azureml_run: The run object.
    :type azureml_run: azureml.core.run
    """
    if not distributed_utils.master_process() or not azureml_run:
        return

    metrics = {}

    metrics[MetricsLiterals.TRAIN_DURATION_SECONDS] = train_time
    metrics[MetricsLiterals.TRAIN_EPOCH_COUNT] = epoch_time.count
    metrics[MetricsLiterals.TRAIN_EPOCH_DURATION_SECONDS_AVG] = epoch_time.avg
    metrics[MetricsLiterals.TRAIN_EPOCH_DURATION_SECONDS_MAX] = epoch_time.max
    metrics[MetricsLiterals.TRAIN_EPOCH_DURATION_SECONDS_MIN] = epoch_time.min

    if train_sys_meter.gpu_mem_usage_accumulator:
        metrics[MetricsLiterals.TRAIN_GPU_MEM_USED_MB_AVG] = \
            train_sys_meter.gpu_mem_usage_accumulator[0][SystemMeter.GPU_MEM_KEY].avg
        metrics[MetricsLiterals.TRAIN_GPU_MEM_USED_MB_MAX] = \
            train_sys_meter.gpu_mem_usage_accumulator[0][SystemMeter.GPU_MEM_KEY].max_val
        metrics[MetricsLiterals.TRAIN_GPU_MEM_USED_MB_MIN] = \
            train_sys_meter.gpu_mem_usage_accumulator[0][SystemMeter.GPU_MEM_KEY].min_val

    if train_sys_meter.gpu_usage_accumulator:
        metrics[MetricsLiterals.TRAIN_GPU_USED_PCT_AVG] = \
            train_sys_meter.gpu_usage_accumulator[0][SystemMeter.GPU_USAGE_KEY].avg
        metrics[MetricsLiterals.TRAIN_GPU_USED_PCT_MAX] = \
            train_sys_meter.gpu_usage_accumulator[0][SystemMeter.GPU_USAGE_KEY].max_val
        metrics[MetricsLiterals.TRAIN_GPU_USED_PCT_MIN] = \
            train_sys_meter.gpu_usage_accumulator[0][SystemMeter.GPU_USAGE_KEY].min_val

    if train_sys_meter.sys_mem_usage_accumulator:
        metrics[MetricsLiterals.TRAIN_SYS_MEM_PCT_AVG] = \
            train_sys_meter.sys_mem_usage_accumulator[SystemMeter.PERCENT].avg
        metrics[MetricsLiterals.TRAIN_SYS_MEM_PCT_MAX] = \
            train_sys_meter.sys_mem_usage_accumulator[SystemMeter.PERCENT].max_val
        metrics[MetricsLiterals.TRAIN_SYS_MEM_PCT_MIN] = \
            train_sys_meter.sys_mem_usage_accumulator[SystemMeter.PERCENT].min_val

        metrics[MetricsLiterals.TRAIN_SYS_MEM_SHARED_MB_AVG] = \
            train_sys_meter.sys_mem_usage_accumulator[SystemMeter.SHARED].avg
        metrics[MetricsLiterals.TRAIN_SYS_MEM_SHARED_MB_MAX] = \
            train_sys_meter.sys_mem_usage_accumulator[SystemMeter.SHARED].max_val
        metrics[MetricsLiterals.TRAIN_SYS_MEM_SHARED_MB_MIN] = \
            train_sys_meter.sys_mem_usage_accumulator[SystemMeter.SHARED].min_val

        metrics[MetricsLiterals.TRAIN_SYS_MEM_USED_MB_AVG] = \
            train_sys_meter.sys_mem_usage_accumulator[SystemMeter.USED].avg
        metrics[MetricsLiterals.TRAIN_SYS_MEM_USED_MB_MAX] = \
            train_sys_meter.sys_mem_usage_accumulator[SystemMeter.USED].max_val
        metrics[MetricsLiterals.TRAIN_SYS_MEM_USED_MB_MIN] = \
            train_sys_meter.sys_mem_usage_accumulator[SystemMeter.USED].min_val

    if valid_sys_meter.gpu_mem_usage_accumulator:
        metrics[MetricsLiterals.VALID_GPU_MEM_USED_MB_AVG] = \
            valid_sys_meter.gpu_mem_usage_accumulator[0][SystemMeter.GPU_MEM_KEY].avg
        metrics[MetricsLiterals.VALID_GPU_MEM_USED_MB_MAX] = \
            valid_sys_meter.gpu_mem_usage_accumulator[0][SystemMeter.GPU_MEM_KEY].max_val
        metrics[MetricsLiterals.VALID_GPU_MEM_USED_MB_MIN] = \
            valid_sys_meter.gpu_mem_usage_accumulator[0][SystemMeter.GPU_MEM_KEY].min_val

    if valid_sys_meter.gpu_usage_accumulator:
        metrics[MetricsLiterals.VALID_GPU_USED_PCT_AVG] = \
            valid_sys_meter.gpu_usage_accumulator[0][SystemMeter.GPU_USAGE_KEY].avg
        metrics[MetricsLiterals.VALID_GPU_USED_PCT_MAX] = \
            valid_sys_meter.gpu_usage_accumulator[0][SystemMeter.GPU_USAGE_KEY].max_val
        metrics[MetricsLiterals.VALID_GPU_USED_PCT_MIN] = \
            valid_sys_meter.gpu_usage_accumulator[0][SystemMeter.GPU_USAGE_KEY].min_val

    if valid_sys_meter.sys_mem_usage_accumulator:
        metrics[MetricsLiterals.VALID_SYS_MEM_PCT_AVG] = \
            valid_sys_meter.sys_mem_usage_accumulator[SystemMeter.PERCENT].avg
        metrics[MetricsLiterals.VALID_SYS_MEM_PCT_MAX] = \
            valid_sys_meter.sys_mem_usage_accumulator[SystemMeter.PERCENT].max_val
        metrics[MetricsLiterals.VALID_SYS_MEM_PCT_MIN] = \
            valid_sys_meter.sys_mem_usage_accumulator[SystemMeter.PERCENT].min_val

        metrics[MetricsLiterals.VALID_SYS_MEM_SHARED_MB_AVG] = \
            valid_sys_meter.sys_mem_usage_accumulator[SystemMeter.SHARED].avg
        metrics[MetricsLiterals.VALID_SYS_MEM_SHARED_MB_MAX] = \
            valid_sys_meter.sys_mem_usage_accumulator[SystemMeter.SHARED].max_val
        metrics[MetricsLiterals.VALID_SYS_MEM_SHARED_MB_MIN] = \
            valid_sys_meter.sys_mem_usage_accumulator[SystemMeter.SHARED].min_val

        metrics[MetricsLiterals.VALID_SYS_MEM_USED_MB_AVG] = \
            valid_sys_meter.sys_mem_usage_accumulator[SystemMeter.USED].avg
        metrics[MetricsLiterals.VALID_SYS_MEM_USED_MB_MAX] = \
            valid_sys_meter.sys_mem_usage_accumulator[SystemMeter.USED].max_val
        metrics[MetricsLiterals.VALID_SYS_MEM_USED_MB_MIN] = \
            valid_sys_meter.sys_mem_usage_accumulator[SystemMeter.USED].min_val

    metrics = round_numeric_values(metrics, 2)

    log_all_metrics(metrics, azureml_run)


def log_script_duration(script_start_time, settings, azureml_run):
    """Given the script start time, measures the total script duration and logs it into Run History.

    :param script_start_time: Starting time of the script measured with time.time()
    :type script_start_time: float
    :param settings: Dictionary with all training and model settings
    :type settings: dict
    :param azureml_run: The run object.
    :type azureml_run: azureml.core.Run
    """
    script_end_time = time.time()
    script_duration_seconds = round(script_end_time - script_start_time, 2)

    logger.info("The script duration was %s seconds.", script_duration_seconds)

    if settings.get(SettingsLiterals.LOG_VERBOSE_METRICS, False):
        azureml_run.log(MetricsLiterals.SCRIPT_DURATION_SECONDS, script_duration_seconds)


def log_end_training_stats(train_time: float,
                           epoch_time: AverageMeter,
                           train_sys_meter: SystemMeter,
                           valid_sys_meter: SystemMeter):
    """Logs the time/utilization stats at the end of training."""
    if distributed_utils.master_process():
        training_time_log = "Total training time {0:.4f} for {1} epochs. " \
                            "Epoch avg: {2:.4f}. ".format(train_time, epoch_time.count, epoch_time.avg)
        mem_stats_log = "Mem stats train: {}. Mem stats validation: {}.".format(
            train_sys_meter.get_avg_mem_stats(), valid_sys_meter.get_avg_mem_stats())
        gpu_stats_log = "GPU stats train: {}. GPU stats validation: {}".format(
            train_sys_meter.get_avg_gpu_stats(), valid_sys_meter.get_avg_gpu_stats())
        logger.info("\n".join([training_time_log, mem_stats_log, gpu_stats_log]))


def _log_end_stats(task: str,
                   time: float,
                   batch_time: AverageMeter,
                   system_meter: SystemMeter):
    """Helper method to logs the time/utilization stats."""
    if distributed_utils.master_process():
        time_log = "Total {0} time {1:.4f} for {2} batches. " \
                   "Batch avg: {3:.4f}. ".format(task, time, batch_time.count, batch_time.avg)
        mem_stats_log = "Mem stats {0}: {1}.".format(task, system_meter.get_avg_mem_stats())
        gpu_stats_log = "GPU stats {0}: {1}.".format(task, system_meter.get_avg_gpu_stats())
        logger.info("\n".join([time_log, mem_stats_log, gpu_stats_log]))


def log_end_scoring_stats(score_time: float,
                          batch_time: AverageMeter,
                          system_meter: SystemMeter):
    """Logs the time/utilization stats at the end of scoring."""
    _log_end_stats("scoring", score_time, batch_time, system_meter)


def log_end_featurizing_stats(featurization_time: float,
                              batch_time: AverageMeter,
                              system_meter: SystemMeter):
    """Logs the time/utilization stats at the end of featurization."""
    _log_end_stats("featurization", featurization_time, batch_time, system_meter)


def is_aml_dataset_input(settings):
    """Helper method to check if the input for training is aml dataset or not.

    :param settings: Training settings.
    :type settings: dict
    """
    return SettingsLiterals.DATASET_ID in settings and \
        settings[SettingsLiterals.DATASET_ID] is not None and \
        settings[SettingsLiterals.DATASET_ID] != ""


def download_required_files(settings, dataset_class, model_factory):
    """Download files required for Aml dataset and model setup.

    This step needs to be done before launching distributed training so that there are no concurrency issues
    where multiple processes are downloading the same file.

    :param settings: Dictionary with all training and model settings
    :type settings: Dict
    :param dataset_class: DatasetWrapper used for Aml Dataset input
    :type dataset_class: Class derived from vision.common.base_aml_dataset_wrapper.AmlDatasetBaseWrapper
    :param model_factory: ModelFactory used to initiate the model
    :type model_factory: Object of a class derived from vision.common.base_model_factory.BaseModelFactory
    """
    # Download aml dataset to local disk
    dataset_id = settings.get(SettingsLiterals.DATASET_ID, None)
    validation_dataset_id = settings.get(SettingsLiterals.VALIDATION_DATASET_ID, None)

    if dataset_id is not None:
        ws = Run.get_context().experiment.workspace
        logger.info("Downloading training dataset files to local disk.")
        dataset_class.download_image_files(dataset_id, ws)
        if validation_dataset_id is not None:
            logger.info("Downloading validation dataset files to local disk.")
            dataset_class.download_image_files(validation_dataset_id, ws)

    # Download pretrained model weights and cache on local disk
    logger.info("Downloading pretrained model weights to local disk.")
    model_name = settings[SettingsLiterals.MODEL_NAME]
    chosen_model_name = model_factory.download_model_weights(model_name=model_name)
    # Update settings with the chosen model_name
    settings[SettingsLiterals.MODEL_NAME] = chosen_model_name


def init_tensorboard():
    """Tries to create a SummaryWriter if tensorboard is installed.

    :return SummaryWriter if tensorboard package is installed, None otherwise
    """
    try:
        from torch.utils.tensorboard import SummaryWriter
        tb_writer = SummaryWriter()
        return tb_writer
    except ImportError:
        logger.info("Tensorboard package is not installed, no logs will be created.")
        return None


def post_warning(azureml_run: Run, warning_message: str):
    """Post a warning to azureml run.

    :param azureml_run: The run object.
    :type azureml_run: Run
    :param warning_message: Warning message.
    :type warning_message: str
    """
    if azureml_run is not None:
        if not isinstance(azureml_run, _OfflineRun):
            try:
                azureml_run._client.run.post_event_warning("Run", warning_message)
            except AzureMLServiceException as ex:
                logging_utilities.log_traceback(ex, logger, is_critical=False)


def warn_for_cpu_devices(device, azureml_run: Run):
    """Post a warning if training using cpu device.

    :param device: Device used for training.
    :type device: str
    :param azureml_run: The run object.
    :type azureml_run: Run
    """
    if device == "cpu":
        warning_message = Warnings.CPU_DEVICE_WARNING.format(torch.__version__)
        logger.info(warning_message)
        if azureml_run is not None:
            post_warning(azureml_run, warning_message)


def _pad(data_list, padding_factor):
    """Pad the dataset so that its length can be evenly divided by padding_factor

    :param data_list: a list of data to be padded
    :type data_list: list
    :param padding_factor: padding factor
    :type padding_factor: int
    :return: a copy of the padded data_list
    :rtype: list
    """
    if padding_factor <= 1 or len(data_list) == 0:
        return data_list
    else:
        data_len = len(data_list)
        remainder = data_len % padding_factor
        padding_len = 0 if remainder == 0 else padding_factor - remainder
        new_data_list = data_list.copy()
        new_data_list += [data_list[i % data_len] for i in range(padding_len)]
        return new_data_list


def _top_initialization(settings):
    """Contains one time init things that all runners should call.

    :param settings: dictionary with automl settings
    :type settings: dict
    :return: None
    """
    # enable traceback logging for remote runs
    os.environ['AUTOML_MANAGED_ENVIRONMENT'] = '1'

    if settings.get(SettingsLiterals.PRINT_LOCAL_PACKAGE_VERSIONS, False):
        print_local_package_versions()


def _distill_run_from_experiment(run_id, experiment_name=None):
    """Get a Run object.

    :param run_id: run id of the run
    :type run_id: str
    :param experiment_name: name of experiment that contains the run id
    :type experiment_name: str
    :return: Run object
    :rtype: Run
    """
    current_experiment = Run.get_context().experiment
    experiment = current_experiment

    if experiment_name is not None:
        workspace = current_experiment.workspace
        experiment = Experiment(workspace, experiment_name)

    return Run(experiment=experiment, run_id=run_id)


def round_numeric_values(dictionary, num_decimals):
    """Round the numeric values of the dictionary to the given number of decimals.

    :param dictionary: Dictionary with the values to be rounded.
    :type dictionary: dict
    :param num_decimals: Number of decimals to use for the rounding.
    :type num_decimals: int
    :return: Dictionary with the values rounded down.
    :rtype: dict
    """
    return_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, numbers.Number):
            return_dict[key] = round(value, num_decimals)
        else:
            return_dict[key] = dictionary[key]

    return return_dict


def print_local_package_versions():
    """Call the "pip list" command to print the list of python packages installed and their versions."""
    print("Checking local pip packages")
    try:
        print()
        subprocess.check_call([sys.executable, "-m", "pip", "list", "--format=freeze"])
        print()
    except Exception as e:
        print("Got exception trying to run pip list: {}".format(e))
