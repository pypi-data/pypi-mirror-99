"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/14 9:07 下午
@Software: PyCharm
@File    : _partial_fixed.py
@E-mail  : victor.xsyang@gmail.com
"""
from typing import Any
from typing import Dict
import warnings

from opts._experimental import experimental
from opts.samples import BaseDistribution
from opts.samplers import BaseSampler
from opts.experiment import Experiment
from opts.trial import FrozenTrial


@experimental("2.4.0")
class PartialFixedSampler(BaseSampler):
    """Sampler with partially fixed parameters.

    """

    def __init__(self, fixed_params: Dict[str, Any], base_sampler: BaseSampler) -> None:
        self._fixed_params = fixed_params
        self._base_sampler = base_sampler

    def reseed_rng(self) -> None:
        self._base_sampler.reseed_rng()

    def infer_relative_search_space(
            self, experiment: Experiment,
            trial: FrozenTrial) -> Dict[str, BaseDistribution]:
        search_space = self._base_sampler.infer_relative_search_space(experiment, trial)
        for param_name in self._fixed_params.keys():
            if param_name in search_space:
                del search_space[param_name]
        return search_space

    def sample_relative(
            self, experiment: Experiment, trial: FrozenTrial,
            search_space: Dict[str, BaseDistribution]
    ) -> Dict[str, Any]:
        return self._base_sampler.sample_relative(experiment, trial, search_space)

    def sample_independent(
            self,
            experiment: Experiment,
            trial: FrozenTrial,
            param_name: str,
            param_distribution: BaseDistribution
    ) -> Any:
        param_value = self._fixed_params.get(param_name)
        if param_value is None:
            return self._base_sampler.sample_independent(
                experiment, trial, param_name, param_distribution
            )
        else:
            param_value_in_internal_repr = param_distribution.to_internal_repr(param_value)
            contained = param_distribution._contains(param_value_in_internal_repr)

            if not contained:
                warnings.warn(
                    f"Fixed parameter '{param_name}' with value {param_value} is out of range "
                    f"for distribution {param_distribution}."
                )
            return param_value
