"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/27 2:45 下午
@Software: PyCharm
@File    : _successive_halving.py
@E-mail  : victor.xsyang@gmail.com
"""
import math
from typing import List
from typing import Optional
from typing import Union

import opts
from opts._experiment_direction import ExperimentDirection
from opts.stoppers._base import BaseStopper
from opts.trial._state import TrialState


class SuccessiveHalvingStopper(BaseStopper):
    """Stopper using Asynchronous Successive Halving Algorithm.

    """

    def __init__(
            self,
            min_resource: Union[str, int] = "auto",
            reduction_factor: int = 4,
            min_early_stopping_rate: int = 0,
    ) -> None:

        if isinstance(min_resource, str) and min_resource != "auto":
            raise ValueError(
                "The value of `min_resource` is {}, "
                "but must be either `min_resource` >= 1 or 'auto'".format(min_resource)
            )

        if isinstance(min_resource, int) and min_resource < 1:
            raise ValueError(
                "The value of `min_resource` is {}, "
                "but must be either `min_resource >= 1` or 'auto'".format(min_resource)
            )

        if reduction_factor < 2:
            raise ValueError(
                "The value of `reduction_factor` is {}, "
                "but must be `reduction_factor >= 2`".format(reduction_factor)
            )

        if min_early_stopping_rate < 0:
            raise ValueError(
                "The value of `min_early_stopping_rate` is {}, "
                "but must be `min_early_stopping_rate >= 0`".format(min_early_stopping_rate)
            )

        self._min_resource: Optional[int] = None
        if isinstance(min_resource, int):
            self._min_resource = min_resource
        self._reduction_factor = reduction_factor
        self._min_early_stopping_rate = min_early_stopping_rate

    def stop(self, experiment: "opts.experiment.Experiment", trial: "opts.trail.FrozenTrial") -> bool:

        step = trial.last_step
        if step is None:
            return False

        rung = _get_current_rung(trial)
        value = trial.intermediate_values[step]
        trials: Optional[List["optuna.trial.FrozenTrial"]] = None

        while True:
            if self._min_resource is None:
                if trials is None:
                    trials = experiment.get_trials(deepcopy=False)
                self._min_resource = _estimate_min_resource(trials)
                if self._min_resource is None:
                    return False

            assert self._min_resource is not None
            rung_promotion_step = self._min_resource * (
                    self._reduction_factor ** (self._min_early_stopping_rate + rung)
            )
            if step < rung_promotion_step:
                return False

            if math.isnan(value):
                return True

            if trials is None:
                trials = experiment.get_trials(deepcopy=False)

            rung_key = _completed_rung_key(rung)

            experiment._storage.set_trial_system_attr(trial._trial_id, rung_key, value)

            if not _is_trial_promotable_to_next_rung(
                    value,
                    _get_competing_values(trials, value, rung_key),
                    self._reduction_factor,
                    experiment.direction,
            ):
                return True

            rung += 1


def _estimate_min_resource(trials: List["opts.trial.FrozenTrial"]) -> Optional[int]:
    n_steps = [
        t.last_step for t in trials if t.state == TrialState.COMPLETE and t.last_step is not None
    ]

    if not n_steps:
        return None

    # Get the maximum number of steps and divide it by 100.
    last_step = max(n_steps)
    return max(last_step // 100, 1)


def _get_current_rung(trial: "opts.trial.FrozenTrial") -> int:
    # The following loop takes `O(log step)` iterations.
    rung = 0
    while _completed_rung_key(rung) in trial.system_attrs:
        rung += 1
    return rung


def _completed_rung_key(rung: int) -> str:
    return "completed_rung_{}".format(rung)


def _get_competing_values(
        trials: List["opts.trial.FrozenTrial"], value: float, rung_key: str
) -> List[float]:
    competing_values = [t.system_attrs[rung_key] for t in trials if rung_key in t.system_attrs]
    competing_values.append(value)
    return competing_values


def _is_trial_promotable_to_next_rung(
        value: float,
        competing_values: List[float],
        reduction_factor: int,
        experiment_direction: ExperimentDirection,
) -> bool:
    promotable_idx = (len(competing_values) // reduction_factor) - 1

    if promotable_idx == -1:
        # Optuna does not support suspending or resuming ongoing trials. Therefore, for the first
        # `eta - 1` trials, this implementation instead promotes the trial if its value is the
        # smallest one among the competing values.
        promotable_idx = 0

    competing_values.sort()
    if experiment_direction == ExperimentDirection.MAXIMIZE:
        return value >= competing_values[-(promotable_idx + 1)]
    return value <= competing_values[promotable_idx]
