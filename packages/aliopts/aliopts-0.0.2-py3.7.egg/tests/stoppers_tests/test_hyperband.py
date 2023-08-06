"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/30 4:44 下午
@Software: PyCharm
@File    : test_hyperband.py
@E-mail  : victor.xsyang@gmail.com
"""
from typing import Callable
from unittest import mock

import numpy
import pytest

import opts


MIN_RESOURCE = 1
MAX_RESOURCE = 16
REDUCTION_FACTOR = 2
N_BRACKETS = 4
EARLY_STOPPING_RATE_LOW = 0
EARLY_STOPPING_RATE_HIGH = 3
N_REPORTS = 10
EXPECTED_N_TRIALS_PER_BRACKET = 10


def test_hyperband_stopper_intermediate_values() -> None:
    stopper = opts.stoppers.HyperbandStopper(
        min_resource=MIN_RESOURCE, max_resource=MAX_RESOURCE, reduction_factor=REDUCTION_FACTOR
    )

    experiment = opts.experiment.create_experiment(sampler=opts.samplers.RandomSampler(), stopper=stopper)

    def objective(trial: opts.trial.Trial) -> float:
        for i in range(N_REPORTS):
            trial.report(i, step=i)

        return 1.0

    experiment.optimize(objective, n_trials=N_BRACKETS * EXPECTED_N_TRIALS_PER_BRACKET)

    trials = experiment.trials
    assert len(trials) == N_BRACKETS * EXPECTED_N_TRIALS_PER_BRACKET


def test_bracket_experiment() -> None:
    stopper = opts.stoppers.HyperbandStopper(
        min_resource=MIN_RESOURCE, max_resource=MAX_RESOURCE, reduction_factor=REDUCTION_FACTOR
    )
    experiment = opts.experiment.create_experiment(sampler=opts.samplers.RandomSampler(), stopper=stopper)
    bracket_experiment = stopper._create_bracket_experiment(experiment, 0)

    with pytest.raises(AttributeError):
        bracket_experiment.optimize(lambda *args: 1.0)

    for attr in ("set_user_attr", "set_system_attr"):
        with pytest.raises(AttributeError):
            getattr(bracket_experiment, attr)("abc", 100)

    for attr in ("user_attrs", "system_attrs"):
        with pytest.raises(AttributeError):
            getattr(bracket_experiment, attr)

    with pytest.raises(AttributeError):
        bracket_experiment.trials_dataframe()

    bracket_experiment.get_trials()
    bracket_experiment.direction
    bracket_experiment._storage
    bracket_experiment._experiment_id
    bracket_experiment.stopper
    bracket_experiment.experiment_name
    # As `_BracketStudy` is defined inside `HyperbandPruner`,
    # we cannot do `assert isinstance(bracket_study, _BracketStudy)`.
    # This is why the below line is ignored by mypy checks.
    bracket_experiment._bracket_id  # type: ignore


def test_hyperband_max_resource_is_auto() -> None:
    stopper = opts.stoppers.HyperbandStopper(
        min_resource=MIN_RESOURCE, reduction_factor=REDUCTION_FACTOR
    )
    experiment = opts.experiment.create_experiment(sampler=opts.samplers.RandomSampler(), stopper=stopper)

    def objective(trial: opts.trial.Trial) -> float:
        for i in range(N_REPORTS):
            trial.report(1.0, i)
            if trial.should_stop():
                raise opts.TrialStop()

        return 1.0

    experiment.optimize(objective, n_trials=N_BRACKETS * EXPECTED_N_TRIALS_PER_BRACKET)

    assert N_REPORTS == stopper._max_resource


def test_hyperband_max_resource_value_error() -> None:
    with pytest.raises(ValueError):
        _ = opts.stoppers.HyperbandStopper(max_resource="not_appropriate")


@pytest.mark.parametrize(
    "sampler_init_func",
    [
        lambda: opts.samplers.RandomSampler(),
        (lambda: opts.samplers.TPESampler(n_startup_trials=1)),
        (
            lambda: opts.samplers.GridSampler(
                search_space={"value": numpy.linspace(0.0, 1.0, 8, endpoint=False).tolist()}
            )
        ),
        (lambda: opts.samplers.CmaEsSampler(n_startup_trials=1)),
    ],
)
def test_hyperband_filter_experiment(
    sampler_init_func: Callable[[], opts.samplers.BaseSampler]
) -> None:
    def objective(trial: opts.trial.Trial) -> float:
        return trial.suggest_uniform("value", 0.0, 1.0)

    n_trials = 8
    n_brackets = 4
    expected_n_trials_per_bracket = n_trials // n_brackets
    with mock.patch(
        "opts.stoppers.HyperbandStopper._get_bracket_id",
        new=mock.Mock(side_effect=lambda experiment, trial: trial.number % n_brackets),
    ):
        for method_name in [
            "infer_relative_search_space",
            "sample_relative",
            "sample_independent",
        ]:
            sampler = sampler_init_func()
            stopper = opts.stoppers.HyperbandStopper(
                min_resource=MIN_RESOURCE,
                max_resource=MAX_RESOURCE,
                reduction_factor=REDUCTION_FACTOR,
            )
            with mock.patch(
                "opts.samplers.{}.{}".format(sampler.__class__.__name__, method_name),
                wraps=getattr(sampler, method_name),
            ) as method_mock:
                experiment = opts.experiment.create_experiment(sampler=sampler, stopper=stopper)
                experiment.optimize(objective, n_trials=n_trials)
                args = method_mock.call_args[0]
                experiment = args[0]
                trials = experiment.get_trials()
                assert len(trials) == expected_n_trials_per_bracket


@pytest.mark.parametrize(
    "stopper_init_func",
    [
        lambda: opts.stoppers.NopStopper(),
        lambda: opts.stoppers.MedianStopper(),
        lambda: opts.stoppers.ThresholdStopper(lower=0.5),
        lambda: opts.stoppers.SuccessiveHalvingStopper(),
    ],
)
def test_hyperband_no_filter_experiment(
    stopper_init_func: Callable[[], opts.stoppers.BaseStopper]
) -> None:
    def objective(trial: opts.trial.Trial) -> float:
        return trial.suggest_uniform("value", 0.0, 1.0)

    n_trials = 10
    for method_name in [
        "infer_relative_search_space",
        "sample_relative",
        "sample_independent",
    ]:
        sampler = opts.samplers.RandomSampler()
        stopper = stopper_init_func()
        with mock.patch(
            "opts.samplers.{}.{}".format(sampler.__class__.__name__, method_name),
            wraps=getattr(sampler, method_name),
        ) as method_mock:
            experiment = opts.experiment.create_experiment(sampler=sampler, stopper=stopper)
            experiment.optimize(objective, n_trials=n_trials)
            args = method_mock.call_args[0]
            experiment = args[0]
            trials = experiment.get_trials()
            assert len(trials) == n_trials


@pytest.mark.parametrize(
    "sampler_init_func",
    [
        lambda: opts.samplers.RandomSampler(),
        (lambda: opts.samplers.TPESampler(n_startup_trials=1)),
        (
            lambda: opts.samplers.GridSampler(
                search_space={"value": numpy.linspace(0.0, 1.0, 10, endpoint=False).tolist()}
            )
        ),
        (lambda: opts.samplers.CmaEsSampler(n_startup_trials=1)),
    ],
)
def test_hyperband_no_call_of_filter_experiment_in_should_stop(
    sampler_init_func: Callable[[], opts.samplers.BaseSampler]
) -> None:
    def objective(trial: opts.trial.Trial) -> float:
        with mock.patch("opts.stoppers._filter_experiment") as method_mock:
            for i in range(N_REPORTS):
                trial.report(i, step=i)
                if trial.should_stop():
                    method_mock.assert_not_called()
                    raise opts.TrialStop()
                else:
                    method_mock.assert_not_called()

        return 1.0

    sampler = sampler_init_func()
    stopper = opts.stoppers.HyperbandStopper(
        min_resource=MIN_RESOURCE, max_resource=MAX_RESOURCE, reduction_factor=REDUCTION_FACTOR
    )
    experiment = opts.experiment.create_experiment(sampler=sampler, stopper=stopper)
    experiment.optimize(objective, n_trials=10)
