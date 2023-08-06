"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/26 9:29 下午
@Software: PyCharm
@File    : _threshold.py
@E-mail  : victor.xsyang@gmail.com
"""
import math
from typing import Any
from typing import Optional

import opts
from opts.stoppers import BaseStopper
from opts.stoppers._percentile import _is_first_in_interval_step


def _check_value(value: Any) -> float:
    try:
        value = float(value)
    except (TypeError, ValueError):
        message = "The `value` argument is of type '{}' but supposed to be a float.".format(
            type(value).__name__
        )
        raise TypeError(message) from None
    return value


class ThresholdStopper(BaseStopper):
    """Stop to detect outlying metrics of the trials.

    Stop if a metric exceeds upper threshold,
    falls behind lower threshold or reaches ``nan``.
    """
    def __init__(
            self,
            lower: Optional[float] = None,
            upper: Optional[float] = None,
            n_warmup_steps: int = 0,
            interval_steps: int = 1
    ) -> None:
        if lower is None and upper is None:
            raise TypeError("Either lower or upper must be specified")
        if lower is not None:
            lower = _check_value(lower)
        if upper is not None:
            upper = _check_value(upper)

        lower = lower if lower is not None else -float("inf")
        upper = upper if upper is not None else float("inf")

        if lower > upper:
            raise ValueError("lower should be smaller than upper.")

        if n_warmup_steps < 0:
            raise ValueError(
                "Number of warmup steps cannot be negative but got {}.".format(n_warmup_steps)
            )

        if interval_steps < 1:
            raise ValueError(
                "Stopping interval steps must be at lest 1 but got {}.".format(interval_steps)
            )

        self._lower = lower
        self._upper = upper
        self._n_warmup_steps = n_warmup_steps
        self._interval_steps = interval_steps


    def stop(self, experiment: "opts.experiment.Experiment", trial: "opts.trial.FrozenTrial") -> bool:

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

        latest_value = trial.intermediate_values[step]
        if math.isnan(latest_value):
            return True

        if latest_value < self._lower:
            return True

        if latest_value > self._upper:
            return True

        return False






