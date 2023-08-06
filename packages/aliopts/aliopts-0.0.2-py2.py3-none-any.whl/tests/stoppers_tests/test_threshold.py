"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/30 2:37 下午
@Software: PyCharm
@File    : test_threshold.py
@E-mail  : victor.xsyang@gmail.com
"""
import pytest

import opts


def test_threshold_stopper_with_ub() -> None:

    experiment = opts.experiment.create_experiment()
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    stopper = opts.stoppers.ThresholdStopper(upper=2.0, n_warmup_steps=0, interval_steps=1)

    trial.report(1.0, 1)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(3.0, 2)
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


def test_threshold_stopper_with_lt() -> None:

    experiment = opts.experiment.create_experiment()
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    stopper = opts.stoppers.ThresholdStopper(lower=2.0, n_warmup_steps=0, interval_steps=1)

    trial.report(3.0, 1)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(1.0, 2)
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


def test_threshold_stop_with_two_side() -> None:

    experiment = opts.experiment.create_experiment()
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    stopper = opts.stoppers.ThresholdStopper(
        lower=0.0, upper=1.0, n_warmup_steps=0, interval_steps=1
    )

    trial.report(-0.1, 1)
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(0.0, 2)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(0.4, 3)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(1.0, 4)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(1.1, 5)
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


def test_threshold_stopper_with_invalid_inputs() -> None:

    with pytest.raises(TypeError):
        opts.stoppers.ThresholdStopper(lower="val", upper=1.0)  # type: ignore

    with pytest.raises(TypeError):
        opts.stoppers.ThresholdStopper(lower=0.0, upper="val")  # type: ignore

    with pytest.raises(TypeError):
        opts.stoppers.ThresholdStopper(lower=None, upper=None)


def test_threshold_stopper_with_nan() -> None:

    experiment = opts.experiment.create_experiment()
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    stopper = opts.stoppers.ThresholdStopper(
        lower=0.0, upper=1.0, n_warmup_steps=0, interval_steps=1
    )

    trial.report(float("nan"), 1)
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


def test_threshold_stopper_n_warmup_steps() -> None:
    experiment = opts.experiment.create_experiment()
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    stopper = opts.stoppers.ThresholdStopper(lower=0.0, upper=1.0, n_warmup_steps=2)

    trial.report(-10.0, 0)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(100.0, 1)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(-100.0, 3)
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(1.0, 4)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(1000.0, 5)
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


def test_threshold_stopper_interval_steps() -> None:
    experiment = opts.experiment.create_experiment()
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    stopper = opts.stoppers.ThresholdStopper(lower=0.0, upper=1.0, interval_steps=2)

    trial.report(-10.0, 0)
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(100.0, 1)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(-100.0, 2)
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(10.0, 3)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(1000.0, 4)
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
