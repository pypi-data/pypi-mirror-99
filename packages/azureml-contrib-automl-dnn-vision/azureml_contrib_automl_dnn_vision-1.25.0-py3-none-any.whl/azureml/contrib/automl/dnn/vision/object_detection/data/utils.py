# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper classes and functions for creating operating with datasets and dataloaders."""

from azureml.automl.core.shared.exceptions import ClientException
from azureml.core import Run

from azureml.contrib.automl.dnn.vision.common.utils import _save_image_df, _save_image_lf
from azureml.contrib.automl.dnn.vision.object_detection.data import datasets


def read_aml_dataset(dataset_id, validation_dataset_id, ignore_data_errors, output_dir, master_process,
                     dataset_class=datasets.AmlDatasetObjectDetectionWrapper,
                     settings=None, download_files=False):
    """Read the training and validation datasets from AML datasets.

    :param dataset_id: Training dataset id
    :type dataset_id: str
    :param validation_dataset_id: Validation dataset id
    :type dataset_id: str
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dir: where to save train and val files
    :type output_dir: str
    :param master_process: boolean flag indicating whether current process is master or not.
    :type master_process: bool
    :param dataset_class: the class to use to instantiate the dataset
    :type dataset_class: Class
    :param settings: dictionary of settings to be passed to the dataset
    :type settings: dict
    :param download_files: flag to indicate if files should be downloaded. Assumption is that aml dataset
                           files are already downloaded to local path by a call to download_required_files()
    :type download_files: bool
    :return: Training dataset and validation dataset
    :rtype: Tuple of form (AmlDatasetObjectDetectionWrapper, AmlDatasetObjectDetectionWrapper)
    """
    ws = Run.get_context().experiment.workspace

    if validation_dataset_id is not None:
        training_dataset = dataset_class(dataset_id=dataset_id, is_train=True,
                                         ignore_data_errors=ignore_data_errors,
                                         workspace=ws, download_files=download_files,
                                         settings=settings)
        validation_dataset = dataset_class(dataset_id=validation_dataset_id, is_train=False,
                                           ignore_data_errors=ignore_data_errors,
                                           workspace=ws, download_files=download_files,
                                           settings=settings)
        if master_process:
            _save_image_df(train_df=training_dataset.get_images_df(),
                           val_df=validation_dataset.get_images_df(),
                           output_dir=output_dir)

    else:
        dataset = dataset_class(dataset_id=dataset_id, is_train=True,
                                ignore_data_errors=ignore_data_errors,
                                workspace=ws, download_files=download_files,
                                settings=settings)
        training_dataset, validation_dataset = dataset.train_val_split()
        if master_process:
            _save_image_df(train_df=dataset.get_images_df(), train_index=training_dataset._indices,
                           val_index=validation_dataset._indices, output_dir=output_dir)

    return training_dataset, validation_dataset


def read_file_dataset(image_folder, annotations_file, annotations_test_file, ignore_data_errors,
                      output_dir, master_process,
                      dataset_class=datasets.FileObjectDetectionDatasetWrapper,
                      settings=None):
    """Read the training and validation datasets from annotation files.

    :param image_folder: target image path
    :type image_folder: str
    :param annotations_file: Training annotations file
    :type annotations_file: str
    :param annotations_test_file: Validation annotations file
    :type annotations_test_file: str
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dir: where to save train and val files
    :type output_dir: str
    :param master_process: boolean flag indicating whether current process is master or not.
    :type master_process: bool
    :param dataset_class: the class to use to instanciate the dataset
    :type dataset_class: Class
    :param settings: dictionary of settings to be passed to the dataset
    :type settings: dict
    :return: Training dataset and validation dataset
    :rtype: Tuple of form (FileObjectDetectionDatasetWrapper, FileObjectDetectionDatasetWrapper)
    """
    if annotations_file is None:
        raise ClientException("labels_file needs to be specified", has_pii=False)

    if annotations_test_file:
        training_dataset = dataset_class(annotations_file, image_folder,
                                         is_train=True,
                                         ignore_data_errors=ignore_data_errors,
                                         settings=settings)
        validation_dataset = dataset_class(annotations_test_file,
                                           image_folder, is_train=False,
                                           ignore_data_errors=ignore_data_errors,
                                           settings=settings)
        if master_process:
            _save_image_lf(train_ds=annotations_file, val_ds=annotations_test_file, output_dir=output_dir)
    else:
        dataset = dataset_class(annotations_file, image_folder, is_train=True,
                                ignore_data_errors=ignore_data_errors,
                                settings=settings)
        training_dataset, validation_dataset = dataset.train_val_split()
        if master_process:
            _save_image_lf(train_ds=training_dataset, val_ds=validation_dataset, output_dir=output_dir)

    return training_dataset, validation_dataset
