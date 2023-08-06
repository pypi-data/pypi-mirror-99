"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/8 4:57 下午
@Software: PyCharm
@File    : _base.py
@E-mail  : victor.xsyang@gmail.com
"""
import abc
from typing import Any
from typing import Dict

from opts.samples import BaseDistribution
from opts.experiment import Experiment
from opts.trial import FrozenTrial


class BaseSampler(object, metaclass=abc.ABCMeta):
    """Base class for samplers.

    """

    @abc.abstractmethod
    def infer_relative_search_space(
            self, experiment: Experiment,
            trial: FrozenTrial) -> Dict[str, BaseDistribution]:
        """Infer the search space that will be used by relative sampling in the target trial.

        :param experiment:
        :param trial:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def sample_relative(
            self, experiment: Experiment, trial: FrozenTrial,
            search_space: Dict[str, BaseDistribution]
    ) -> Dict[str, Any]:
        """Sample parameters in a given search space.

        :param experiment:
        :param trial:
        :param search_space:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def sample_independent(
            self,
            experiment: Experiment,
            trial: FrozenTrial,
            param_name: str,
            param_distribution: BaseDistribution
    ) -> Any:
        """Sample a parameter for a given distribution.

        :param experiment:
        :param trial:
        :param param_name:
        :param param_distribution:
        :return:
        """
        raise NotImplementedError

    def reseed_rng(self) -> None:
        """Reseed sampler's random number generator.

        :return:
        """
        pass


if __name__ == '__main__':
    pass
