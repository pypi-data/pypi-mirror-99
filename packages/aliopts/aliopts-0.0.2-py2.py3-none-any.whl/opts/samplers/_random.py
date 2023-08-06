"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/9 11:27 上午
@Software: PyCharm
@File    : _random.py
@E-mail  : victor.xsyang@gmail.com
"""
from typing import Any
from typing import Dict
from typing import Optional

import numpy

from opts import samples
from opts.samples import BaseDistribution
from opts.samplers import BaseSampler
from opts.experiment import Experiment
from opts.trial import FrozenTrial


class RandomSampler(BaseSampler):
    """Sampler using random sampling.
    This sampler is based on *independent sampling*.
    """
    def __init__(self, seed: Optional[int] = None) -> None:
        self._rng = numpy.random.RandomState(seed)

    def reseed_rng(self) -> None:
        self._rng = numpy.random.RandomState()

    def infer_relative_search_space(
            self, experiment: Experiment,
            trial: FrozenTrial) -> Dict[str, BaseDistribution]:
        return {}

    def sample_relative(
            self, experiment: Experiment, trial: FrozenTrial,
            search_space: Dict[str, BaseDistribution]
    ) -> Dict[str, Any]:
        return {}

    def sample_independent(
            self,
            experiment: Experiment,
            trial: FrozenTrial,
            param_name: str,
            param_distribution: BaseDistribution
                           ) -> Any:
        if isinstance(param_distribution, samples.UniformDistribution):
            return self._rng.uniform(param_distribution.low, param_distribution.high)
        elif isinstance(param_distribution, samples.LogUniformDistribution):
            log_low = numpy.log(param_distribution.low)
            log_high = numpy.log(param_distribution.high)
            return float(numpy.exp(self._rng.uniform(log_low, log_high)))
        elif isinstance(param_distribution, samples.DiscreteUniformDistribution):
            q = param_distribution.q
            r = param_distribution.high - param_distribution.low
            low = 0 - 0.5 * q
            high = r + 0.5 * q
            s = self._rng.uniform(low, high)
            v = numpy.round(s / q) * q + param_distribution.low
            return float(min(max(v, param_distribution.low), param_distribution.high))
        elif isinstance(param_distribution, samples.IntUniformDistribution):
            r = (param_distribution.high - param_distribution.low) / param_distribution.step
            s = self._rng.randint(0, r+1)
            v = s * param_distribution.step + param_distribution.low
            return int(v)
        elif isinstance(param_distribution, samples.IntLogUniformDistribution):
            log_low = numpy.log(param_distribution.low - 0.5)
            log_high = numpy.log(param_distribution.high + 0.5)
            s = numpy.exp(self._rng.uniform(log_low, log_high))
            v = numpy.round(s)
            return int(min(max(v, param_distribution.low), param_distribution.high))
        elif isinstance(param_distribution, samples.CategoricalDistribution):
            choices = param_distribution.choices
            index = self._rng.randint(0, len(choices))
            return choices[index]
        else:
            raise NotImplementedError
