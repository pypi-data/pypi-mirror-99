# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Wrapper for Yolo model"""

import os
import time

import torch

from azureml.contrib.automl.dnn.vision.object_detection.models.base_model_wrapper \
    import BaseObjectDetectionModelWrapper
from azureml.contrib.automl.dnn.vision.common.constants import SettingsLiterals, PretrainedModelUrls, ArtifactLiterals
from azureml.contrib.automl.dnn.vision.object_detection_yolo.common.constants import YoloParameters, \
    training_settings_defaults, YoloLiterals
from azureml.contrib.automl.dnn.vision.object_detection_yolo.models.yolo import Model

from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.object_detection_yolo.utils.utils import check_file
from azureml.contrib.automl.dnn.vision.common.pretrained_model_utilities import PretrainedModelFactory
from azureml.contrib.automl.dnn.vision.common.torch_utils import intersect_dicts
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionSystemException

from torchvision.ops._register_onnx_ops import _onnx_opset_version

from azureml.contrib.automl.dnn.vision.object_detection_yolo.models.common import Conv, Hardswish

logger = get_logger(__name__)


class YoloV5Wrapper(BaseObjectDetectionModelWrapper):
    """YoloV5 Model Wrapper"""
    def __init__(self, model_name, number_of_classes, specs,
                 model_state=None, model_settings=None):
        """
        :param model_name: model name
        :type model_name: str
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param specs: specifications for creating the model
        :type specs: dict
        :param model_state: Model weights. If None, then a new model is created
        :type model_state: dict
        :param model_settings: Model settings.
        :type model_settings: BaseModelSettings
        """
        super().__init__(model_name=model_name, number_of_classes=number_of_classes, specs=specs,
                         model_settings=model_settings)

        self._specs = specs

        load_pretrained_model_dict = model_state is None

        self._model = self._create_model(number_of_classes=number_of_classes, specs=specs)

        if load_pretrained_model_dict:
            model_size = specs[YoloLiterals.MODEL_SIZE]
            size = model_size[0]
            model_size_with_version = self.model_name[:-1] + YoloParameters.DEFAULT_MODEL_VERSION + size

            # Download pretrained model weights based on model size
            pretrained_ckpt = PretrainedModelFactory._load_state_dict_from_url_with_retry(
                PretrainedModelUrls.MODEL_URLS[model_size_with_version])
            # pretrained_ckpt.float()  # to FP32

            state_dict = intersect_dicts(pretrained_ckpt, self.state_dict(), prefix="model.")
            if len(state_dict.keys()) == 0:
                raise AutoMLVisionSystemException("Could not load pre-trained weights. Dict intersection "
                                                  "is empty.", has_pii=False)
            self.load_state_dict(state_dict, strict=False)
        else:
            model_state_with_prefix = {'model.' + k: v for k, v in model_state.items()}
            self.load_state_dict(model_state_with_prefix)

    def _create_model(self, number_of_classes, specs):
        """Create a yolo model

        :param cfg: yaml file for model definition
        :type cfg: string
        :param number_of_classes: number of classes
        :type number_of_classes: int
        :param specs: Dictionary with all training and model settings
        :type specs: Dictionary
        :return: yolo model
        :rtype: <class 'azureml.contrib.automl.dnn.vision.object_detection_yolo.models.yolo.Model'>
        """

        # Find cfg (for model definition) based on model_size
        cfg, model_size = self._find_config(self.model_name, self._specs[YoloLiterals.MODEL_SIZE])
        self._specs[YoloLiterals.MODEL_SIZE] = model_size

        model = Model(model_cfg=cfg, nc=number_of_classes)

        return model

    @staticmethod
    def _find_config(model_name, model_size):
        """Find a file path for cfg

        :param model_name: model name
        :type model_name: str
        :param model_size: model size
        :type model_size: str
        :return: File path for model_cfg
        :rtype: String
        """
        # Verify model_name
        if model_name != training_settings_defaults[SettingsLiterals.MODEL_NAME]:
            logger.warning("[{} model_name is NOT supported, using {} that is supported. "
                           .format(model_name,
                                   training_settings_defaults[SettingsLiterals.MODEL_NAME]))
            model_name = training_settings_defaults[SettingsLiterals.MODEL_NAME]

        # Verify model_size
        size = model_size[0].lower()
        if size not in ['s', 'm', 'l', 'x']:
            logger.warning("[{} model_size is NOT supported. It should start with s, m, l or x. "
                           "Using {} instead]".format(model_size, YoloParameters.DEFAULT_MODEL_SIZE))
            model_size = YoloParameters.DEFAULT_MODEL_SIZE
            size = model_size[0]

        # Find cfg file name based on the model_name and model_size
        cfg = model_name[:-1] + YoloParameters.DEFAULT_MODEL_VERSION + size + '.yaml'

        current_file_path = os.path.dirname(__file__)
        model_cfg = check_file(os.path.join(current_file_path, cfg))

        return model_cfg, model_size

    def export_onnx_model(self, file_path=ArtifactLiterals.ONNX_MODEL_FILE_NAME, device=None, enable_norm=False):
        """
        Export the pytorch model to onnx model file.

        :param file_path: file path to save the exported onnx model.
        :type file_path: str
        :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
        :type device: str
        :param enable_norm: enable normalization when exporting onnx
        :type enable_norm: bool
        """
        # TODO: only a batch size of 1 with fixed image size is supported.
        # TODO: letterbox for input image
        # TODO: post-processing nms
        # TODO: convert to rcnn output format
        onnx_export_start = time.time()

        class ModelNormalizerWrapper(torch.nn.Module):
            def __init__(self, model):
                super(ModelNormalizerWrapper, self).__init__()
                self.model = model
                self.img_size = 640

            def forward(self, x):
                norm_x = self.normalize(x)
                output = self.model(norm_x)
                return output

            def normalize(self, imgs):
                new_imgs = imgs.clone()
                new_imgs /= 255
                return new_imgs

        # Input
        img_size = self.model.hyp['img_size']
        dummy_input = torch.randn(1, 3, img_size, img_size, device=device, requires_grad=False)

        # Update model to replace nn.Hardswish() with export-friendly Hardswish()
        model = self.model
        if device is not None:
            model.to(device=device)
        model.eval()
        for k, m in model.named_modules():
            if isinstance(m, Conv) and isinstance(m.act, torch.nn.Hardswish):
                m.act = Hardswish()  # replace activation

        num_params = sum(x.numel() for x in model.parameters())  # number parameters
        logger.info("[model: ONNX, # layers: {}, # param: {}]".format(len(list(model.parameters())), num_params))

        new_model = model
        if enable_norm:
            dummy_input *= 255.
            new_model = ModelNormalizerWrapper(model)
        torch.onnx.export(new_model,
                          dummy_input,
                          file_path,
                          do_constant_folding=False,
                          opset_version=_onnx_opset_version,
                          input_names=['input'],
                          output_names=['output'],
                          dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}})

        onnx_export_time = time.time() - onnx_export_start
        logger.info('ONNX ({}) export time {:.4f} with enable_onnx_normalization ({})'
                    .format(file_path, onnx_export_time, enable_norm))

    @property
    def model(self):
        """Returns the wrapped model."""
        return self._model

    @property
    def model_size(self):
        """Returns the model size."""
        return self._specs[YoloLiterals.MODEL_SIZE]

    @property
    def specs(self):
        """Returns the model specs."""
        return self._specs
