"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/24 9:35 下午
@Software: PyCharm
@File    : _fixed.py
@E-mail  : victor.xsyang@gmail.com
"""
import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Sequence
from typing import Union

from opts import samples
from opts.samples import BaseDistribution
from opts.samples import CategoricalChoiceType
from opts.samples import CategoricalDistribution
from opts.samples import DiscreteUniformDistribution
from opts.samples import IntLogUniformDistribution
from opts.samples import IntUniformDistribution
from opts.samples import LogUniformDistribution
from opts.samples import UniformDistribution
from opts.trial._base import BaseTrial


class FixedTrial(BaseTrial):
    """A trial class which suggests a fixed value for each parameter.

    """
    def __init__(self, params: Dict[str, Any], number: int = 0) -> None:
        self._params = params
        self._suggested_params: Dict[str, Any] = {}
        self._distributions: Dict[str, BaseDistribution] = {}
        self._user_attrs: Dict[str, Any] = {}
        self._system_attrs: Dict[str, Any] = {}
        self._datetime_start = datetime.datetime.now()
        self._number = number

    def suggest_float(self,
                      name: str,
                      low: float,
                      high: float,
                      *,
                      step: Optional[float] = None,
                      log: bool = False
                      ) -> float:
        if step is not None:
            if log:
                raise ValueError("The parameter `step` is not supported when `log` is True.")
            else:
                return self._suggest(name, DiscreteUniformDistribution(low=low, high=high, q=step))

        else:
            if log:
                return self._suggest(name, LogUniformDistribution(low=low, high=high))
            else:
                return self._suggest(name, UniformDistribution(low=low, high=high))

    def suggest_uniform(self, name: str, low: float, high: float) -> float:
        return self._suggest(name, UniformDistribution(low=low, high=high))

    def suggest_loguniform(self, name: str, low: float, high: float) -> float:

        return self._suggest(name, LogUniformDistribution(low=low, high=high))

    def suggest_discrete_uniform(self, name: str, low: float, high: float, q: float) -> float:
        discrete = DiscreteUniformDistribution(low=low, high=high, q=q)
        return self._suggest(name, discrete)

    def suggest_int(self, name: str, low: int, high: int, step: int = 1, log: bool = False) -> int:
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
        return int(self._suggest(name, distribution))

    def suggest_categorical(
        self, name: str, choices: Sequence[CategoricalChoiceType]
    ) -> CategoricalChoiceType:

        return self._suggest(name, CategoricalDistribution(choices=choices))

    def report(self, value: float, step: int) -> None:

        pass

    def should_stop(self) -> bool:

        return False

    def set_user_attr(self, key: str, value: Any) -> None:
        self._user_attrs[key] = value

    def set_system_attr(self, key: str, value: Any) -> None:
        self._system_attrs[key] = value

    def _suggest(self, name: str, distribution: BaseDistribution) -> Any:
        if name not in self._params:
            raise ValueError(
                "The value of the parameter '{}' is not found. Please set it at "
                "the construction of the FixedTrial object.".format(name)
            )
        value = self._params[name]
        param_value_in_internal_repr = distribution.to_internal_repr(value)
        if not distribution._contains(param_value_in_internal_repr):
            raise ValueError(
                "The value {} of the parameter '{}' is out of "
                "the range of the distribution {}.".format(value, name, distribution)
            )

        if name in self._distributions:
            samples.check_distribution_compatibility(self._distributions[name], distribution)

        self._suggested_params[name] = value
        self._distributions[name] = distribution

        return value

    @property
    def params(self) -> Dict[str, Any]:

        return self._suggested_params

    @property
    def distributions(self) -> Dict[str, BaseDistribution]:

        return self._distributions

    @property
    def user_attrs(self) -> Dict[str, Any]:

        return self._user_attrs

    @property
    def system_attrs(self) -> Dict[str, Any]:

        return self._system_attrs

    @property
    def datetime_start(self) -> Optional[datetime.datetime]:

        return self._datetime_start

    @property
    def number(self) -> int:

        return self._number

