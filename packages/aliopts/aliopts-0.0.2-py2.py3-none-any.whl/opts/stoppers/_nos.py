"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/26 8:42 下午
@Software: PyCharm
@File    : _nos.py
@E-mail  : victor.xsyang@gmail.com
"""
import opts
from opts.stoppers import BaseStopper


class NopStopper(BaseStopper):
    """Stop which never stoppers trials.

    """
    def stop(self, experiment: "opts.experiment.Experiment", trial: "opts.trial.FrozenTrial") -> bool:
        return False