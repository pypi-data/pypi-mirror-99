# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Convenience functions to create model wrappers."""

import torch

from .object_detection_model_wrappers import ObjectDetectionModelFactory
from .instance_segmentation_model_wrappers import InstanceSegmentationModelFactory
from ..common.constants import ModelNames


def setup_model(model_name, number_of_classes, classes, device, distributed=False, rank=None,
                model_state=None, specs=None, settings=None):
    """Returns model wrapper from name and number of classes.

    :param model_name: Name of model to get
    :type model_name: String
    :param number_of_classes: Number of classes
    :type number_of_classes: Int
    :param classes: list of class names
    :type classes: List
    :param device: device to use
    :type device: torch.device
    :param distributed: flag that indicates if the model is going to be used in distributed mode
    :type distributed: bool
    :param rank: rank of the process in distributed mode
    :type rank: int
    :param model_state: model weights
    :type model_state: dict
    :param specs: model specifications
    :type specs: dict
    :param settings: Settings to initialize model settings from.
    :type settings: dict
    :return: Model wrapper containing model
    :rtype: Object derived from BaseObjectDetectionModelWrapper (See object_detection.model.base_model_wrapper)
    """

    # TODO: this is temporary, the next refactoring step is to use the ObjectDetectionModelFactory
    if model_name == ModelNames.YOLO_V5:
        model_wrapper = _setup_yolo_model(model_name, number_of_classes, model_state, specs)
    else:
        object_detection_model_factory = ObjectDetectionModelFactory()
        instance_segmentation_model_factory = InstanceSegmentationModelFactory()

        if instance_segmentation_model_factory.model_supported(model_name):
            model_factory = instance_segmentation_model_factory
        else:
            model_factory = object_detection_model_factory

        model_wrapper = model_factory.get_model_wrapper(
            model_name=model_name, number_of_classes=number_of_classes,
            model_state=model_state, specs=specs, settings=settings)

    model_wrapper.classes = classes
    model_wrapper.device = device

    # Move base model to device
    model_wrapper.to_device(device)

    if distributed:
        model_wrapper.model = torch.nn.parallel.DistributedDataParallel(model_wrapper.model,
                                                                        device_ids=[rank],
                                                                        output_device=rank)
    model_wrapper.distributed = distributed

    return model_wrapper


def _setup_yolo_model(model_name, number_of_classes, model_state, specs):
    from azureml.contrib.automl.dnn.vision.object_detection_yolo.models.yolo_wrapper import YoloV5Wrapper
    model_wrapper = YoloV5Wrapper(model_name, number_of_classes, specs, model_state)

    # TODO: temporary hack to reduce the amount of refactoring; replace with proper
    # attributes on the model wrapper
    model_wrapper.model.hyp = specs
    model_wrapper.model.nc = number_of_classes

    return model_wrapper
