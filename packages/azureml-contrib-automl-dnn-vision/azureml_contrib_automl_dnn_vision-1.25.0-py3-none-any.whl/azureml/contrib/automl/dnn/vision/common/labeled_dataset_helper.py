# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Common helper class for reading labeled Aml Datasets."""

import json
import os
import tempfile
import time
import uuid
import azureml.dataprep as dprep
from azureml.dataprep import ExecutionError
from azureml.dataprep.api.functions import get_portable_path

from azureml.core import Dataset as AmlDataset
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionDataException

from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger

logger = get_logger(__name__)


class AmlLabeledDatasetHelper:
    """Helper for AzureML labeled dataset.

    """

    LABEL_COLUMN_PROPERTY = '_Label_Column:Label_'
    DEFAULT_LABEL_COLUMN_NAME = 'label'
    DEFAULT_LABEL_CONFIDENCE_COLUMN_NAME = 'label_confidence'
    COLUMN_PROPERTY = 'Column'
    IMAGE_COLUMN_PROPERTY = '_Image_Column:Image_'
    DEFAULT_IMAGE_COLUMN_NAME = 'image_url'
    PORTABLE_PATH_COLUMN_NAME = 'PortablePath'
    DATASTORE_PREFIX = 'AmlDatastore://'
    PATH_COLUMN_NAME = 'Path'

    def __init__(self, dataset_id, workspace=None,
                 ignore_data_errors=False, datasetclass=AmlDataset,
                 image_column_name=DEFAULT_IMAGE_COLUMN_NAME,
                 download_files=True):
        """Constructor - This reads the labeled dataset and downloads the images that it contains.

        :param dataset_id: dataset id
        :type dataset_id: str
        :param workspace: workspace object
        :type workspace: azureml.core.Workspace
        :param ignore_data_errors: Setting this ignores and files in the labeled dataset that fail to download.
        :type ignore_data_errors: bool
        :param datasetclass: The source dataset class.
        :type datasetclass: class
        :param image_column_name: The column name for the image file.
        :type image_column_names: str
        :param download_files: Flag to download files or not.
        :type download_files: bool
        """

        self._data_dir = AmlLabeledDatasetHelper.get_data_dir()

        ds = datasetclass.get_by_id(workspace, dataset_id)

        self.image_column_name = AmlLabeledDatasetHelper.get_image_column_name(
            ds, image_column_name)
        self.label_column_name = AmlLabeledDatasetHelper.get_label_column_name(
            ds, AmlLabeledDatasetHelper.DEFAULT_LABEL_COLUMN_NAME)

        if download_files:
            AmlLabeledDatasetHelper.download_image_files(ds, self.image_column_name)

        dflow = ds._dataflow.add_column(get_portable_path(dprep.col(self.image_column_name)),
                                        AmlLabeledDatasetHelper.PORTABLE_PATH_COLUMN_NAME, self.image_column_name)
        self.images_df = dflow.to_pandas_dataframe(extended_types=True)

        if ignore_data_errors:
            missing_file_indices = []
            for index in self.images_df.index:
                full_path = self.get_image_full_path(index)
                if not os.path.exists(full_path):
                    missing_file_indices.append(index)
            self.images_df.drop(missing_file_indices, inplace=True)
            self.images_df.reset_index(inplace=True, drop=True)

    def get_image_full_path(self, index):
        """Return the full local path for an image.

        :param index: index
        :type index: int
        :return: Full path for the local image file
        :rtype: str
        """
        return AmlLabeledDatasetHelper.get_full_path(index, self.images_df, self._data_dir)

    def get_file_name_list(self):
        """Return a list of the relative file names for the images.

        :return: List of the relative file names for the images
        :rtype: list(str)
        """
        return self.images_df[AmlLabeledDatasetHelper.PORTABLE_PATH_COLUMN_NAME].tolist()

    @staticmethod
    def get_full_path(index, images_df, data_dir):
        """Return the full local path for an image.

        :param index: index
        :type index: int
        :param images_df: DataFrame containing images.
        :type images_df: Pandas DataFrame
        :param data_dir: data folder
        :type data_dir: str
        :return: Full path for the local image file
        :rtype: str
        """
        image_rel_path = images_df[AmlLabeledDatasetHelper.PORTABLE_PATH_COLUMN_NAME][index]
        # the image_rel_path can sometimes be an exception from dataprep
        if type(image_rel_path) is not str:
            logger.warning("The relative path of the image is of type {}, "
                           "expecting a string. Will ignore the image.".format(type(image_rel_path)))
            image_rel_path = "_invalid_"
        return data_dir + '/' + image_rel_path

    @staticmethod
    def write_dataset_file_line(fw, image_file_name, confidence, label):
        """Write a line to the dataset file.

        :param fw: The file to write to.
        :type fw: file
        :param image_file_name: The image file name with path within the datastore.
        :type image_file_name: str
        :param confidence: Label confidence value between 0.0 and 1.0
        :type confidence: float
        :param label: The label name.
        :type label: str
        """

        image_full_path = AmlLabeledDatasetHelper.DATASTORE_PREFIX + image_file_name

        fw.write(
            json.dumps(
                {
                    AmlLabeledDatasetHelper.DEFAULT_IMAGE_COLUMN_NAME: image_full_path,
                    AmlLabeledDatasetHelper.DEFAULT_LABEL_CONFIDENCE_COLUMN_NAME: confidence,
                    AmlLabeledDatasetHelper.DEFAULT_LABEL_COLUMN_NAME: label
                }
            )
        )
        fw.write('\n')

    @staticmethod
    def create(run, datastore, labeled_dataset_file, target_path,
               task, labeled_dataset_factory,
               dataset_id_property_name='labeled_dataset_id'):
        """Create a labeled dataset file.

        :param run: AzureML Run to write the dataset id to..
        :type run: Run
        :param datastore: The AML datastore to store the Dataset file.
        :type datastore: Datastore
        :param labeled_dataset_file: The name of the Labeled Dataset file.
        :type labeled_dataset_file: str
        :param target_path: The path for the Labeled Dataset file in Datastore
        :type target_path: str
        :param task: The type of Labeled Dataset
        :type task: str
        :param labeled_dataset_factory: The labeled dataset factory class.
        :type labeled_dataset_factory: _LabeledDatasetFactory
        :param dataset_id_property_name: The name of the dataset id property
        :type dataset_id_property_name: str
        """
        labeled_dataset_file_dirname, labeled_dataset_file_basename = os.path.split(labeled_dataset_file)
        datastore.upload_files(files=[labeled_dataset_file], target_path=target_path,
                               relative_root=labeled_dataset_file_dirname, overwrite=True)
        labeled_dataset_path = target_path + '/' + labeled_dataset_file_basename
        dataset = labeled_dataset_factory.from_json_lines(task=task,
                                                          path=datastore.path(labeled_dataset_path))
        run.add_properties({dataset_id_property_name: dataset.id})

    @staticmethod
    def get_default_target_path():
        """Get the default target path in datastore to be used for Labeled Dataset files.

            :return: The default target path
            :rtype: str
            """
        return 'automl/datasets/' + str(uuid.uuid4())

    @staticmethod
    def get_data_dir():
        """Get the data directory to download the image files to.

        :return: Data directory path
        :type: str
        """
        return tempfile.gettempdir()

    @staticmethod
    def _get_column_name(ds: AmlDataset,
                         parent_column_property: str,
                         default_value: str):
        if parent_column_property in ds._properties:
            image_property = ds._properties[parent_column_property]
            if AmlLabeledDatasetHelper.COLUMN_PROPERTY in image_property:
                return image_property[AmlLabeledDatasetHelper.COLUMN_PROPERTY]
            lower_column_property = AmlLabeledDatasetHelper.COLUMN_PROPERTY.lower()
            if lower_column_property in image_property:
                return image_property[lower_column_property]
        return default_value

    @staticmethod
    def get_image_column_name(ds, default_image_column_name):
        """Get the image column name by inspecting AmlDataset properties.
        Return default_image_column_name if not found in properties.

        :param ds: Aml Dataset object
        :type ds: TabularDataset (Labeled) or FileDataset
        :param default_image_column_name: default value to return
        :type default_image_column_name: str
        :return: Image column name
        :rtype: str
        """
        return AmlLabeledDatasetHelper._get_column_name(ds,
                                                        AmlLabeledDatasetHelper.IMAGE_COLUMN_PROPERTY,
                                                        default_image_column_name)

    @staticmethod
    def get_label_column_name(ds, default_label_column_name):
        """Get the label column name by inspecting AmlDataset properties.
        Return default_label_column_name if not found in properties.

        :param ds: Aml Dataset object
        :type ds: TabularDataset (Labeled) or FileDataset
        :param default_label_column_name: default value to return
        :type default_label_column_name: str
        :return: Label column name
        :rtype: str
        """
        return AmlLabeledDatasetHelper._get_column_name(ds,
                                                        AmlLabeledDatasetHelper.LABEL_COLUMN_PROPERTY,
                                                        default_label_column_name)

    @staticmethod
    def download_image_files(ds, image_column_name):
        """Helper method to download dataset files.

        :param ds: Aml Dataset object
        :type ds: TabularDataset (Labeled) or FileDataset
        :param image_column_name: The column name for the image file.
        :type image_column_names: str
        :return:
        """
        logger.info("Start downloading image files")
        start_time = time.perf_counter()
        data_dir = AmlLabeledDatasetHelper.get_data_dir()
        try:
            ds._dataflow.write_streams(image_column_name, dprep.LocalFileOutput(data_dir)).run_local()
        except ExecutionError as e:
            raise AutoMLVisionDataException(
                "Could not download dataset files. "
                "Please check the logs for more details. Error Code: {}".format(e.error_code))

        logger.info("Downloading image files took {:.2f} seconds".format(time.perf_counter() - start_time))
