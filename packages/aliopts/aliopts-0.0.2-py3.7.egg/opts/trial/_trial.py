"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/25 4:17 下午
@Software: PyCharm
@File    : _trial.py
@E-mail  : victor.xsyang@gmail.com
"""
import copy
import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Sequence
from typing import Union
import warnings

import opts
from opts import samples
from opts import logger
from opts import stoppers
from opts.samples import BaseDistribution
from opts.samples import CategoricalChoiceType
from opts.samples import CategoricalDistribution
from opts.samples import DiscreteUniformDistribution
from opts.samples import IntLogUniformDistribution
from opts.samples import IntUniformDistribution
from opts.samples import LogUniformDistribution
from opts.samples import UniformDistribution
from opts.trial._base import BaseTrial

_logger = logger.get_logger(__name__)


class Trial(BaseTrial):
    """A trial is a process evaluating an objective function.

    """

    def __init__(self, experiment: "opts.experiment.Experiment", trial_id: int) -> None:
        self.experiment = experiment
        self._trial_id = trial_id

        self._experiment_id = self.experiment._experiment_id
        self.storage = self.experiment._storage
        self._init_relative_params()

    def _init_relative_params(self) -> None:
        trial = self.storage.get_trial(self._trial_id)
        experiment = stoppers._filter_experiment(self.experiment, trial)

        self.relative_search_space = self.experiment.sampler.infer_relative_search_space(experiment, trial)
        self.relative_params = self.experiment.sampler.sample_relative(
            experiment, trial, self.relative_search_space
        )

    def suggest_float(self,
                      name: str,
                      low: float,
                      high: float,
                      *,
                      step: Optional[float] = None,
                      log: bool = False
                      ) -> float:
        """Suggest a value for the floating pointing parameter.

        :param name:
        :param low:
        :param high:
        :param step:
        :param log:
        :return:
        """
        if step is not None:
            if log:
                raise ValueError("The parameter `step` is not supported when `log` is True")
            else:
                return self.suggest_discrete_uniform(name, low, high, step)
        else:
            if log:
                return self.suggest_loguniform(name, low, high)
            else:
                return self.suggest_uniform(name, low, high)

    def suggest_uniform(self, name: str, low: float, high: float) -> float:
        """Suggest a value for the continuous parameter.

        :param name:
        :param low:
        :param high:
        :return:
        """
        distribution = UniformDistribution(low=low, high=high)
        self._check_distribution(name, distribution)
        return self._suggest(name, distribution)

    def suggest_loguniform(self, name: str, low: float, high: float) -> float:
        """Suggest a value for the continuous parameter.

        :param name:
        :param low:
        :param high:
        :return:
        """
        distribution = LogUniformDistribution(low=low, high=high)
        self._check_distribution(name, distribution)
        return self._suggest(name, distribution)

    def suggest_discrete_uniform(self, name: str, low: float, high: float, q: float) -> float:
        """Suggest a value for the discrete parameter.

        :param name:
        :param low:
        :param high:
        :param q:
        :return:
        """
        distribution = DiscreteUniformDistribution(low=low, high=high, q=q)
        self._check_distribution(name, distribution)
        return self._suggest(name, distribution)

    def suggest_int(self, name: str, low: int, high: int, step: int = 1, log: bool = False) -> int:
        """Suggest a value for the parameter.

        :param name:
        :param low:
        :param high:
        :param step:
        :param log:
        :return:
        """
        if step != 1:
            if log:
                raise ValueError(
                    "The parameter `step != 1` is not supported when `log` is True."
                    "The specified `step` is {}.".format(step)
                )
            else:
                distribution: Union[
                    IntUniformDistribution, IntLogUniformDistribution
                ] = IntUniformDistribution(low=low, high=high, step=step)
        else:
            if log:
                distribution = IntLogUniformDistribution(low=low, high=high)
            else:
                distribution = IntUniformDistribution(low=low, high=high, step=step)

        self._check_distribution(name, distribution)
        return int(self._suggest(name, distribution))

    def suggest_categorical(
            self, name: str, choices: Sequence[CategoricalChoiceType]
    ) -> CategoricalChoiceType:
        return self._suggest(name, CategoricalDistribution(choices=choices))

    def _suggest(self, name: str, distribution: BaseDistribution) -> Any:

        storage = self.storage
        trial_id = self._trial_id

        trial = storage.get_trial(trial_id)

        if name in trial.distributions:
            # No need to sample if already suggested.
            samples.check_distribution_compatibility(trial.distributions[name], distribution)
            param_value = distribution.to_external_repr(storage.get_trial_param(trial_id, name))
        else:
            if self._is_fixed_param(name, distribution):
                param_value = storage.get_trial_system_attrs(trial_id)["fixed_params"][name]
            elif distribution.single():
                param_value = samples._get_single_value(distribution)
            elif self._is_relative_param(name, distribution):
                param_value = self.relative_params[name]
            else:
                experiment = stoppers._filter_experiment(self.experiment, trial)
                param_value = self.experiment.sampler.sample_independent(
                    experiment, trial, name, distribution
                )

            param_value_in_internal_repr = distribution.to_internal_repr(param_value)
            storage.set_trial_param(trial_id, name, param_value_in_internal_repr, distribution)

        return param_value

    def report(self, value: float, step: int) -> None:
        """Report an objective function value for a given step.

        """

        try:
            # For convenience, we allow users to report a value that can be cast to `float`.
            value = float(value)
        except (TypeError, ValueError):
            message = "The `value` argument is of type '{}' but supposed to be a float.".format(
                type(value).__name__
            )
            raise TypeError(message) from None

        if step < 0:
            raise ValueError("The `step` argument is {} but cannot be negative.".format(step))

        intermediate_values = self.storage.get_trial(self._trial_id).intermediate_values

        if step in intermediate_values:
            # Do nothing if already reported.
            return

        self.storage.set_trial_intermediate_value(self._trial_id, step, value)

    def set_system_attr(self, key: str, value: Any) -> None:
        """Set system attributes to the trial.

        Args:
            key:
                A key string of the attribute.
            value:
                A value of the attribute. The value should be JSON serializable.
        """

        self.storage.set_trial_system_attr(self._trial_id, key, value)

    def set_user_attr(self, key: str, value: Any) -> None:
        """Set user attributes to the trial.
        Args:
            key:
                A key string of the attribute.
            value:
                A value of the attribute. The value should be JSON serializable.
        """

        self.storage.set_trial_user_attr(self._trial_id, key, value)

    def should_stop(self) -> bool:
        trial = self.experiment._storage.get_trial(self._trial_id)
        return self.experiment.stopper.stop(self.experiment, trial)

    def _check_distribution(self, name: str, distribution: BaseDistribution) -> None:
        old_distribution = self.storage.get_trial(self._trial_id).distributions.get(
            name, distribution
        )
        if old_distribution != distribution:
            warnings.warn(
                'Inconsistent parameter values for distribution with name "{}"! '
                "This might be a configuration mistake. "
                "Opts allows to call the same distribution with the same "
                "name more then once in a trial. "
                "When the parameter values are inconsistent opts only "
                "uses the values of the first call and ignores all following. "
                "Using these values: {}".format(name, old_distribution._asdict()),
                RuntimeWarning
            )

    def _is_fixed_param(self, name: str, distribution: BaseDistribution) -> bool:

        system_attrs = self.storage.get_trial_system_attrs(self._trial_id)
        if "fixed_params" not in system_attrs:
            return False

        if name not in system_attrs["fixed_params"]:
            return False

        param_value = system_attrs["fixed_params"][name]
        param_value_in_internal_repr = distribution.to_internal_repr(param_value)

        contained = distribution._contains(param_value_in_internal_repr)
        if not contained:
            warnings.warn(
                "Fixed parameter '{}' with value {} is out of range "
                "for distribution {}.".format(name, param_value, distribution)
            )
        return contained

    def _is_relative_param(self, name: str, distribution: BaseDistribution) -> bool:

        if name not in self.relative_params:
            return False

        if name not in self.relative_search_space:
            raise ValueError(
                "The parameter '{}' was sampled by `sample_relative` method "
                "but it is not contained in the relative search space.".format(name)
            )

        relative_distribution = self.relative_search_space[name]
        samples.check_distribution_compatibility(relative_distribution, distribution)

        param_value = self.relative_params[name]
        param_value_in_internal_repr = distribution.to_internal_repr(param_value)
        return distribution._contains(param_value_in_internal_repr)


    @property
    def params(self) -> Dict[str, Any]:
        """Return parameters to be optimized

        :return:
        """
        return copy.deepcopy(self.storage.get_trial_params(self._trial_id))

    @property
    def datetime_start(self) -> Optional[datetime.datetime]:
        return self.storage.get_trial(self._trial_id).datetime_start

    @property
    def distributions(self) -> Dict[str, BaseDistribution]:
        """Return distributions of parameters to be optimized.

        Returns:
            A dictionary containing all distributions.
        """

        return copy.deepcopy(self.storage.get_trial(self._trial_id).distributions)

    @property
    def user_attrs(self) -> Dict[str, Any]:
        """Return user attributes.

        Returns:
            A dictionary containing all user attributes.
        """

        return copy.deepcopy(self.storage.get_trial_user_attrs(self._trial_id))

    @property
    def system_attrs(self) -> Dict[str, Any]:
        """Return system attributes.

        Returns:
            A dictionary containing all system attributes.
        """

        return copy.deepcopy(self.storage.get_trial_system_attrs(self._trial_id))

    @property
    def number(self) -> int:
        """Return trial's number which is consecutive and unique in a study.

        Returns:
            A trial number.
        """

        return self.storage.get_trial_number_from_id(self._trial_id)
