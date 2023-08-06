"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/30 9:14 下午
@Software: PyCharm
@File    : test_sucessive_halving.py
@E-mail  : victor.xsyang@gmail.com
"""
from typing import Tuple

import pytest

import opts


@pytest.mark.parametrize("direction_value", [("minimize", 2), ("maximize", 0.5)])
def test_successive_halving_stopper_intermediate_values(direction_value: Tuple[str, float]) -> None:

    direction, intermediate_value = direction_value
    stopper = opts.stoppers.SuccessiveHalvingStopper(
        min_resource=1, reduction_factor=2, min_early_stopping_rate=0
    )
    experiment = opts.experiment.create_experiment(direction=direction)

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(1, 1)

    # A pruner is not activated at a first trial.
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    # A pruner is not activated if a trial has no intermediate values.
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(intermediate_value, 1)
    # A pruner is activated if a trial has an intermediate value.
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


def test_successive_halving_stopper_rung_check() -> None:

    stopper = opts.stoppers.SuccessiveHalvingStopper(
        min_resource=1, reduction_factor=2, min_early_stopping_rate=0
    )
    experiment= opts.experiment.create_experiment()

    # Report 7 trials in advance.
    for i in range(7):
        trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
        trial.report(0.1 * (i + 1), step=7)
        stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    # Report a trial that has the 7-th value from bottom.
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(0.75, step=7)
    stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_0" in trial.system_attrs
    assert "completed_rung_1" not in trial.system_attrs

    # Report a trial that has the third value from bottom.
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(0.25, step=7)
    stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_1" in trial.system_attrs
    assert "completed_rung_2" not in trial.system_attrs

    # Report a trial that has the lowest value.
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(0.05, step=7)
    stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_2" in trial.system_attrs
    assert "completed_rung_3" not in trial.system_attrs


def test_successive_halving_stopper_first_trial_is_not_stopped() -> None:

    stopper = opts.stoppers.SuccessiveHalvingStopper(
        min_resource=1, reduction_factor=2, min_early_stopping_rate=0
    )
    experiment= opts.experiment.create_experiment()

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    for i in range(10):
        trial.report(1, step=i)

        # The first trial is not pruned.
        assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    # The trial completed until rung 3.
    assert "completed_rung_0" in trial.system_attrs
    assert "completed_rung_1" in trial.system_attrs
    assert "completed_rung_2" in trial.system_attrs
    assert "completed_rung_3" in trial.system_attrs
    assert "completed_rung_4" not in trial.system_attrs


def test_successive_halving_stopper_with_nan() -> None:

    stopper = opts.stoppers.SuccessiveHalvingStopper(
        min_resource=2, reduction_factor=2, min_early_stopping_rate=0
    )
    experiment = opts.experiment.create_experiment()

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))

    # A pruner is not activated if the step is not a rung completion point.
    trial.report(float("nan"), step=1)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    # A pruner is activated if the step is a rung completion point and
    # the intermediate value is NaN.
    trial.report(float("nan"), step=2)
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


@pytest.mark.parametrize("n_reports", range(3))
@pytest.mark.parametrize("n_trials", [1, 2])
def test_successive_halving_stopper_with_auto_min_resource(n_reports: int, n_trials: int) -> None:

    stopper = opts.stoppers.SuccessiveHalvingStopper(min_resource="auto")
    experiment = opts.experiment.create_experiment(sampler=opts.samplers.RandomSampler(), stopper=stopper)

    assert stopper._min_resource is None

    def objective(trial: opts.trial.Trial) -> float:

        for i in range(n_reports):
            trial.report(1.0 / (i + 1), i)
            if trial.should_stop():
                raise opts.TrialStop()
        return 1.0

    experiment.optimize(objective, n_trials=n_trials)
    if n_reports > 0 and n_trials > 1:
        assert stopper._min_resource is not None and stopper._min_resource > 0
    else:
        assert stopper._min_resource is None


def test_successive_halving_stopper_with_invalid_str_to_min_resource() -> None:

    with pytest.raises(ValueError):
        opts.stoppers.SuccessiveHalvingStopper(min_resource="fixed")


def test_successive_halving_stopper_min_resource_parameter() -> None:

    experiment = opts.experiment.create_experiment()

    # min_resource=0: Error (must be `min_resource >= 1`).
    with pytest.raises(ValueError):
        opts.stoppers.SuccessiveHalvingStopper(
            min_resource=0, reduction_factor=2, min_early_stopping_rate=0
        )

    # min_resource=1: The rung 0 ends at step 1.
    stopper = opts.stoppers.SuccessiveHalvingStopper(
        min_resource=1, reduction_factor=2, min_early_stopping_rate=0
    )
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))

    trial.report(1, step=1)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_0" in trial.system_attrs
    assert "completed_rung_1" not in trial.system_attrs

    # min_resource=2: The rung 0 ends at step 2.
    stopper = opts.stoppers.SuccessiveHalvingStopper(
        min_resource=2, reduction_factor=2, min_early_stopping_rate=0
    )
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))

    trial.report(1, step=1)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_0" not in trial.system_attrs

    trial.report(1, step=2)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_0" in trial.system_attrs
    assert "completed_rung_1" not in trial.system_attrs


def test_successive_halving_stopper_reduction_factor_parameter() -> None:

    experiment = opts.experiment.create_experiment()

    # reduction_factor=1: Error (must be `reduction_factor >= 2`).
    with pytest.raises(ValueError):
        opts.stoppers.SuccessiveHalvingStopper(
            min_resource=1, reduction_factor=1, min_early_stopping_rate=0
        )

    # reduction_factor=2: The rung 0 ends at step 1.
    stopper = opts.stoppers.SuccessiveHalvingStopper(
        min_resource=1, reduction_factor=2, min_early_stopping_rate=0
    )
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))

    trial.report(1, step=1)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_0" in trial.system_attrs
    assert "completed_rung_1" not in trial.system_attrs

    # reduction_factor=3: The rung 1 ends at step 3.
    stopper = opts.stoppers.SuccessiveHalvingStopper(
        min_resource=1, reduction_factor=3, min_early_stopping_rate=0
    )
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))

    trial.report(1, step=1)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_0" in trial.system_attrs
    assert "completed_rung_1" not in trial.system_attrs

    trial.report(1, step=2)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_1" not in trial.system_attrs

    trial.report(1, step=3)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_1" in trial.system_attrs
    assert "completed_rung_2" not in trial.system_attrs


def test_successive_halving_stopper_min_early_stopping_rate_parameter() -> None:

    experiment = opts.experiment.create_experiment()

    # min_early_stopping_rate=-1: Error (must be `min_early_stopping_rate >= 0`).
    with pytest.raises(ValueError):
        opts.stoppers.SuccessiveHalvingStopper(
            min_resource=1, reduction_factor=2, min_early_stopping_rate=-1
        )

    # min_early_stopping_rate=0: The rung 0 ends at step 1.
    stopper = opts.stoppers.SuccessiveHalvingStopper(
        min_resource=1, reduction_factor=2, min_early_stopping_rate=0
    )
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))

    trial.report(1, step=1)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_0" in trial.system_attrs

    # min_early_stopping_rate=1: The rung 0 ends at step 2.
    stopper = opts.stoppers.SuccessiveHalvingStopper(
        min_resource=1, reduction_factor=2, min_early_stopping_rate=1
    )
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))

    trial.report(1, step=1)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_0" not in trial.system_attrs
    assert "completed_rung_1" not in trial.system_attrs

    trial.report(1, step=2)
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    assert "completed_rung_0" in trial.system_attrs
    assert "completed_rung_1" not in trial.system_attrs
