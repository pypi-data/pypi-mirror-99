from abc import ABCMeta, abstractmethod
import numpy as np

from torch import Tensor

__all__ = ['AbstractMetric', 'MetricsGroup']


class AbstractMetric(metaclass=ABCMeta):
    """
    Abstract class for metrics. When it works in piepline, it store metric value for every call of :meth:`calc`

    :param name: name of metric. Name wil be used in monitors, so be careful in use unsupported characters
    """

    def __init__(self, name: str):
        self._name = name
        self._values = np.array([])

    @abstractmethod
    def calc(self, output: Tensor, target: Tensor) -> np.ndarray or float:
        """
        Calculate metric by output from model and target

        :param output: output from model
        :param target: ground truth
        """

    def _calc(self, output: Tensor, target: Tensor):
        """
        Calculate metric by output from model and target. Method for internal use

        :param output: output from model
        :param target: ground truth
        """
        self._values = np.append(self._values, self.calc(output, target))

    def name(self) -> str:
        """
        Get name of metric

        :return: metric name
        """
        return self._name

    def get_values(self) -> np.ndarray:
        """
        Get array of metric values

        :return: array of values
        """
        return self._values

    def get_value(self) -> float:
        """
        Get common value of collected metrics values (like mean)

        :return: reduced value
        """
        return float(np.mean(self._values))

    def reset(self) -> None:
        """
        Reset array of metric values
        """
        self._values = np.array([])

    @staticmethod
    def min_val() -> float:
        """
        Get minimum value of metric. This used for correct histogram visualisation in some monitors

        :return: minimum value
        """
        return 0

    @staticmethod
    def max_val() -> float:
        """
        Get maximum value of metric. This used for correct histogram visualisation in some monitors

        :return: maximum value
        """
        return 1


class MetricsGroup:
    """
    Class for unite metrics or another :class:`MetricsGroup`'s in one namespace.
    Note: MetricsGroup may contain only 2 level of :class:`MetricsGroup`'s. So ``MetricsGroup().add(MetricsGroup().add(MetricsGroup()))``
    will raises :class:`MGException`

    :param name: group name. Name wil be used in monitors, so be careful in use unsupported characters
    """

    class MGException(Exception):
        """
        Exception for MetricsGroup
        """

        def __init__(self, msg: str):
            self.__msg = msg

        def __str__(self):
            return self.__msg

    def __init__(self, name: str):
        self.__name = name
        self.__metrics = []
        self.__metrics_groups = []
        self.__lvl = 1

    def add(self, item: AbstractMetric or 'MetricsGroup') -> 'MetricsGroup':
        """
        Add :class:`AbstractMetric` or :class:`MetricsGroup`

        :param item: object to add
        :return: self object
        :rtype: :class:`MetricsGroup`
        """
        if isinstance(item, type(self)):
            item._set_level(self.__lvl + 1)
            self.__metrics_groups.append(item)
        else:
            self.__metrics.append(item)
        return self

    def metrics(self) -> [AbstractMetric]:
        """
        Get list of metrics

        :return: list of metrics
        """
        return self.__metrics

    def groups(self) -> ['MetricsGroup']:
        """
        Get list of metrics groups

        :return: list of metrics groups
        """
        return self.__metrics_groups

    def name(self) -> str:
        """
        Get group name

        :return: name
        """
        return self.__name

    def have_groups(self) -> bool:
        """
        Is this group contains another metrics groups

        :return: True if contains, otherwise - False
        """
        return len(self.__metrics_groups) > 0

    def _set_level(self, level: int) -> None:
        """
        Internal method for set metrics group level
        TODO: if metrics group contains in two groups with different levels - this is undefined case

        :param level: parent group level
        """
        if level > 2:
            raise self.MGException(
                "The metric group {} have {} level. There must be no more than 2 levels".format(self.__name, self.__lvl))
        self.__lvl = level
        for group in self.__metrics_groups:
            group._set_level(self.__lvl + 1)

    def calc(self, output: Tensor, target: Tensor) -> None:
        """
        Recursive calculate all metrics in this group and all nested group

        :param output: predict value
        :param target: target value
        """
        for metric in self.__metrics:
            metric._calc(output, target)
        for group in self.__metrics_groups:
            group.calc(output, target)

    def reset(self) -> None:
        """
        Recursive reset all metrics in this group and all nested group
        """
        for metric in self.__metrics:
            metric.reset()
        for group in self.__metrics_groups:
            group.reset()
