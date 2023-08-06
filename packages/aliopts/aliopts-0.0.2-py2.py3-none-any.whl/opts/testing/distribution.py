"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/26 4:19 下午
@Software: PyCharm
@File    : distribution.py
@E-mail  : victor.xsyang@gmail.com
"""
from typing import Dict

from opts.samples import BaseDistribution


class UnsupportedDistribution(BaseDistribution):
    def single(self) -> bool:

        return False

    def _contains(self, param_value_in_internal_repr: float) -> bool:

        return True

    def _asdict(self) -> Dict:

        return {}
