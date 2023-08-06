"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/26 4:24 下午
@Software: PyCharm
@File    : sampler.py
@E-mail  : victor.xsyang@gmail.com
"""
from typing import Any
from typing import Dict

import opts
from opts import samples
from opts.samples import BaseDistribution


class DeterministicRelativeSampler(opts.samplers.BaseSampler):
    def __init__(
        self, relative_search_space: Dict[str, BaseDistribution], relative_params: Dict[str, Any]
    ) -> None:

        self.relative_search_space = relative_search_space
        self.relative_params = relative_params

    def infer_relative_search_space(
        self, experiment: "opts.experiment.Experiment", trial: "opts.trial.FrozenTrial"
    ) -> Dict[str, BaseDistribution]:

        return self.relative_search_space

    def sample_relative(
        self,
        experiment: "opts.experiment.Experiment",
        trial: "opts.trial.FrozenTrial",
        search_space: Dict[str, BaseDistribution],
    ) -> Dict[str, Any]:

        return self.relative_params

    def sample_independent(
        self,
        experiment: "opts.experiment.Experiment",
        trial: "opts.trial.FrozenTrial",
        param_name: str,
        param_distribution: BaseDistribution,
    ) -> Any:

        if isinstance(param_distribution, samples.UniformDistribution):
            param_value: Any = param_distribution.low
        elif isinstance(param_distribution, samples.LogUniformDistribution):
            param_value = param_distribution.low
        elif isinstance(param_distribution, samples.DiscreteUniformDistribution):
            param_value = param_distribution.low
        elif isinstance(param_distribution, samples.IntUniformDistribution):
            param_value = param_distribution.low
        elif isinstance(param_distribution, samples.CategoricalDistribution):
            param_value = param_distribution.choices[0]
        else:
            raise NotImplementedError

        return param_value


class FirstTrialOnlyRandomSampler(opts.samplers.RandomSampler):
    def sample_relative(
        self,
        experiment: "opts.experiment.Experiment",
        trial: "opts.trial.FrozenTrial",
        search_space: Dict[str, BaseDistribution],
    ) -> Dict[str, float]:

        if len(experiment.trials) > 1:
            raise RuntimeError("`FirstTrialOnlyRandomSampler` only works on the first trial.")

        return super(FirstTrialOnlyRandomSampler, self).sample_relative(experiment, trial, search_space)

    def sample_independent(
        self,
        experiment: "opts.experiment.Experiment",
        trial: "opts.trial.FrozenTrial",
        param_name: str,
        param_distribution: BaseDistribution,
    ) -> float:

        if len(experiment.trials) > 1:
            raise RuntimeError("`FirstTrialOnlyRandomSampler` only works on the first trial.")

        return super(FirstTrialOnlyRandomSampler, self).sample_independent(
            experiment, trial, param_name, param_distribution
        )
