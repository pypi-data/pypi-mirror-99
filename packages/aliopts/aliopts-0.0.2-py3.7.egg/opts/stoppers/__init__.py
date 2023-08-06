"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/25 4:29 下午
@Software: PyCharm
@File    : __init__.py.py
@E-mail  : victor.xsyang@gmail.com
"""
from typing import TYPE_CHECKING

from opts.stoppers._base import BaseStopper
from opts.stoppers._hyperband import HyperbandStopper
from opts.stoppers._median import MedianStopper
from opts.stoppers._nos import NopStopper
from opts.stoppers._percentile import PercentileStopper
from opts.stoppers._successive_halving import SuccessiveHalvingStopper
from opts.stoppers._threshold import ThresholdStopper

if TYPE_CHECKING:
    from opts.experiment import Experiment
    from opts.trial import FrozenTrial

__all__ = [
    "BaseStopper",
    "HyperbandStopper",
    "MedianStopper",
    "NopStopper",
    "PercentileStopper",
    "SuccessiveHalvingStopper",
    "ThresholdStopper"
]


def _filter_experiment(experiment: "opts.experiment.Experiment", trial: "opts.trial.FrozenTrial") -> "Experiment":
    if isinstance(experiment.stopper, HyperbandStopper):
        stopper: HyperbandStopper = experiment.stopper
        return stopper._create_bracket_experiment(experiment, stopper._get_bracket_id(experiment, trial))
    else:
        return experiment
