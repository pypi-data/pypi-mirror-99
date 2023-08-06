"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/24 9:33 下午
@Software: PyCharm
@File    : _base.py
@E-mail  : victor.xsyang@gmail.com
"""
import abc
import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Sequence

from opts.samples import BaseDistribution
from opts.samples import CategoricalChoiceType


class BaseTrial(object, metaclass=abc.ABCMeta):
    """Base class for trials

    """
    @abc.abstractmethod
    def suggest_float(self,
                      name: str,
                      low: float,
                      high: float,
                      *,
                      step: Optional[float] = None,
                      log: bool = False
                      ) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def suggest_uniform(self, name: str, low: float, high: float) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def suggest_loguniform(self, name: str, low: float, high: float) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def suggest_discrete_uniform(self, name: str, low: float, high: float, q: float) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def suggest_int(self, name: str, low: int, high: int, step: int = 1, log: bool = False) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def suggest_categorical(
            self, name: str, choices: Sequence[CategoricalChoiceType]
    ) -> CategoricalChoiceType:
        raise NotImplementedError

    @abc.abstractmethod
    def report(self, value: float, step: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def should_stop(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def set_user_attr(self, key: str, value: Any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def set_system_attr(self, key: str, value: Any) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def params(self) -> Dict[str, Any]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def distributions(self) -> Dict[str, BaseDistribution]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def user_attrs(self) -> Dict[str, Any]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def system_attrs(self) -> Dict[str, Any]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def datetime_start(self) -> Optional[datetime.datetime]:
        raise NotImplementedError

    @property
    def number(self) -> int:
        raise NotImplementedError
