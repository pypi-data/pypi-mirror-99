# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper functions to build model wrappers."""
import torch
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.transform import GeneralizedRCNNTransform
from torchvision.transforms import functional

from .base_model_wrapper import BaseObjectDetectionModelWrapper
from .customrcnn import convert_box_score_thresh_to_float_tensor
from ..common.constants import ModelNames, ModelLiterals, RetinaNetLiterals
from ...common.base_model_factory import BaseModelFactory
from ...common.base_model_settings import BaseModelSettings
from ...common.constants import ArtifactLiterals, PretrainedModelNames
from ...common.exceptions import AutoMLVisionSystemException
from ...common.pretrained_model_utilities import PretrainedModelFactory
from ...common.logging_utils import get_logger

logger = get_logger(__name__)


class CallableGeneralizedRCNNTransform:
    """Wrapper that exposes transforms extracted from GeneralizedRCNNTransform
    to be used when loading data on cpu."""

    def __init__(self, model):
        """Init method.

        :param model: a model that uses GeneralizedRCNNTransform. FasterRCNN or RetinaNet.
        """
        self._gen_rcnn_transform = GeneralizedRCNNTransform(min_size=model.transform.min_size,
                                                            max_size=model.transform.max_size,
                                                            image_mean=model.transform.image_mean,
                                                            image_std=model.transform.image_std)

    @staticmethod
    def identity_batch(images):
        """A NOP batch method.

        :param images: images to batch
        :return: same images
        """
        return images

    @staticmethod
    def identity_normalize(image):
        """A NOP normalization method.

        :param image: image to normalize
        :return: same image
        """
        return image

    @staticmethod
    def identity_resize(image, target_index):
        """A NOP resize method.

        :param image: image to resize.
        :param target_index: target index to resize.
        :return: tuple with same image and target_index.
        """
        return image, target_index

    def inference_transform(self, image):
        """Apply the transform from the model on a single image at inference time.

        :param image: the image to prepare for inference
        :type image: PIL Image
        :return: transformed image
        :rtype: Tensor
        """
        self._gen_rcnn_transform.training = False
        # No need for batching here, as this function is called for each image
        self._gen_rcnn_transform.batch_images = self.identity_batch
        image_tensor = functional.to_tensor(image)
        new_image, _ = self._gen_rcnn_transform(torch.unsqueeze(image_tensor, 0))  # transform expects a batch

        # remove the batch dimension
        return new_image.tensors[0]

    def train_validation_transform(self, is_train, image, boxes, masks=None):
        """Exposes model specific transformations.

        :param is_train: True if the transformations are for training, False otherwise.
        :param image: image tensor, 3 dimensions
        :param boxes: boxes tensor
        :param mask: tensors of masks (unnecessary)
        :return: a tuple with new image, boxes, height and width, and optionally new masks
        """

        self._gen_rcnn_transform.training = is_train
        # No need for batching here, as this function is called for each image
        self._gen_rcnn_transform.batch_images = self.identity_batch

        targets = {"boxes": boxes}

        if masks is not None:
            targets['masks'] = masks

        new_image, new_targets = self._gen_rcnn_transform(torch.unsqueeze(image, 0),  # transform expects a batch
                                                          [targets])
        # remove the batch dimension
        new_image = new_image.tensors[0]
        # the first element of the list contains the boxes for the image,
        # as the batch only has one entry

        new_boxes = new_targets[0]["boxes"]
        new_masks = new_targets[0].get("masks", None)

        new_height = new_image.shape[1]
        new_width = new_image.shape[2]

        return new_image, new_boxes, new_height, new_width, new_masks


class FasterRCNNModelSettings(BaseModelSettings):
    """Model settings for Faster RCNN model."""

    def __init__(self, settings):
        """Initialize model settings from run settings dictionary.

        :param settings: Settings passed into runner.
        :type settings: dict
        """
        if settings is None:
            settings = {}

        valid_keys = [ModelLiterals.MIN_SIZE, ModelLiterals.BOX_SCORE_THRESH,
                      ModelLiterals.BOX_NMS_THRESH, ModelLiterals.BOX_DETECTIONS_PER_IMG]
        self._model_settings = {key: settings[key] for key in valid_keys if key in settings}

    def model_init_kwargs(self):
        """Get kwargs to be used for model initialization.

        :return: kwargs used for initialization
        :rtype: dict
        """
        return self._model_settings

    def get_settings_dict(self):
        """Get settings dict from which model settings object can be re-initialized.

        :return: Settings dictionary
        :rtype: dict
        """
        return self._model_settings


class FasterRCNNResnet50FPNWrapper(BaseObjectDetectionModelWrapper):
    """Model wrapper for Faster RCNN with Resnet50 FPN backbone."""

    def __init__(self, number_of_classes, model_state=None, specs=None,
                 model_name=ModelNames.FASTER_RCNN_RESNET50_FPN, model_settings=None):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: int
        :param model_state: Model weights. If None, then a new model is created
        :type model_state: dict
        :param specs: specifications for creating the model
        :type specs: dict
        :param model_settings: Optional argument to define model settings
        :type model_settings: BaseModelSettings
        """
        super().__init__(model_name=model_name, number_of_classes=number_of_classes, specs=specs,
                         model_settings=model_settings)

        load_pretrained_model_dict = model_state is None

        self._model = self._create_model(number_of_classes=number_of_classes, specs=specs,
                                         load_pretrained_model_dict=load_pretrained_model_dict)

        if not load_pretrained_model_dict:
            self.load_state_dict(model_state)

    @property
    def model(self):
        """Returns the wrapped model."""
        return self._model

    @model.setter
    def model(self, value):
        """Sets the wrapped model.

        :param value: the model
        :type value: nn.Module
        """
        self._model = value

    def _create_model(self, number_of_classes, specs=None, load_pretrained_model_dict=True):
        kwargs = {} if self.model_settings is None else self.model_settings.model_init_kwargs()
        kwargs = convert_box_score_thresh_to_float_tensor(ModelLiterals.BOX_SCORE_THRESH, **kwargs)
        model = PretrainedModelFactory.fasterrcnn_resnet50_fpn(pretrained=True,
                                                               load_pretrained_model_dict=load_pretrained_model_dict,
                                                               **kwargs)

        if number_of_classes is not None:
            input_features = model.roi_heads.box_predictor.cls_score.in_features
            model.roi_heads.box_predictor = FastRCNNPredictor(input_features,
                                                              number_of_classes)

        return model

    def get_inference_transform(self):
        """Get the transformation function to use at inference time."""
        return CallableGeneralizedRCNNTransform(self.model).inference_transform

    def get_train_validation_transform(self):
        """Get the transformation function to use at training and validation time."""
        model = self.model.module if self._distributed else self.model
        return CallableGeneralizedRCNNTransform(model).train_validation_transform

    def disable_model_transform(self):
        """Disable resize and normalize from the model."""
        model = self.model.module if self._distributed else self.model
        model.transform.resize = CallableGeneralizedRCNNTransform.identity_resize
        model.transform.normalize = CallableGeneralizedRCNNTransform.identity_normalize


class RetinaNetModelSettings(BaseModelSettings):
    """Model settings for Retinat model."""

    def __init__(self, settings):
        """Initialize model settings from run settings dictionary.

        :param settings: Settings passed into runner.
        :type settings: dict
        """
        if settings is None:
            settings = {}

        valid_keys = [ModelLiterals.MIN_SIZE, ModelLiterals.BOX_SCORE_THRESH,
                      ModelLiterals.BOX_NMS_THRESH, ModelLiterals.BOX_DETECTIONS_PER_IMG]
        self._model_settings = {key: settings[key] for key in valid_keys if key in settings}

    def model_init_kwargs(self):
        """Get kwargs to be used for model initialization.

        :return: kwargs used for initialization
        :rtype: dict
        """
        # Map ModelLiterals to exact keys expected in RetinaNet kwargs
        retinanet_key_mapping = {
            ModelLiterals.MIN_SIZE: RetinaNetLiterals.MIN_SIZE,
            ModelLiterals.BOX_SCORE_THRESH: RetinaNetLiterals.SCORE_THRESH,
            ModelLiterals.BOX_NMS_THRESH: RetinaNetLiterals.NMS_THRESH,
            ModelLiterals.BOX_DETECTIONS_PER_IMG: RetinaNetLiterals.DETECTIONS_PER_IMG
        }
        kwargs = {retinanet_key_mapping[key]: value for key, value in self._model_settings.items()
                  if key in retinanet_key_mapping}
        return kwargs

    def get_settings_dict(self):
        """Get settings dict from which model settings object can be re-initialized.

        :return: Settings dictionary
        :rtype: dict
        """
        return self._model_settings


class RetinaNetResnet50FPNWrapper(BaseObjectDetectionModelWrapper):
    """Model wrapper for RetinaNet with Resnet50 FPN backbone."""

    def __init__(self, number_of_classes, model_state=None, specs=None,
                 model_name=ModelNames.RETINANET_RESNET50_FPN, model_settings=None):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: int
        :param model_state: Model weights. If None, then a new model is created
        :type model_state: dict
        :param specs: specifications for creating the model
        :type specs: dict
        :param model_settings: Optional argument to define model settings
        :type model_settings: BaseModelSettings
        """

        super().__init__(model_name=model_name, number_of_classes=number_of_classes, specs=specs,
                         model_settings=model_settings)

        load_pretrained_model_dict = model_state is None

        self._model = self._create_model(number_of_classes=number_of_classes, specs=specs,
                                         load_pretrained_model_dict=load_pretrained_model_dict)

        if not load_pretrained_model_dict:
            self.load_state_dict(model_state)

    @property
    def model(self):
        """Returns the wrapped model."""
        return self._model

    @model.setter
    def model(self, value):
        """Sets the wrapped model.

        :param value: the model
        :type value: nn.Module
        """
        self._model = value

    def _create_model(self, number_of_classes, specs=None, load_pretrained_model_dict=True):
        kwargs = {} if self.model_settings is None else self.model_settings.model_init_kwargs()
        kwargs = convert_box_score_thresh_to_float_tensor(RetinaNetLiterals.SCORE_THRESH, **kwargs)
        model = PretrainedModelFactory.retinanet_restnet50_fpn(pretrained=True,
                                                               load_pretrained_model_dict=load_pretrained_model_dict,
                                                               num_classes=number_of_classes,
                                                               **kwargs)
        return model

    def get_inference_transform(self):
        """Get the transformation function to use at inference time."""
        return CallableGeneralizedRCNNTransform(self.model).inference_transform

    def get_train_validation_transform(self):
        """Get the transformation function to use at training and validation time."""
        model = self.model.module if self._distributed else self.model
        return CallableGeneralizedRCNNTransform(model).train_validation_transform

    def disable_model_transform(self):
        """Disable resize and normalize from the model."""
        model = self.model.module if self._distributed else self.model
        model.transform.resize = CallableGeneralizedRCNNTransform.identity_resize
        model.transform.normalize = CallableGeneralizedRCNNTransform.identity_normalize

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
        self._export_onnx_model_with_names(file_path, device, enable_norm,
                                           input_names=['input'], output_names=['boxes', 'scores', 'labels'],
                                           dynamic_axes={'input': {0: 'batch'},
                                                         'boxes': {0: 'prediction'},
                                                         'labels': {0: 'prediction'},
                                                         'scores': {0: 'prediction'}})


class ObjectDetectionModelFactory(BaseModelFactory):
    """Factory function to create models."""

    def __init__(self):
        """Init method."""
        super().__init__()

        self._models_dict = {
            ModelNames.FASTER_RCNN_RESNET50_FPN: FasterRCNNResnet50FPNWrapper,
            ModelNames.RETINANET_RESNET50_FPN: RetinaNetResnet50FPNWrapper
        }

        self._pre_trained_model_names_dict = {
            ModelNames.FASTER_RCNN_RESNET50_FPN: PretrainedModelNames.FASTERRCNN_RESNET50_FPN_COCO,
            ModelNames.RETINANET_RESNET50_FPN: PretrainedModelNames.RETINANET_RESNET50_FPN_COCO
        }

        self._model_settings_dict = {
            ModelNames.FASTER_RCNN_RESNET50_FPN: FasterRCNNModelSettings,
            ModelNames.RETINANET_RESNET50_FPN: RetinaNetModelSettings
        }

        self._default_model = ModelNames.FASTER_RCNN_RESNET50_FPN

    def get_model_wrapper(self, number_of_classes, model_name=None, model_state=None, specs=None,
                          settings=None):
        """ Get the wrapper for a fasterrcnn model

        :param number_of_classes: number of classes in object detection
        :type number_of_classes: int
        :param model_name: string name of the model
        :type model_name: str
        :param model_state: model weights
        :type model_state: dict
        :param specs: model specifications
        :type specs: dict
        :param settings: Settings to initialize model settings from
        :type settings: dict
        """

        if model_name is None:
            model_name = self._default_model

        if model_name not in self._models_dict:
            raise ValueError('Unsupported model')

        if model_name not in self._model_settings_dict:
            raise AutoMLVisionSystemException("Model name {} does not have corresponding model settings class."
                                              .format(model_name))
        model_settings = self._model_settings_dict[model_name](settings=settings)

        return self._models_dict[model_name](number_of_classes=number_of_classes,
                                             model_state=model_state,
                                             specs=specs,
                                             model_settings=model_settings)
