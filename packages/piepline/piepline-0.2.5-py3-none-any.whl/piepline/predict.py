"""
The main module for run inference
"""
from abc import ABCMeta

from torch.nn import Module
from tqdm import tqdm
import torch

from piepline.utils.checkpoints_manager import CheckpointsManager
from piepline.data_producer.data_producer import DataProducer
from piepline.data_processor.data_processor import DataProcessor

__all__ = ['Predictor', 'DataProducerPredictor']


class BasePredictor(metaclass=ABCMeta):
    def __init__(self, model: Module, checkpoints_manager: CheckpointsManager, device: torch.device = None):
        self._data_processor = DataProcessor(model, device=device)

        checkpoints_manager.unpack()
        checkpoints_manager.load_model_weights(model)
        checkpoints_manager.pack()

    def data_processor(self) -> DataProcessor:
        return self._data_processor


class Predictor(BasePredictor):
    """
    Predictor run inference by training parameters

    Args:
        model (Module): model object, used for predict
        checkpoints_manager (:class:`CheckpointsManager`): checkpoints manager
        device (torch.device or str): target device
    """

    def __init__(self, model: Module, checkpoints_manager: CheckpointsManager, device: torch.device or str = None):
        super().__init__(model, checkpoints_manager, device=device)

    def predict(self, data: torch.Tensor or dict):
        """
        Predict one data batch

        :param data: data as :class:`torch.Tensor` or dict with key ``data``
        :return: processed output
        :rtype: model output type
        """
        return self._data_processor.predict(data)


class DataProducerPredictor(BasePredictor):
    def __init__(self, model: Module, checkpoints_manager: CheckpointsManager, device: torch.device = None):
        super().__init__(model, checkpoints_manager, device=device)

    def predict(self, data_producer: DataProducer, callback: callable) -> None:
        """
        Run prediction iterates by ``data_producer``

        :param data_producer: :class:`DataProducer` object
        :param callback: callback, that call for every data prediction and get it's result as parameter
        """
        loader = data_producer.get_loader()

        for img in tqdm(loader):
            callback(self._data_processor.predict(img))
            del img
