"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/25 1:41 下午
@Software: PyCharm
@File    : _state.py
@E-mail  : victor.xsyang@gmail.com
"""
import enum


class TrialState(enum.Enum):
    """State of a class `opts.trial.Trial`.

    """
    RUNNING = 0
    COMPLETE = 1
    STOP = 2
    FAIL = 3
    WAITING = 4

    def __repr__(self) -> str:
        return str(self)

    def is_finished(self) -> bool:
        return self != TrialState.RUNNING and self != TrialState.WAITING