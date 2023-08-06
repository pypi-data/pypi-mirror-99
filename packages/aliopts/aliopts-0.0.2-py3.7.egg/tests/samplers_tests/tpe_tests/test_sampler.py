"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/30 11:43 上午
@Software: PyCharm
@File    : test_sampler.py
@E-mail  : victor.xsyang@gmail.com
"""
import random
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union
from unittest.mock import Mock
from unittest.mock import patch
import warnings

import numpy as np
import pytest

import opts
from opts import samples
from opts import TrialStop
from opts.samplers import _tpe
from opts.samplers import TPESampler
from opts.trial import Trial


@pytest.mark.parametrize("use_hyperband", [False, True])
def test_hyperopt_parameters(use_hyperband: bool) -> None:

    sampler = TPESampler(**TPESampler.hyperopt_parameters())
    experiment = opts.create_experiment(
        sampler=sampler, stopper=opts.stoppers.HyperbandStopper() if use_hyperband else None
    )
    experiment.optimize(lambda t: t.suggest_uniform("x", 10, 20), n_trials=50)


def test_multivariate_experimental_warning() -> None:
    with pytest.warns(opts.errors.ExperimentalWarning):
        opts.samplers.TPESampler(multivariate=True)


def test_infer_relative_search_space() -> None:
    sampler = TPESampler()
    search_space = {
        "a": samples.UniformDistribution(1.0, 100.0),
        "b": samples.LogUniformDistribution(1.0, 100.0),
        "c": samples.DiscreteUniformDistribution(1.0, 100.0, 3.0),
        "d": samples.IntUniformDistribution(1, 100),
        "e": samples.IntUniformDistribution(0, 100, step=2),
        "f": samples.IntLogUniformDistribution(1, 100),
        "g": samples.CategoricalDistribution(["x", "y", "z"]),
    }

    def obj(t: Trial) -> float:
        t.suggest_uniform("a", 1.0, 100.0)
        t.suggest_loguniform("b", 1.0, 100.0)
        t.suggest_discrete_uniform("c", 1.0, 100.0, 3.0)
        t.suggest_int("d", 1, 100)
        t.suggest_int("e", 0, 100, step=2)
        t.suggest_int("f", 1, 100, log=True)
        t.suggest_categorical("g", ["x", "y", "z"])
        return 0.0

    # Study and frozen-trial are not supposed to be accessed.
    experiment1 = Mock(spec=[])
    frozen_trial = Mock(spec=[])
    assert sampler.infer_relative_search_space(experiment1, frozen_trial) == {}

    experiment2 = opts.create_experiment(sampler=sampler)
    experiment2.optimize(obj, n_trials=1)
    assert sampler.infer_relative_search_space(experiment2, experiment2.best_trial) == {}

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(multivariate=True)
    experiment3 = opts.create_experiment(sampler=sampler)
    experiment3.optimize(obj, n_trials=1)
    assert sampler.infer_relative_search_space(experiment3, experiment3.best_trial) == search_space


@pytest.mark.parametrize("multivariate", [False, True])
def test_sample_relative_empty_input(multivariate: bool) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(multivariate=multivariate)
    # Study and frozen-trial are not supposed to be accessed.
    experiment = Mock(spec=[])
    frozen_trial = Mock(spec=[])
    assert sampler.sample_relative(experiment, frozen_trial, {}) == {}


def test_sample_relative_seed_fix() -> None:
    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=dist) for i in range(1, 8)]

    # Prepare a trial and a sample for later checks.
    trial = frozen_trial_factory(8)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        suggestion = sampler.sample_relative(experiment, trial, {"param-a": dist})

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_relative(experiment, trial, {"param-a": dist}) == suggestion

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=1, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_relative(experiment, trial, {"param-a": dist}) != suggestion


def test_sample_relative_prior() -> None:
    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=dist) for i in range(1, 8)]

    # Prepare a trial and a sample for later checks.
    trial = frozen_trial_factory(8)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        suggestion = sampler.sample_relative(experiment, trial, {"param-a": dist})

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(consider_prior=False, n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_relative(experiment, trial, {"param-a": dist}) != suggestion

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(prior_weight=0.2, n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_relative(experiment, trial, {"param-a": dist}) != suggestion


def test_sample_relative_n_startup_trial() -> None:
    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=dist) for i in range(1, 8)]

    trial = frozen_trial_factory(8)
    # sample_relative returns {} for only 4 observations.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials[:4]):
        assert sampler.sample_relative(experiment, trial, {"param-a": dist}) == {}
    # sample_relative returns some value for only 7 observations.
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert "param-a" in sampler.sample_relative(experiment, trial, {"param-a": dist}).keys()


def test_sample_relative_misc_arguments() -> None:
    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=dist) for i in range(1, 40)]

    # Prepare a trial and a sample for later checks.
    trial = frozen_trial_factory(40)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        suggestion = sampler.sample_relative(experiment, trial, {"param-a": dist})

    # Test misc. parameters.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_ei_candidates=13, n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_relative(experiment, trial, {"param-a": dist}) != suggestion

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(gamma=lambda _: 5, n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_relative(experiment, trial, {"param-a": dist}) != suggestion

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(
            weights=lambda n: np.asarray([i ** 2 + 1 for i in range(n)]),
            n_startup_trials=5,
            seed=0,
            multivariate=True,
        )
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_relative(experiment, trial, {"param-a": dist}) != suggestion


def test_sample_relative_uniform_distributions() -> None:
    experiment= opts.create_experiment()

    # Prepare sample from uniform distribution for cheking other distributions.
    uni_dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=uni_dist) for i in range(1, 8)]
    trial = frozen_trial_factory(8)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        uniform_suggestion = sampler.sample_relative(experiment, trial, {"param-a": uni_dist})
    assert 1.0 <= uniform_suggestion["param-a"] < 100.0


def test_sample_relative_log_uniform_distributions() -> None:
    """Prepare sample from uniform distribution for cheking other distributions."""

    experiment = opts.create_experiment()

    uni_dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=uni_dist) for i in range(1, 8)]
    trial = frozen_trial_factory(8)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        uniform_suggestion = sampler.sample_relative(experiment, trial, {"param-a": uni_dist})

    # Test sample from log-uniform is different from uniform.
    log_dist = opts.samples.LogUniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=log_dist) for i in range(1, 8)]
    trial = frozen_trial_factory(8)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        loguniform_suggestion = sampler.sample_relative(experiment, trial, {"param-a": log_dist})
    assert 1.0 <= loguniform_suggestion["param-a"] < 100.0
    assert uniform_suggestion["param-a"] != loguniform_suggestion["param-a"]


def test_sample_relative_disrete_uniform_distributions() -> None:
    """Test samples from discrete have expected intervals."""

    experiment = opts.create_experiment()
    disc_dist = opts.samples.DiscreteUniformDistribution(1.0, 100.0, 0.1)

    def value_fn(idx: int) -> float:
        random.seed(idx)
        return int(random.random() * 1000) * 0.1

    past_trials = [frozen_trial_factory(i, dist=disc_dist, value_fn=value_fn) for i in range(1, 8)]
    trial = frozen_trial_factory(8)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        discrete_uniform_suggestion = sampler.sample_relative(experiment, trial, {"param-a": disc_dist})
    assert 1.0 <= discrete_uniform_suggestion["param-a"] <= 100.0
    np.testing.assert_almost_equal(
        int(discrete_uniform_suggestion["param-a"] * 10),
        discrete_uniform_suggestion["param-a"] * 10,
    )


def test_sample_relative_categorical_distributions() -> None:
    """Test samples are drawn from the specified category."""

    experiment = opts.create_experiment()
    categories = [i * 0.3 + 1.0 for i in range(330)]

    def cat_value_fn(idx: int) -> float:
        random.seed(idx)
        return categories[random.randint(0, len(categories) - 1)]

    cat_dist = opts.samples.CategoricalDistribution(categories)
    past_trials = [
        frozen_trial_factory(i, dist=cat_dist, value_fn=cat_value_fn) for i in range(1, 8)
    ]
    trial = frozen_trial_factory(8)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        categorical_suggestion = sampler.sample_relative(experiment, trial, {"param-a": cat_dist})
    assert categorical_suggestion["param-a"] in categories


@pytest.mark.parametrize("step", [1, 2])
def test_sample_relative_int_uniform_distributions(step: int) -> None:
    """Test sampling from int distribution returns integer."""

    experiment = opts.create_experiment()

    def int_value_fn(idx: int) -> float:
        random.seed(idx)
        return step * random.randint(0, 100 // step)

    int_dist = opts.samples.IntUniformDistribution(0, 100, step=step)
    past_trials = [
        frozen_trial_factory(i, dist=int_dist, value_fn=int_value_fn) for i in range(1, 8)
    ]
    trial = frozen_trial_factory(8)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        int_suggestion = sampler.sample_relative(experiment, trial, {"param-a": int_dist})
    assert 1 <= int_suggestion["param-a"] <= 100
    assert isinstance(int_suggestion["param-a"], int)
    assert int_suggestion["param-a"] % step == 0


def test_sample_relative_int_loguniform_distributions() -> None:
    """Test sampling from int distribution returns integer."""

    experiment = opts.create_experiment()

    def int_value_fn(idx: int) -> float:
        random.seed(idx)
        return random.randint(0, 100)

    intlog_dist = opts.samples.IntLogUniformDistribution(1, 100)
    past_trials = [
        frozen_trial_factory(i, dist=intlog_dist, value_fn=int_value_fn) for i in range(1, 8)
    ]
    trial = frozen_trial_factory(8)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        intlog_suggestion = sampler.sample_relative(experiment, trial, {"param-a": intlog_dist})
    assert 1 <= intlog_suggestion["param-a"] <= 100
    assert isinstance(intlog_suggestion["param-a"], int)


@pytest.mark.parametrize(
    "state",
    [
        (opts.trial.TrialState.FAIL,),
        (opts.trial.TrialState.STOP,),
        (opts.trial.TrialState.RUNNING,),
        (opts.trial.TrialState.WAITING,),
    ],
)
def test_sample_relative_handle_unsuccessful_states(
    state: opts.trial.TrialState,
) -> None:
    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)

    # Prepare sampling result for later tests.
    past_trials = [frozen_trial_factory(i, dist=dist) for i in range(1, 100)]
    trial = frozen_trial_factory(100)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        all_success_suggestion = sampler.sample_relative(experiment, trial, {"param-a": dist})

    # Test unsuccessful trials are handled differently.
    state_fn = build_state_fn(state)
    past_trials = [frozen_trial_factory(i, dist=dist, state_fn=state_fn) for i in range(1, 100)]
    trial = frozen_trial_factory(100)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        partial_unsuccessful_suggestion = sampler.sample_relative(experiment, trial, {"param-a": dist})
    assert partial_unsuccessful_suggestion != all_success_suggestion


def test_sample_relative_ignored_states() -> None:
    """Tests FAIL, RUNNING, and WAITING states are equally."""

    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)

    suggestions = []
    for state in [
        opts.trial.TrialState.FAIL,
        opts.trial.TrialState.RUNNING,
        opts.trial.TrialState.WAITING,
    ]:
        state_fn = build_state_fn(state)
        past_trials = [frozen_trial_factory(i, dist=dist, state_fn=state_fn) for i in range(1, 30)]
        trial = frozen_trial_factory(30)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
            sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
        with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
            suggestions.append(sampler.sample_relative(experiment, trial, {"param-a": dist})["param-a"])

    assert len(set(suggestions)) == 1


def test_sample_relative_stop_state() -> None:
    """Tests Stop state is treated differently from both FAIL and COMPLETE."""

    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)

    suggestions = []
    for state in [
        opts.trial.TrialState.COMPLETE,
        opts.trial.TrialState.FAIL,
        opts.trial.TrialState.STOP,
    ]:
        state_fn = build_state_fn(state)
        past_trials = [frozen_trial_factory(i, dist=dist, state_fn=state_fn) for i in range(1, 40)]
        trial = frozen_trial_factory(40)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
            sampler = TPESampler(n_startup_trials=5, seed=0, multivariate=True)
        with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
            suggestions.append(sampler.sample_relative(experiment, trial, {"param-a": dist})["param-a"])

    assert len(set(suggestions)) == 3


def test_sample_independent_seed_fix() -> None:
    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=dist) for i in range(1, 8)]

    # Prepare a trial and a sample for later checks.
    trial = frozen_trial_factory(8)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        suggestion = sampler.sample_independent(experiment, trial, "param-a", dist)

    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_independent(experiment, trial, "param-a", dist) == suggestion

    sampler = TPESampler(n_startup_trials=5, seed=1)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_independent(experiment, trial, "param-a", dist) != suggestion


def test_sample_independent_prior() -> None:
    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=dist) for i in range(1, 8)]

    # Prepare a trial and a sample for later checks.
    trial = frozen_trial_factory(8)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        suggestion = sampler.sample_independent(experiment, trial, "param-a", dist)

    sampler = TPESampler(consider_prior=False, n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_independent(experiment, trial, "param-a", dist) != suggestion

    sampler = TPESampler(prior_weight=0.5, n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_independent(experiment, trial, "param-a", dist) != suggestion


def test_sample_independent_n_startup_trial() -> None:
    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=dist) for i in range(1, 8)]

    trial = frozen_trial_factory(8)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials[:4]):
        with patch.object(
            opts.samplers.RandomSampler, "sample_independent", return_value=1.0
        ) as sample_method:
            sampler.sample_independent(experiment, trial, "param-a", dist)
    assert sample_method.call_count == 1
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        with patch.object(
            opts.samplers.RandomSampler, "sample_independent", return_value=1.0
        ) as sample_method:
            sampler.sample_independent(experiment, trial, "param-a", dist)
    assert sample_method.call_count == 0


def test_sample_independent_misc_arguments() -> None:
    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=dist) for i in range(1, 8)]

    # Prepare a trial and a sample for later checks.
    trial = frozen_trial_factory(8)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        suggestion = sampler.sample_independent(experiment, trial, "param-a", dist)

    # Test misc. parameters.
    sampler = TPESampler(n_ei_candidates=13, n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_independent(experiment, trial, "param-a", dist) != suggestion

    sampler = TPESampler(gamma=lambda _: 5, n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        assert sampler.sample_independent(experiment, trial, "param-a", dist) != suggestion

    sampler = TPESampler(
        weights=lambda i: np.asarray([i * 0.11 for i in range(7)]), n_startup_trials=5, seed=0
    )
    with patch("opts.Experiment.get_trials", return_value=past_trials):
        assert sampler.sample_independent(experiment, trial, "param-a", dist) != suggestion


def test_sample_independent_uniform_distributions() -> None:
    experiment= opts.create_experiment()

    # Prepare sample from uniform distribution for cheking other distributions.
    uni_dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=uni_dist) for i in range(1, 8)]
    trial = frozen_trial_factory(8)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        uniform_suggestion = sampler.sample_independent(experiment, trial, "param-a", uni_dist)
    assert 1.0 <= uniform_suggestion < 100.0


def test_sample_independent_log_uniform_distributions() -> None:
    """Prepare sample from uniform distribution for cheking other distributions."""

    experiment = opts.create_experiment()

    uni_dist = opts.samples.UniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=uni_dist) for i in range(1, 8)]
    trial = frozen_trial_factory(8)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        uniform_suggestion = sampler.sample_independent(experiment, trial, "param-a", uni_dist)

    # Test sample from log-uniform is different from uniform.
    log_dist = opts.samples.LogUniformDistribution(1.0, 100.0)
    past_trials = [frozen_trial_factory(i, dist=log_dist) for i in range(1, 8)]
    trial = frozen_trial_factory(8)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        loguniform_suggestion = sampler.sample_independent(experiment, trial, "param-a", log_dist)
    assert 1.0 <= loguniform_suggestion < 100.0
    assert uniform_suggestion != loguniform_suggestion


def test_sample_independent_disrete_uniform_distributions() -> None:
    """Test samples from discrete have expected intervals."""

    experiment = opts.create_experiment()
    disc_dist = opts.samples.DiscreteUniformDistribution(1.0, 100.0, 0.1)

    def value_fn(idx: int) -> float:
        random.seed(idx)
        return int(random.random() * 1000) * 0.1

    past_trials = [frozen_trial_factory(i, dist=disc_dist, value_fn=value_fn) for i in range(1, 8)]
    trial = frozen_trial_factory(8)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch("opts.Experiment.get_trials", return_value=past_trials):
        discrete_uniform_suggestion = sampler.sample_independent(
            experiment, trial, "param-a", disc_dist
        )
    assert 1.0 <= discrete_uniform_suggestion <= 100.0
    assert abs(int(discrete_uniform_suggestion * 10) - discrete_uniform_suggestion * 10) < 1e-3


def test_sample_independent_categorical_distributions() -> None:
    """Test samples are drawn from the specified category."""

    experiment = opts.create_experiment()
    categories = [i * 0.3 + 1.0 for i in range(330)]

    def cat_value_fn(idx: int) -> float:
        random.seed(idx)
        return categories[random.randint(0, len(categories) - 1)]

    cat_dist = opts.samples.CategoricalDistribution(categories)
    past_trials = [
        frozen_trial_factory(i, dist=cat_dist, value_fn=cat_value_fn) for i in range(1, 8)
    ]
    trial = frozen_trial_factory(8)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        categorical_suggestion = sampler.sample_independent(experiment, trial, "param-a", cat_dist)
    assert categorical_suggestion in categories


def test_sample_independent_int_uniform_distributions() -> None:
    """Test sampling from int distribution returns integer."""

    experiment = opts.create_experiment()

    def int_value_fn(idx: int) -> float:
        random.seed(idx)
        return random.randint(0, 100)

    int_dist = opts.samples.IntUniformDistribution(1, 100)
    past_trials = [
        frozen_trial_factory(i, dist=int_dist, value_fn=int_value_fn) for i in range(1, 8)
    ]
    trial = frozen_trial_factory(8)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        int_suggestion = sampler.sample_independent(experiment, trial, "param-a", int_dist)
    assert 1 <= int_suggestion <= 100
    assert isinstance(int_suggestion, int)


def test_sample_independent_int_loguniform_distributions() -> None:
    """Test sampling from int distribution returns integer."""

    experiment = opts.create_experiment()

    def int_value_fn(idx: int) -> float:
        random.seed(idx)
        return random.randint(0, 100)

    intlog_dist = opts.samples.IntLogUniformDistribution(1, 100)
    past_trials = [
        frozen_trial_factory(i, dist=intlog_dist, value_fn=int_value_fn) for i in range(1, 8)
    ]
    trial = frozen_trial_factory(8)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        intlog_suggestion = sampler.sample_independent(experiment, trial, "param-a", intlog_dist)
    assert 1 <= intlog_suggestion <= 100
    assert isinstance(intlog_suggestion, int)


@pytest.mark.parametrize(
    "state",
    [
        (opts.trial.TrialState.FAIL,),
        (opts.trial.TrialState.STOP,),
        (opts.trial.TrialState.RUNNING,),
        (opts.trial.TrialState.WAITING,),
    ],
)
def test_sample_independent_handle_unsuccessful_states(state: opts.trial.TrialState) -> None:
    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)

    # Prepare sampling result for later tests.
    past_trials = [frozen_trial_factory(i, dist=dist) for i in range(1, 30)]
    trial = frozen_trial_factory(30)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        all_success_suggestion = sampler.sample_independent(experiment, trial, "param-a", dist)

    # Test unsuccessful trials are handled differently.
    state_fn = build_state_fn(state)
    past_trials = [frozen_trial_factory(i, dist=dist, state_fn=state_fn) for i in range(1, 30)]
    trial = frozen_trial_factory(30)
    sampler = TPESampler(n_startup_trials=5, seed=0)
    with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
        partial_unsuccessful_suggestion = sampler.sample_independent(experiment, trial, "param-a", dist)
    assert partial_unsuccessful_suggestion != all_success_suggestion


def test_sample_independent_ignored_states() -> None:
    """Tests FAIL, RUNNING, and WAITING states are equally."""

    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)

    suggestions = []
    for state in [
        opts.trial.TrialState.FAIL,
        opts.trial.TrialState.RUNNING,
        opts.trial.TrialState.WAITING,
    ]:
        state_fn = build_state_fn(state)
        past_trials = [frozen_trial_factory(i, dist=dist, state_fn=state_fn) for i in range(1, 30)]
        trial = frozen_trial_factory(30)
        sampler = TPESampler(n_startup_trials=5, seed=0)
        with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
            suggestions.append(sampler.sample_independent(experiment, trial, "param-a", dist))

    assert len(set(suggestions)) == 1


def test_sample_independent_stop_state() -> None:
    """Tests Stop state is treated differently from both FAIL and COMPLETE."""

    experiment = opts.create_experiment()
    dist = opts.samples.UniformDistribution(1.0, 100.0)

    suggestions = []
    for state in [
        opts.trial.TrialState.COMPLETE,
        opts.trial.TrialState.FAIL,
        opts.trial.TrialState.STOP,
    ]:
        state_fn = build_state_fn(state)
        past_trials = [frozen_trial_factory(i, dist=dist, state_fn=state_fn) for i in range(1, 30)]
        trial = frozen_trial_factory(30)
        sampler = TPESampler(n_startup_trials=5, seed=0)
        with patch.object(experiment._storage, "get_all_trials", return_value=past_trials):
            suggestions.append(sampler.sample_independent(experiment, trial, "param-a", dist))

    assert len(set(suggestions)) == 3


def test_get_observation_pairs() -> None:
    def objective(trial: Trial) -> float:

        x = trial.suggest_int("x", 5, 5)
        if trial.number == 0:
            return x
        elif trial.number == 1:
            trial.report(1, 4)
            trial.report(2, 7)
            raise TrialStop()
        elif trial.number == 2:
            trial.report(float("nan"), 3)
            raise TrialStop()
        elif trial.number == 3:
            raise TrialStop()
        else:
            raise RuntimeError()

    # Test direction=minimize.
    experiment = opts.create_experiment(direction="minimize")
    experiment.optimize(objective, n_trials=5, catch=(RuntimeError,))

    assert _tpe.sampler._get_observation_pairs(experiment, "x") == (
        [5.0, 5.0, 5.0, 5.0],
        [
            (-float("inf"), 5.0),  # COMPLETE
            (-7, 2),  # Stop (with intermediate values)
            (-3, float("inf")),  # Stop (with a NaN intermediate value; it's treated as infinity)
            (float("inf"), 0.0),  # Stop (without intermediate values)
        ],
    )
    assert _tpe.sampler._get_observation_pairs(experiment, "y") == (
        [None, None, None, None],
        [
            (-float("inf"), 5.0),  # COMPLETE
            (-7, 2),  # Stop (with intermediate values)
            (-3, float("inf")),  # Stop (with a NaN intermediate value; it's treated as infinity)
            (float("inf"), 0.0),  # Stop (without intermediate values)
        ],
    )

    # Test direction=maximize.
    experiment = opts.create_experiment(direction="maximize")
    experiment.optimize(objective, n_trials=4)
    experiment._storage.create_new_trial(experiment._experiment_id)  # Create a running trial.

    assert _tpe.sampler._get_observation_pairs(experiment, "x") == (
        [5.0, 5.0, 5.0, 5.0],
        [
            (-float("inf"), -5.0),  # COMPLETE
            (-7, -2),  # Stop (with intermediate values)
            (-3, float("inf")),  # Stop (with a NaN intermediate value; it's treated as infinity)
            (float("inf"), 0.0),  # Stop (without intermediate values)
        ],
    )
    assert _tpe.sampler._get_observation_pairs(experiment, "y") == (
        [None, None, None, None],
        [
            (-float("inf"), -5.0),  # COMPLETE
            (-7, -2),  # Stop (with intermediate values)
            (-3, float("inf")),  # Stop (with a NaN intermediate value; it's treated as infinity)
            (float("inf"), 0.0),  # Stop (without intermediate values)
        ],
    )


def test_get_multivariate_observation_pairs() -> None:
    def objective(trial: Trial) -> float:

        x = trial.suggest_int("x", 5, 5)
        y = trial.suggest_int("y", 6, 6)
        if trial.number == 0:
            return x + y
        elif trial.number == 1:
            trial.report(1, 4)
            trial.report(2, 7)
            raise TrialStop()
        elif trial.number == 2:
            trial.report(float("nan"), 3)
            raise TrialStop()
        elif trial.number == 3:
            raise TrialStop()
        else:
            raise RuntimeError()

    # Test direction=minimize.
    experiment = opts.create_experiment(direction="minimize")
    experiment.optimize(objective, n_trials=5, catch=(RuntimeError,))

    assert _tpe.sampler._get_multivariate_observation_pairs(experiment, ["x", "y"]) == (
        {"x": [5.0, 5.0, 5.0, 5.0], "y": [6.0, 6.0, 6.0, 6.0]},
        [
            (-float("inf"), 11.0),  # COMPLETE
            (-7, 2),  # PRUNED (with intermediate values)
            (-3, float("inf")),  # PRUNED (with a NaN intermediate value; it's treated as infinity)
            (float("inf"), 0.0),  # PRUNED (without intermediate values)
        ],
    )

    # Test direction=maximize.
    experiment = opts.create_experiment(direction="maximize")
    experiment.optimize(objective, n_trials=4)
    experiment._storage.create_new_trial(experiment._experiment_id)  # Create a running trial.

    assert _tpe.sampler._get_multivariate_observation_pairs(experiment, ["x", "y"]) == (
        {"x": [5.0, 5.0, 5.0, 5.0], "y": [6.0, 6.0, 6.0, 6.0]},
        [
            (-float("inf"), -11.0),  # COMPLETE
            (-7, -2),  # PRUNED (with intermediate values)
            (-3, float("inf")),  # PRUNED (with a NaN intermediate value; it's treated as infinity)
            (float("inf"), 0.0),  # PRUNED (without intermediate values)
        ],
    )


def frozen_trial_factory(
    idx: int,
    dist: opts.samples.BaseDistribution = opts.samples.UniformDistribution(
        1.0, 100.0
    ),
    state_fn: Callable[
        [int], opts.trial.TrialState
    ] = lambda _: opts.trial.TrialState.COMPLETE,
    value_fn: Optional[Callable[[int], Union[int, float]]] = None,
    target_fn: Callable[[float], float] = lambda val: (val - 20.0) ** 2,
    interm_val_fn: Callable[[int], Dict[int, float]] = lambda _: {},
) -> opts.trial.FrozenTrial:
    if value_fn is None:
        random.seed(idx)
        value = random.random() * 99.0 + 1.0
    else:
        value = value_fn(idx)
    return opts.trial.FrozenTrial(
        number=idx,
        state=state_fn(idx),
        value=target_fn(value),
        datetime_start=None,
        datetime_complete=None,
        params={"param-a": value},
        distributions={"param-a": dist},
        user_attrs={},
        system_attrs={},
        intermediate_values=interm_val_fn(idx),
        trial_id=idx + 123,
    )


def build_state_fn(state: opts.trial.TrialState) -> Callable[[int], opts.trial.TrialState]:
    def state_fn(idx: int) -> opts.trial.TrialState:
        return [opts.trial.TrialState.COMPLETE, state][idx % 2]

    return state_fn


def test_reseed_rng() -> None:
    sampler = TPESampler()
    original_seed = sampler._rng.seed

    with patch.object(
        sampler._random_sampler, "reseed_rng", wraps=sampler._random_sampler.reseed_rng
    ) as mock_object:
        sampler.reseed_rng()
        assert mock_object.call_count == 1
        assert original_seed != sampler._rng.seed
