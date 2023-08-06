"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/21 4:54 下午
@Software: PyCharm
@File    : test_experiment.py
@E-mail  : victor.xsyang@gmail.com
"""
import copy
import itertools
import multiprocessing
import pickle
import threading
import time
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Tuple
from unittest.mock import Mock  # NOQA
from unittest.mock import patch
import uuid

import _pytest.capture
from _pytest.recwarn import WarningsRecorder
import joblib
import pandas as pd
import pytest

import opts
from opts import _optimize
from opts import create_trial
from opts.testing.storage import StorageSupplier

CallbackFuncType = Callable[[opts.experiment.Experiment, opts.trial.FrozenTrial], None]

STORAGE_MODES = [
    "inmemory",
    "sqlite",
    "cache",
    "redis",
]


def func(trial: opts.trial.Trial, x_max: float = 1.0) -> float:
    x = trial.suggest_uniform("x", -x_max, x_max)
    y = trial.suggest_loguniform("y", 20, 30)
    z = trial.suggest_categorical("z", (-1.0, 1.0))
    assert isinstance(z, float)
    return (x - 2) ** 2 + (y - 25) ** 2 + z


class Func(object):
    def __init__(self, sleep_sec: Optional[float] = None) -> None:
        self.n_calls = 0
        self.sleep_sec = sleep_sec
        self.lock = threading.Lock()
        self.x_max = 10.0

    def __call__(self, trial: opts.trial.Trial) -> float:
        with self.lock:
            self.n_calls += 1
            x_max = self.x_max
            self.x_max *= 0.9

        # Sleep for testing parallelism
        if self.sleep_sec is not None:
            time.sleep(self.sleep_sec)

        value = func(trial, x_max)
        check_params(trial.params)
        return value


def check_params(params: Dict[str, Any]) -> None:
    assert sorted(params.keys()) == ["x", "y", "z"]


def check_value(value: Optional[float]) -> None:
    assert isinstance(value, float)
    assert -1.0 <= value <= 12.0 ** 2 + 5.0 ** 2 + 1.0


def check_frozen_trial(frozen_trial: opts.trial.FrozenTrial) -> None:
    if frozen_trial.state == opts.trial.TrialState.COMPLETE:
        check_params(frozen_trial.params)
        check_value(frozen_trial.value)


def check_experiment(experiment: opts.Experiment) -> None:
    for trial in experiment.trials:
        check_frozen_trial(trial)

    complete_trials = [t for t in experiment.trials if t.state == opts.trial.TrialState.COMPLETE]
    if len(complete_trials) == 0:
        with pytest.raises(ValueError):
            experiment.best_params
        with pytest.raises(ValueError):
            experiment.best_value
        with pytest.raises(ValueError):
            experiment.best_trial
    else:
        check_params(experiment.best_params)
        check_value(experiment.best_value)
        check_frozen_trial(experiment.best_trial)


def test_optimize_trivial_in_memory_new() -> None:
    experiment = opts.create_experiment()
    experiment.optimize(func, n_trials=10)
    check_experiment(experiment)


def test_optimize_trivial_in_memory_resume() -> None:
    experiment = opts.create_experiment()
    experiment.optimize(func, n_trials=10)
    experiment.optimize(func, n_trials=10)
    check_experiment(experiment)
