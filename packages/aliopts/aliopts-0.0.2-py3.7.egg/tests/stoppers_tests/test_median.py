"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/30 3:35 下午
@Software: PyCharm
@File    : test_median.py
@E-mail  : victor.xsyang@gmail.com
"""
from typing import List
from typing import Tuple

import pytest

import opts
from opts.trial import TrialState


def test_median_stopper_with_one_trial() -> None:

    experiment= opts.experiment.create_experiment()
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(1, 1)
    stopper = opts.stoppers.MedianStopper(0, 0)

    # A pruner is not activated at a first trial.
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


@pytest.mark.parametrize("direction_value", [("minimize", 2), ("maximize", 0.5)])
def test_median_stopper_intermediate_values(direction_value: Tuple[str, float]) -> None:

    direction, intermediate_value = direction_value
    stopper = opts.stoppers.MedianStopper(0, 0)
    experiment = opts.experiment.create_experiment(direction=direction)

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(1, 1)
    experiment._storage.set_trial_state(trial._trial_id, TrialState.COMPLETE)

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    # A pruner is not activated if a trial has no intermediate values.
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(intermediate_value, 1)
    # A pruner is activated if a trial has an intermediate value.
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


def test_median_stopper_intermediate_values_nan() -> None:

    stopper = opts.stoppers.MedianStopper(0, 0)
    experiment = opts.experiment.create_experiment()

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(float("nan"), 1)
    # A pruner is not activated if the study does not have any previous trials.
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    experiment._storage.set_trial_state(trial._trial_id, TrialState.COMPLETE)

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(float("nan"), 1)
    # A pruner is activated if the best intermediate value of this trial is NaN.
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    experiment._storage.set_trial_state(trial._trial_id, TrialState.COMPLETE)

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(1, 1)
    # A pruner is not activated if the median intermediate value is NaN.
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


def test_median_stopper_n_startup_trials() -> None:

    stopper = opts.stoppers.MedianStopper(2, 0)
    experiment= opts.experiment.create_experiment()

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(1, 1)
    experiment._storage.set_trial_state(trial._trial_id, TrialState.COMPLETE)

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(2, 1)
    # A pruner is not activated during startup trials.
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))
    experiment._storage.set_trial_state(trial._trial_id, TrialState.COMPLETE)

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(3, 1)
    # A pruner is activated after startup trials.
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


def test_median_stopper_n_warmup_steps() -> None:

    stopper = opts.stoppers.MedianStopper(0, 1)
    experiment = opts.experiment.create_experiment()

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(1, 0)
    trial.report(1, 1)
    experiment._storage.set_trial_state(trial._trial_id, TrialState.COMPLETE)

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(2, 0)
    # A pruner is not activated during warm-up steps.
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(2, 1)
    # A pruner is activated after warm-up steps.
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


@pytest.mark.parametrize(
    "n_warmup_steps,interval_steps,report_steps,expected_stop_steps",
    [
        (1, 2, 1, [1, 3]),
        (0, 3, 10, list(range(29))),
        (2, 3, 10, list(range(10, 29))),
        (0, 10, 3, [0, 1, 2, 12, 13, 14, 21, 22, 23]),
        (2, 10, 3, [3, 4, 5, 12, 13, 14, 24, 25, 26]),
    ],
)
def test_median_stopper_interval_steps(
    n_warmup_steps: int, interval_steps: int, report_steps: int, expected_stop_steps: List[int]
) -> None:

    stopper = opts.stoppers.MedianStopper(0, n_warmup_steps, interval_steps)
    experiment = opts.experiment.create_experiment()

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    n_steps = max(expected_stop_steps)
    base_index = 0
    for i in range(base_index, base_index + n_steps):
        trial.report(base_index, i)
    experiment._storage.set_trial_state(trial._trial_id, TrialState.COMPLETE)

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    for i in range(base_index, base_index + n_steps):
        if (i - base_index) % report_steps == 0:
            trial.report(2, i)
        assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id)) == (
            i >= n_warmup_steps and i in expected_stop_steps
        )
