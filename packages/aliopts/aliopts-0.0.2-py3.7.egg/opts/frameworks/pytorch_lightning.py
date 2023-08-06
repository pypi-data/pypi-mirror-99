"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/17 3:47 下午
@Software: PyCharm
@File    : pytorch_lightning.py
@E-mail  : victor.xsyang@gmail.com
"""
import opts
from opts._imports import try_import

with try_import() as _imports:
    from pytorch_lightning import LightningModule
    from pytorch_lightning import Trainer
    from pytorch_lightning.callbacks import EarlyStopping

if not _imports.is_successful():
    EarlyStopping = object
    LightningModule = object
    Trainer = object


class PytorchLightningStoppingCallback(EarlyStopping):
    """PyTorch Lightning callback to stop unpromising trials.

    """
    def __init__(self, trial: opts.trial.Trial, monitor: str) -> None:
        _imports.check()
        super(PytorchLightningStoppingCallback, self).__init__(monitor=monitor)

        self._trial = trial

    def on_validation_end(self, trainer: Trainer, pl_module: LightningModule) -> None:
        logs = trainer.callback_metrics
        epoch = pl_module.current_epoch
        current_score = logs.get(self.monitor)
        if current_score is None:
            return

        self._trial.report(current_score, step=epoch)
        if self._trial.should_stop():
            message = "Trial was stopped at epoch {}.".format(epoch)
            raise opts.TrialStop(message)
