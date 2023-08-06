"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/30 4:29 下午
@Software: PyCharm
@File    : test_nop.py
@E-mail  : victor.xsyang@gmail.com
"""
import opts


def test_nop_stopper() -> None:

    experiment = opts.experiment.create_experiment()
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(1, 1)
    stopper = opts.stoppers.NopStopper()

    # A NopPruner instance is always deactivated.
    assert not stopper.stop(experiment=experiment, trial=experiment.trials[0])

