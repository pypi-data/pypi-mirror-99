# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Classes that define a common interface for all optimizers."""

from abc import ABC, abstractmethod

from azureml.contrib.automl.dnn.vision.object_detection.trainer.learning_parameters import OptimizerParameters
from azureml.contrib.automl.dnn.vision.object_detection.common import constants
import torch.optim

from azureml.automl.core.shared.exceptions import ClientException

from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionTrainingException


class BaseOptimizerWrapper(ABC):
    """Class that defines a common interface for all optimizers."""

    def __init__(self, learning_parameters, model, trainable_parameters=None):
        """
        :param learning_parameters: Parameters that define behavior of the optimizer
        :type learning_parameters: OptimizerParameters (see object_detection.train.learning_parameters)
        :param model: Model to be optimized
        :type model: Pytorch nn.module
        :param trainable_parameters: Parameters that can be trained
        :type trainable_parameters: List of Pytorch parameters
        """
        self._learning_parameters = learning_parameters
        self._model = model
        self._trainable_parameters = trainable_parameters

        self._optimizer = None

    @property
    def optimizer(self):
        """Get the optimizer

        :return: Pytorch Optimizer
        :rtype: Pytorch Optimizer
        """
        return self._optimizer

    @abstractmethod
    def state_dict(self):
        """Returns the state of the optimizer as a dictionary.

        :return dictionary with the object state
        :rtype dict
        """
        pass

    @abstractmethod
    def load_state_dict(self, state_dict):
        """Loads the optimizer state.

        :param state_dict: dictionary containing the state of the optimizer.
        :type state_dict: dict
        """
        pass


class SGDWrapper(BaseOptimizerWrapper):
    """Wraps Stochastic Gradient Descent Optimizer."""

    def __init__(self, learning_parameters, model=None, trainable_parameters=None):
        """
        :param learning_parameters: Parameters that define behavior of the optimizer. SGD supports:
                                        -learning rate (lr)
                                        -momentum (momentum)
                                        -weight decay (weight_decay)
        :type learning_parameters: OptimizerParameters (see object_detection.train.learning_parameters)
        :param model: Model to be optimized
        :type model: Pytorch nn.module
        :param trainable_parameters (optional): Parameters that can be trained, defaults to retrain all parameters.
        :type trainable_parameters (optional): List of Pytorch parameters
        """
        super().__init__(learning_parameters=learning_parameters,
                         model=model,
                         trainable_parameters=trainable_parameters)

        self._learning_rate = (learning_parameters.learning_rate if
                               learning_parameters.learning_rate is not None else
                               constants.LearningParameters.SGD_DEFAULT_LEARNING_RATE)

        self._momentum = (learning_parameters.momentum if
                          learning_parameters.momentum is not None else
                          constants.LearningParameters.SGD_DEFAULT_MOMENTUM)

        self._weight_decay = (learning_parameters.weight_decay if
                              learning_parameters.weight_decay is not None else
                              constants.LearningParameters.SGD_DEFAULT_WEIGHT_DECAY)

        if trainable_parameters is None and model is None:
            raise AutoMLVisionTrainingException("Model and training_parameters cannot be both None.")

        if trainable_parameters is not None:
            self._trainable_parameters = trainable_parameters
        else:
            self._trainable_parameters = [param for param in model.parameters()
                                          if param.requires_grad]

        self._optimizer = torch.optim.SGD(self._trainable_parameters,
                                          lr=self._learning_rate,
                                          momentum=self._momentum,
                                          weight_decay=self._weight_decay)

    def state_dict(self):
        """Returns the state of the optimizer as a dictionary.

        :return dictionary with the object state
        :rtype dict
        """
        return self._optimizer.state_dict()

    def load_state_dict(self, state_dict):
        """Loads the optimizer state.

        :param state_dict: dictionary containing the state of the optimizer.
        :type state_dict: dict
        """
        self._optimizer.load_state_dict(state_dict)


class OptimizerFactory:
    """Factory class that creates optimizer wrappers."""

    _optimizers_dict = {
        constants.OptimizerNames.SGD: SGDWrapper
    }

    @staticmethod
    def _get_optimizer(optimizer_name, model, learning_parameters, trainable_parameters=None):
        """Create an optimizer

        :param optimizer_name: Name of the optimizer. Currently supported: -Stochastic Gradient Descent (SGD)
        :type optimizer_name: String
        :param model: Model to be optimized
        :type model: pytorch model
        :param learning_parameters: Parameters for optimizer
        :type learning_parameters: OptimizerParameters (see torch.train.learning_parameters
        :param trainable_parameters: Trainable parameters
        :type trainable_parameters: Trainable parameters
        :returns: Pytorch Optimizer
        :rtype: Pytorch Optimizer
        """
        if optimizer_name is None:
            optimizer_name = constants.OptimizerNames.DEFAULT_OPTIMIZER

        if optimizer_name not in OptimizerFactory._optimizers_dict:
            raise ClientException('{} not supported'.format(optimizer_name)) \
                .with_generic_msg("Optimizer name not supported.")

        return OptimizerFactory._optimizers_dict[optimizer_name](model=model,
                                                                 learning_parameters=learning_parameters,
                                                                 trainable_parameters=trainable_parameters).optimizer


def setup_optimizer(model, optimizer=None, trainable_parameters=None, **kwargs):
    """Convenience function that wraps creating an optimizer.

    :param model: Model to be optimized
    :type model: Pytorch model
    :param optimizer: (optional) name of optimizer. Defaults to SGD.
    :type optimizer: (optional) str
    :param trainable_parameters: Trainable parameters
    :type trainable_parameters: Trainable parameters
    :param kwargs: Optional Parameters for optimizer
    :type kwargs: dict
    :returns: Pytorch optimizer
    :rtype: Pytorch optimizer
    """
    optimizer_parameters = OptimizerParameters(**kwargs)

    optimizer_factory = OptimizerFactory()

    return optimizer_factory._get_optimizer(optimizer, model, optimizer_parameters, trainable_parameters)
