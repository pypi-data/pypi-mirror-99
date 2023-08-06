# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper classes and functions for creating dataloaders."""

from torch.utils.data import BatchSampler
from torch.utils.data.distributed import DistributedSampler

from ..common import constants
from ..common.constants import DataLoaderParameterLiterals
from ...common.dataloaders import RobustDataLoader


class DataLoaderParameters:
    """Class that encodes all the parameters used to define a dataloader
    behavior.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs: Optional parameters to define dataloader behavior.
            Currently supports:
            -batch_size: (Int) Number of records in each batch
            -shuffle: (Bool) Whether to shuffle the data in between each epoch
            -num_workers: (Int or None) Number of workers if specified
            -distributed: (Bool) Whether to use a distributed data loader
            -drop_last: (Bool) Whether to drop the last incomplete batch
        :type kwargs: dict
        """
        self._batch_size = kwargs.get(
            DataLoaderParameterLiterals.BATCH_SIZE, constants.DataLoaderParameters.DEFAULT_BATCH_SIZE)
        self._shuffle = kwargs.get(
            DataLoaderParameterLiterals.SHUFFLE, constants.DataLoaderParameters.DEFAULT_SHUFFLE)
        self._num_workers = kwargs.get(
            DataLoaderParameterLiterals.NUM_WORKERS, constants.DataLoaderParameters.DEFAULT_NUM_WORKERS)
        self._distributed = kwargs.get(
            DataLoaderParameterLiterals.DISTRIBUTED, constants.DataLoaderParameters.DEFAULT_DISTRIBUTED)
        self._drop_last = kwargs.get(
            DataLoaderParameterLiterals.DROP_LAST, constants.DataLoaderParameters.DEFAULT_DROP_LAST)

    @property
    def batch_size(self):
        """Get batch size

        :return: Batch size
        :rtype: Int
        """
        return self._batch_size

    @property
    def shuffle(self):
        """Get whether dataset is shuffled between epoch

        :return: Dataset will be shuffled
        :rtype: Bool
        """
        return self._shuffle

    @property
    def num_workers(self):
        """Get number of workers if specified

        :return: Number of workers
        :rtype: Int or None
        """
        return self._num_workers

    @property
    def distributed(self):
        """Get whether to use a distributed data loader

        :return: Distributed or not
        :rtype: Bool
        """
        return self._distributed

    @property
    def drop_last(self):
        """Get whether to drop the last incomplete batch

        :return: drop_last or not
        :rtype: Bool
        """
        return self._drop_last


def setup_dataloader(dataset, **kwargs):
    """Helper function to create dataloader

    :param dataset: Dataset used to create dataloader
    :type dataset: CommonObjectDetectionDatasetWrapper or class derived from CommonObjectDetectionDatasetWrapper
        (see object_detection.data.datasets
    :param kwargs: Optional keyword arguments, currently supported:
        -batch_size: (Int) Number of records per batch
        -shuffle: (Bool) Whether to shuffle the data between epochs
        -num_workers: (Int) Number of workers to use
        -distributed: (Bool) Whether to use a distributed data loader
        -drop_last: (Bool) Whether to drop the last incomplete batch
    :type kwargs: dict
    :return: Dataloader
    :rytpe: Pytorch Dataloader
    """

    parameters = DataLoaderParameters(**kwargs)

    if parameters.distributed:
        sampler = DistributedSampler(dataset, shuffle=parameters.shuffle)
        batch_sampler = BatchSampler(sampler, parameters.batch_size, drop_last=parameters.drop_last)
        # In distributed mode, we launch the distributed workers using torch.multiprocessing.spawn.
        # This sets the multiprocessing context to "spawn" for all multiprocessing operations, including data loader
        # workers launched when num_workers > 1. Using "spawn" is usually slower than the default "fork". This results
        # in the first mini-batch load time in every epoch to be significantly high because workers are created
        # every time a dataloader iterator is created.
        # Set the multiprocessing context as "fork" here to address the high mini-batch load times.
        loader = RobustDataLoader(
            dataset,
            batch_sampler=batch_sampler,
            num_workers=parameters.num_workers,
            multiprocessing_context="fork",
            collate_fn=dataset.collate_function,
            # TODO RK: check impact on FasterRcnn before enabling it?
            # pin_memory=True,
            distributed_sampler=sampler)
    else:
        loader = RobustDataLoader(
            dataset,
            batch_size=parameters.batch_size,
            shuffle=parameters.shuffle,
            num_workers=parameters.num_workers,
            drop_last=parameters.drop_last,
            # TODO RK: check impact on FasterRcnn before enabling it?
            # pin_memory=True,
            collate_fn=dataset.collate_function)

    return loader
