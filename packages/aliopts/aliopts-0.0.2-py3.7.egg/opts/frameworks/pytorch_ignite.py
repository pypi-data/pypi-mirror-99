"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/17 3:11 下午
@Software: PyCharm
@File    : pytorch_ignite.py
@E-mail  : victor.xsyang@gmail.com
"""
import opts
from opts.trial import Trial
from opts._imports import try_import

with try_import() as _imports:
    from ignite.engine import Engine


class PytorchIgniteStoppinghandler(object):
    """Pytorch Ignite handler to stop unpromising trials

    """
    def __init__(self, trial: Trial, metric: str, trainer: Engine) -> None:
        _imports.check()
        self._trial = trial
        self._metric = metric
        self._trainer = trainer

    def __call__(self, engine: Engine) -> None:
        score = engine.state.metrics[self._metric]
        self._trial.report(score, self._trainer.state.epoch)
        if self._trial.should_stop():
            message = "Trial was stopped at {} epoch.".format(self._trainer.state.epoch)
            raise opts.TrialStop(message)