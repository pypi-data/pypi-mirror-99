# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines transformation functions for the package."""
from azureml.automl.core.shared.exceptions import ClientException

try:
    from torchvision import transforms
except ImportError:
    print('ImportError: torch not installed. If on windows, install torch, pretrainedmodels, torchvision and '
          'pytorch-ignite separately before running the package.')


def _get_common_train_transforms(input_size):
    """Get train transformation that works for most common classification cases.

    :param input_size:
    :type input_size: int
    :return: Transform object for training
    :rtype: object
    """
    return transforms.Compose([
        transforms.RandomResizedCrop(input_size),
        transforms.RandomHorizontalFlip(),
        transforms.RandomChoice([
            transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0.4),
            transforms.Lambda(_identity),
        ]),
        transforms.ToTensor(),
        transforms.Lambda(_make_3d_tensor),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


def _get_common_valid_transforms(resize_to=None, crop_size=None):
    """Get validation transformation which is just cropping the input after a resize.

    :param resize_to: square size to resize to
    :type resize_to: int
    :param crop_size: final input size to crop the image to
    :type crop_size: int
    :return: Transform object for validation
    :rtype: object
    """
    if resize_to is None or crop_size is None:
        raise ClientException('one of crop_size or input_size is None', has_pii=False)

    return transforms.Compose([
        transforms.Resize(resize_to),
        transforms.CenterCrop(crop_size),
        transforms.ToTensor(),
        transforms.Lambda(_make_3d_tensor),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


def _identity(x):
    """Identity transformation.

    :param x: input tensor
    :type x: torch.Tensor
    :return: return the input as is
    :rtype: torch.Tensor
    """
    return x


def _make_3d_tensor(x):
    """This function is for images that have less channels.

    :param x: input tensor
    :type x: torch.Tensor
    :return: return a tensor with the correct number of channels
    :rtype: torch.Tensor
    """
    return x if x.shape[0] == 3 else x.expand((3, x.shape[1], x.shape[2]))
