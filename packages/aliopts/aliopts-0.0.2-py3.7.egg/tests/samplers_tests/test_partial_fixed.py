"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/26 12:23 下午
@Software: PyCharm
@File    : test_partial_fixed.py
@E-mail  : victor.xsyang@gmail.com
"""
from typing import cast
from unittest.mock import patch
import warnings

import pytest

import opts
from opts.samplers import PartialFixedSampler
from opts.samplers import RandomSampler
from opts.trial import Trial


def test_fixed_sampling() -> None:
    def objective(trial: Trial) -> float:
        x = trial.suggest_float("x", -10, 10)
        y = trial.suggest_float("y", -10, 10)
        return x ** 2 + y ** 2

    experiment0 = opts.create_experiment()
    experiment0.sampler = RandomSampler(seed=42)
    experiment0.optimize(objective, n_trials=1)
    x_sampled0 = experiment0.trials[0].params["x"]

    # Fix parameter ``y`` as 0.
    experiment1 = opts.create_experiment()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        experiment1.sampler = PartialFixedSampler(
            fixed_params={"y": 0}, base_sampler=RandomSampler(seed=42)
        )
    experiment1.optimize(objective, n_trials=1)

    x_sampled1 = experiment1.trials[0].params["x"]
    y_sampled1 = experiment1.trials[0].params["y"]
    assert x_sampled1 == x_sampled0
    assert y_sampled1 == 0


def test_float_to_int() -> None:
    def objective(trial: Trial) -> float:
        x = trial.suggest_int("x", -10, 10)
        y = trial.suggest_int("y", -10, 10)
        return x ** 2 + y ** 2

    fixed_y = 0.5

    # Parameters of Int-type-distribution are rounded to int-type,
    # even if they are defined as float-type.
    experiment = opts.create_experiment()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        experiment.sampler = PartialFixedSampler(
            fixed_params={"y": fixed_y}, base_sampler=experiment.sampler
        )
    experiment.optimize(objective, n_trials=1)
    assert experiment.trials[0].params["y"] == int(fixed_y)


@pytest.mark.parametrize("fixed_y", [-2, 2])
def test_out_of_the_range_numerical(fixed_y: int) -> None:
    def objective(trial: Trial) -> float:
        x = trial.suggest_int("x", -1, 1)
        y = trial.suggest_int("y", -1, 1)
        return x ** 2 + y ** 2

    # It is possible to fix numerical parameters as out-of-the-range value.
    # `UserWarning` will occur.
    experiment = opts.create_experiment()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        experiment.sampler = PartialFixedSampler(
            fixed_params={"y": fixed_y}, base_sampler=experiment.sampler
        )
    with pytest.warns(UserWarning):
        experiment.optimize(objective, n_trials=1)
    assert experiment.trials[0].params["y"] == fixed_y


def test_out_of_the_range_categorical() -> None:
    def objective(trial: Trial) -> float:
        x = trial.suggest_int("x", -1, 1)
        y = trial.suggest_categorical("y", [-1, 0, 1])
        y = cast(int, y)
        return x ** 2 + y ** 2

    fixed_y = 2

    # It isn't possible to fix categorical parameters as out-of-the-range value.
    # `ValueError` will occur.
    experiment = opts.create_experiment()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        experiment.sampler = PartialFixedSampler(
            fixed_params={"y": fixed_y}, base_sampler=experiment.sampler
        )
    with pytest.raises(ValueError):
        experiment.optimize(objective, n_trials=1)


def test_partial_fixed_experimental_warning() -> None:
    experiment = opts.create_experiment()
    with pytest.warns(opts.errors.ExperimentalWarning):
        opts.samplers.PartialFixedSampler(fixed_params={"x": 0}, base_sampler=experiment.sampler)


def test_reseed_rng() -> None:
    base_sampler = RandomSampler()
    experiment = opts.create_experiment(sampler=base_sampler)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = PartialFixedSampler(fixed_params={"x": 0}, base_sampler=experiment.sampler)
    original_seed = base_sampler._rng.seed

    with patch.object(base_sampler, "reseed_rng", wraps=base_sampler.reseed_rng) as mock_object:
        sampler.reseed_rng()
        assert mock_object.call_count == 1
        assert original_seed != base_sampler._rng.seed
