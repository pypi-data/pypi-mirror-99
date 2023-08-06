"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/25 4:51 下午
@Software: PyCharm
@File    : _experiment_direction.py
@E-mail  : victor.xsyang@gmail.com
"""
import enum


class ExperimentDirection(enum.Enum):
    """

    """
    NOT_SET = 0
    MINIMIZE = 1
    MAXIMIZE = 2