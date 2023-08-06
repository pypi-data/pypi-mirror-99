"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/30 2:55 下午
@Software: PyCharm
@File    : test_percentile.py
@E-mail  : victor.xsyang@gmail.com
"""
import math
from typing import List
from typing import Tuple

import pytest

import opts
from opts.stoppers import _percentile
from opts.experiment import Experiment
from opts.experiment import ExperimentDirection
from opts.trial import TrialState


def test_percentile_stopper_percentile() -> None:

    opts.stoppers.PercentileStopper(0.0)
    opts.stoppers.PercentileStopper(25.0)
    opts.stoppers.PercentileStopper(100.0)

    with pytest.raises(ValueError):
        opts.stoppers.PercentileStopper(-0.1)

    with pytest.raises(ValueError):
        opts.stoppers.PercentileStopper(100.1)


def test_percentile_stopper_n_startup_trials() -> None:

    opts.stoppers.PercentileStopper(25.0, n_startup_trials=0)
    opts.stoppers.PercentileStopper(25.0, n_startup_trials=5)

    with pytest.raises(ValueError):
        opts.stoppers.PercentileStopper(25.0, n_startup_trials=-1)


def test_percentile_stopper_n_warmup_steps() -> None:

    opts.stoppers.PercentileStopper(25.0, n_warmup_steps=0)
    opts.stoppers.PercentileStopper(25.0, n_warmup_steps=5)

    with pytest.raises(ValueError):
        opts.stoppers.PercentileStopper(25.0, n_warmup_steps=-1)


def test_percentile_pruner_interval_steps() -> None:

    opts.stoppers.PercentileStopper(25.0, interval_steps=1)
    opts.stoppers.PercentileStopper(25.0, interval_steps=5)

    with pytest.raises(ValueError):
        opts.stoppers.PercentileStopper(25.0, interval_steps=-1)

    with pytest.raises(ValueError):
        opts.stoppers.PercentileStopper(25.0, interval_steps=0)


def test_percentile_stopper_with_one_trial() -> None:

    experiment = opts.experiment.create_experiment()
    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    trial.report(1, 1)
    stopper = opts.stoppers.PercentileStopper(25.0, 0, 0)

    # A pruner is not activated at a first trial.
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


@pytest.mark.parametrize(
    "direction_value", [("minimize", [1, 2, 3, 4, 5], 2.1), ("maximize", [1, 2, 3, 4, 5], 3.9)]
)
def test_25_percentile_stopper_intermediate_values(
    direction_value: Tuple[str, List[float], float]
) -> None:

    direction, intermediate_values, latest_value = direction_value
    stopper = opts.stoppers.PercentileStopper(25.0, 0, 0)
    experiment = opts.experiment.create_experiment(direction=direction)

    for v in intermediate_values:
        trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
        trial.report(v, 1)
        experiment._storage.set_trial_state(trial._trial_id, TrialState.COMPLETE)

    trial = opts.trial.Trial(experiment, experiment._storage.create_new_trial(experiment._experiment_id))
    # A pruner is not activated if a trial has no intermediate values.
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))

    trial.report(latest_value, 1)
    # A pruner is activated if a trial has an intermediate value.
    assert stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


def test_25_percentile_stopper_intermediate_values_nan() -> None:

    stopper = opts.stoppers.PercentileStopper(25.0, 0, 0)
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
    # A pruner is not activated if the 25 percentile intermediate value is NaN.
    assert not stopper.stop(experiment=experiment, trial=experiment._storage.get_trial(trial._trial_id))


@pytest.mark.parametrize(
    "direction_expected", [(ExperimentDirection.MINIMIZE, 0.1), (ExperimentDirection.MAXIMIZE, 0.2)]
)
def test_get_best_intermediate_result_over_steps(
    direction_expected: Tuple[ExperimentDirection, float]
) -> None:

    direction, expected = direction_expected

    if direction == ExperimentDirection.MINIMIZE:
        experiment = opts.experiment.create_experiment(direction="minimize")
    else:
        experiment = opts.experiment.create_experiment(direction="maximize")

    # FrozenTrial.intermediate_values has no elements.
    trial_id_empty = experiment._storage.create_new_trial(experiment._experiment_id)
    trial_empty = experiment._storage.get_trial(trial_id_empty)

    with pytest.raises(ValueError):
        _percentile._get_best_intermediate_result_over_steps(trial_empty, direction)

    # Input value has no NaNs but float values.
    trial_id_float = experiment._storage.create_new_trial(experiment._experiment_id)
    trial_float = opts.trial.Trial(experiment, trial_id_float)
    trial_float.report(0.1, step=0)
    trial_float.report(0.2, step=1)
    frozen_trial_float = experiment._storage.get_trial(trial_id_float)
    assert expected == _percentile._get_best_intermediate_result_over_steps(
        frozen_trial_float, direction
    )

    # Input value has a float value and a NaN.
    trial_id_float_nan = experiment._storage.create_new_trial(experiment._experiment_id)
    trial_float_nan = opts.trial.Trial(experiment, trial_id_float_nan)
    trial_float_nan.report(0.3, step=0)
    trial_float_nan.report(float("nan"), step=1)
    frozen_trial_float_nan = experiment._storage.get_trial(trial_id_float_nan)
    assert 0.3 == _percentile._get_best_intermediate_result_over_steps(
        frozen_trial_float_nan, direction
    )

    # Input value has a NaN only.
    trial_id_nan = experiment._storage.create_new_trial(experiment._experiment_id)
    trial_nan = opts.trial.Trial(experiment, trial_id_nan)
    trial_nan.report(float("nan"), step=0)
    frozen_trial_nan = experiment._storage.get_trial(trial_id_nan)
    assert math.isnan(
        _percentile._get_best_intermediate_result_over_steps(frozen_trial_nan, direction)
    )


def test_get_percentile_intermediate_result_over_trials() -> None:
    def setup_experiment(trial_num: int, _intermediate_values: List[List[float]]) -> Experiment:

        _experiment = opts.experiment.create_experiment(direction="minimize")
        trial_ids = [_experiment._storage.create_new_trial(_experiment._experiment_id) for _ in range(trial_num)]

        for step, values in enumerate(_intermediate_values):
            # Study does not have any trials.
            with pytest.raises(ValueError):
                _all_trials = _experiment._storage.get_all_trials(_experiment._experiment_id)
                _direction = _experiment._storage.get_experiment_direction(_experiment._experiment_id)
                _percentile._get_percentile_intermediate_result_over_trials(
                    _all_trials, _direction, step, 25
                )

            for i in range(trial_num):
                trial_id = trial_ids[i]
                value = values[i]
                _experiment._storage.set_trial_intermediate_value(trial_id, step, value)

        # Set trial states complete because this method ignores incomplete trials.
        for trial_id in trial_ids:
            _experiment._storage.set_trial_state(trial_id, TrialState.COMPLETE)

        return _experiment

    # Input value has no NaNs but float values (step=0).
    intermediate_values = [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]]
    experiment = setup_experiment(9, intermediate_values)
    all_trials = experiment._storage.get_all_trials(experiment._experiment_id)
    direction = experiment._storage.get_experiment_direction(experiment._experiment_id)
    assert 0.3 == _percentile._get_percentile_intermediate_result_over_trials(
        all_trials, direction, 0, 25.0
    )

    # Input value has a float value and NaNs (step=1).
    intermediate_values.append(
        [0.1, 0.2, 0.3, 0.4, 0.5, float("nan"), float("nan"), float("nan"), float("nan")]
    )
    experiment = setup_experiment(9, intermediate_values)
    all_trials = experiment._storage.get_all_trials(experiment._experiment_id)
    direction = experiment._storage.get_experiment_direction(experiment._experiment_id)
    assert 0.2 == _percentile._get_percentile_intermediate_result_over_trials(
        all_trials, direction, 1, 25.0
    )

    # Input value has NaNs only (step=2).
    intermediate_values.append(
        [
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
        ]
    )
    experiment = setup_experiment(9, intermediate_values)
    all_trials = experiment._storage.get_all_trials(experiment._experiment_id)
    direction = experiment._storage.get_experiment_direction(experiment._experiment_id)
    assert math.isnan(
        _percentile._get_percentile_intermediate_result_over_trials(all_trials, direction, 2, 75)
    )
