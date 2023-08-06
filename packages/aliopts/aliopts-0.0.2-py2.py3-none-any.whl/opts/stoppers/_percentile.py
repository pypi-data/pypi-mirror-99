"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/25 5:40 下午
@Software: PyCharm
@File    : _percentile.py
@E-mail  : victor.xsyang@gmail.com
"""
import functools
import math
from typing import KeysView
from typing import List

import numpy as np

import opts
from opts._experiment_direction import ExperimentDirection
from opts.stoppers import BaseStopper
from opts.trial._state import TrialState


def _get_best_intermediate_result_over_steps(
    trial: "opts.trial.FrozenTrial", direction: ExperimentDirection
) -> float:

    values = np.array(list(trial.intermediate_values.values()), np.float)
    if direction == ExperimentDirection.MAXIMIZE:
        return np.nanmax(values)
    return np.nanmin(values)


def _get_percentile_intermediate_result_over_trials(
    all_trials: List["opts.trial.FrozenTrial"],
    direction: ExperimentDirection,
    step: int,
    percentile: float,
) -> float:

    completed_trials = [t for t in all_trials if t.state == TrialState.COMPLETE]

    if len(completed_trials) == 0:
        raise ValueError("No trials have been completed.")

    intermediate_values = [
        t.intermediate_values[step] for t in completed_trials if step in t.intermediate_values
    ]

    if not intermediate_values:
        return math.nan

    if direction == ExperimentDirection.MAXIMIZE:
        percentile = 100 - percentile

    return float(
        np.nanpercentile(
            np.array(intermediate_values, np.float),
            percentile,
        )
    )


def _is_first_in_interval_step(
    step: int, intermediate_steps: KeysView[int], n_warmup_steps: int, interval_steps: int
) -> bool:

    nearest_lower_stopping_step = (
        step - n_warmup_steps
    ) // interval_steps * interval_steps + n_warmup_steps
    assert nearest_lower_stopping_step >= 0

    # `intermediate_steps` may not be sorted so we must go through all elements.
    second_last_step = functools.reduce(
        lambda second_last_step, s: s if s > second_last_step and s != step else second_last_step,
        intermediate_steps,
        -1,
    )

    return second_last_step < nearest_lower_stopping_step


class PercentileStopper(BaseStopper):
    """Stopper to keep the specified percentile of the trials.

    """

    def __init__(
        self,
        percentile: float,
        n_startup_trials: int = 5,
        n_warmup_steps: int = 0,
        interval_steps: int = 1,
    ) -> None:

        if not 0.0 <= percentile <= 100:
            raise ValueError(
                "Percentile must be between 0 and 100 inclusive but got {}.".format(percentile)
            )
        if n_startup_trials < 0:
            raise ValueError(
                "Number of startup trials cannot be negative but got {}.".format(n_startup_trials)
            )
        if n_warmup_steps < 0:
            raise ValueError(
                "Number of warmup steps cannot be negative but got {}.".format(n_warmup_steps)
            )
        if interval_steps < 1:
            raise ValueError(
                "Pruning interval steps must be at least 1 but got {}.".format(interval_steps)
            )

        self._percentile = percentile
        self._n_startup_trials = n_startup_trials
        self._n_warmup_steps = n_warmup_steps
        self._interval_steps = interval_steps

    def stop(self, experiment: "opts.experiment.Experiment", trial: "opts.trial.FrozenTrial") -> bool:

        all_trials = experiment.get_trials(deepcopy=False)
        n_trials = len([t for t in all_trials if t.state == TrialState.COMPLETE])

        if n_trials == 0:
            return False

        if n_trials < self._n_startup_trials:
            return False

        step = trial.last_step
        if step is None:
            return False

        n_warmup_steps = self._n_warmup_steps
        if step < n_warmup_steps:
            return False

        if not _is_first_in_interval_step(
            step, trial.intermediate_values.keys(), n_warmup_steps, self._interval_steps
        ):
            return False

        direction = experiment.direction
        best_intermediate_result = _get_best_intermediate_result_over_steps(trial, direction)
        if math.isnan(best_intermediate_result):
            return True

        p = _get_percentile_intermediate_result_over_trials(
            all_trials, direction, step, self._percentile
        )
        if math.isnan(p):
            return False

        if direction == ExperimentDirection.MAXIMIZE:
            return best_intermediate_result < p
        return best_intermediate_result > p















