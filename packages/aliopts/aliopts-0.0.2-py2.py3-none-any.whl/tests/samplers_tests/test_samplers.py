"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/27 6:21 下午
@Software: PyCharm
@File    : test_samplers.py
@E-mail  : victor.xsyang@gmail.com
"""
from collections import OrderedDict
import pickle
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Sequence
import warnings

import numpy as np
import pytest

import opts
from opts.samples import BaseDistribution
from opts.samples import CategoricalChoiceType
from opts.samples import CategoricalDistribution
from opts.samples import DiscreteUniformDistribution
from opts.samples import IntUniformDistribution
from opts.samples import LogUniformDistribution
from opts.samples import UniformDistribution
from opts.samplers import BaseSampler
from opts.samplers import PartialFixedSampler
from opts.experiment import Experiment
from opts.testing.storage import StorageSupplier
from opts.trial import FrozenTrial
from opts.trial import Trial

parametrize_sampler = pytest.mark.parametrize(
    "sampler_class",
    [
        opts.samplers.RandomSampler,
        lambda: opts.samplers.TPESampler(n_startup_trials=0),
        lambda: opts.samplers.TPESampler(n_startup_trials=0, multivariate=True),
        lambda: opts.samplers.CmaEsSampler(n_startup_trials=0),
        lambda: opts.frameworks.SkoptSampler(skopt_kwargs={"n_initial_points": 1}),
        lambda: opts.frameworks.PyCmaSampler(n_startup_trials=0),
    ],
)

@pytest.mark.parametrize("seed", [None, 0, 169208])
def test_pickle_random_sampler(seed: Optional[int]) -> None:

    sampler = opts.samplers.RandomSampler(seed)
    restored_sampler = pickle.loads(pickle.dumps(sampler))
    assert sampler._rng.bytes(10) == restored_sampler._rng.bytes(10)


def test_random_sampler_reseed_rng() -> None:
    sampler = opts.samplers.RandomSampler()
    original_seed = sampler._rng.seed

    sampler.reseed_rng()
    assert original_seed != sampler._rng.seed


@parametrize_sampler
@pytest.mark.parametrize(
    "distribution",
    [
        UniformDistribution(-1.0, 1.0),
        UniformDistribution(0.0, 1.0),
        UniformDistribution(-1.0, 0.0),
    ],
)
def test_uniform(
    sampler_class: Callable[[], BaseSampler], distribution: UniformDistribution
) -> None:

    experiment = opts.experiment.create_experiment(sampler=sampler_class())
    points = np.array(
        [
            experiment.sampler.sample_independent(experiment, _create_new_trial(experiment), "x", distribution)
            for _ in range(100)
        ]
    )
    assert np.all(points >= distribution.low)
    assert np.all(points < distribution.high)
    assert not isinstance(
        experiment.sampler.sample_independent(experiment, _create_new_trial(experiment), "x", distribution),
        np.floating,
    )

def _create_new_trial(experiment: Experiment) -> FrozenTrial:

    trial_id = experiment._storage.create_new_trial(experiment._experiment_id)
    return experiment._storage.get_trial(trial_id)


@parametrize_sampler
@pytest.mark.parametrize("distribution", [LogUniformDistribution(1e-7, 1.0)])
def test_log_uniform(
    sampler_class: Callable[[], BaseSampler], distribution: LogUniformDistribution
) -> None:

    experiment = opts.experiment.create_experiment(sampler=sampler_class())
    points = np.array(
        [
            experiment.sampler.sample_independent(experiment, _create_new_trial(experiment), "x", distribution)
            for _ in range(100)
        ]
    )
    assert np.all(points >= distribution.low)
    assert np.all(points < distribution.high)
    assert not isinstance(
        experiment.sampler.sample_independent(experiment, _create_new_trial(experiment), "x", distribution),
        np.floating,
    )


@parametrize_sampler
@pytest.mark.parametrize(
    "distribution",
    [DiscreteUniformDistribution(-10, 10, 0.1), DiscreteUniformDistribution(-10.2, 10.2, 0.1)],
)
def test_discrete_uniform(
    sampler_class: Callable[[], BaseSampler], distribution: DiscreteUniformDistribution
) -> None:

    experiment = opts.experiment.create_experiment(sampler=sampler_class())
    points = np.array(
        [
            experiment.sampler.sample_independent(experiment, _create_new_trial(experiment), "x", distribution)
            for _ in range(1)
        ]
    )
    assert np.all(points >= distribution.low)
    assert np.all(points <= distribution.high)
    assert not isinstance(
        experiment.sampler.sample_independent(experiment, _create_new_trial(experiment), "x", distribution),
        np.floating,
    )

    # Check all points are multiples of distribution.q.
    points = points
    points -= distribution.low

    points /= distribution.q
    round_points = np.round(points)
    np.testing.assert_almost_equal(round_points, points)


@parametrize_sampler
@pytest.mark.parametrize(
    "distribution",
    [
        IntUniformDistribution(-10, 10),
        IntUniformDistribution(0, 10),
        IntUniformDistribution(-10, 0),
        IntUniformDistribution(-10, 10, 2),
        IntUniformDistribution(0, 10, 2),
        IntUniformDistribution(-10, 0, 2),
    ],
)
def test_int(
    sampler_class: Callable[[], BaseSampler], distribution: IntUniformDistribution
) -> None:

    experiment = opts.experiment.create_experiment(sampler=sampler_class())
    points = np.array(
        [
            experiment.sampler.sample_independent(experiment, _create_new_trial(experiment), "x", distribution)
            for _ in range(100)
        ]
    )
    assert np.all(points >= distribution.low)
    assert np.all(points <= distribution.high)
    assert not isinstance(
        experiment.sampler.sample_independent(experiment, _create_new_trial(experiment), "x", distribution),
        np.integer,
    )

@parametrize_sampler
@pytest.mark.parametrize("choices", [(1, 2, 3), ("a", "b", "c"), (1, "a")])
def test_categorical(
    sampler_class: Callable[[], BaseSampler], choices: Sequence[CategoricalChoiceType]
) -> None:

    distribution = CategoricalDistribution(choices)

    experiment = opts.experiment.create_experiment(sampler=sampler_class())

    def sample() -> float:

        trial = _create_new_trial(experiment)
        param_value = experiment.sampler.sample_independent(experiment, trial, "x", distribution)
        return distribution.to_internal_repr(param_value)

    points = np.array([sample() for _ in range(100)])

    # 'x' value is corresponding to an index of distribution.choices.
    assert np.all(points >= 0)
    assert np.all(points <= len(distribution.choices) - 1)
    round_points = np.round(points)
    np.testing.assert_almost_equal(round_points, points)


class FixedSampler(BaseSampler):
    def __init__(
        self,
        relative_search_space: Dict[str, BaseDistribution],
        relative_params: Dict[str, Any],
        unknown_param_value: Any,
    ) -> None:

        self.relative_search_space = relative_search_space
        self.relative_params = relative_params
        self.unknown_param_value = unknown_param_value

    def infer_relative_search_space(
        self, experiment: Experiment, trial: FrozenTrial
    ) -> Dict[str, BaseDistribution]:

        return self.relative_search_space

    def sample_relative(
        self, experiment: Experiment, trial: FrozenTrial, search_space: Dict[str, BaseDistribution]
    ) -> Dict[str, Any]:

        return self.relative_params

    def sample_independent(
        self,
        experiment: Experiment,
        trial: FrozenTrial,
        param_name: str,
        param_distribution: BaseDistribution,
    ) -> Any:

        return self.unknown_param_value

def test_sample_relative() -> None:

    relative_search_space: Dict[str, BaseDistribution] = {
        "a": UniformDistribution(low=0, high=5),
        "b": CategoricalDistribution(choices=("foo", "bar", "baz")),
        "c": IntUniformDistribution(low=20, high=50),  # Not exist in `relative_params`.
    }
    relative_params = {
        "a": 3.2,
        "b": "baz",
    }
    unknown_param_value = 30

    sampler = FixedSampler(  # type: ignore
        relative_search_space, relative_params, unknown_param_value
    )
    experiment = opts.experiment.create_experiment(sampler=sampler)

    def objective(trial: Trial) -> float:

        # Predefined parameters are sampled by `sample_relative()` method.
        assert trial.suggest_uniform("a", 0, 5) == 3.2
        assert trial.suggest_categorical("b", ["foo", "bar", "baz"]) == "baz"

        # Other parameters are sampled by `sample_independent()` method.
        assert trial.suggest_int("c", 20, 50) == unknown_param_value
        assert trial.suggest_loguniform("d", 1, 100) == unknown_param_value
        assert trial.suggest_uniform("e", 20, 40) == unknown_param_value

        return 0.0

    experiment.optimize(objective, n_trials=10, catch=())
    for trial in experiment.trials:
        assert trial.params == {"a": 3.2, "b": "baz", "c": 30, "d": 30, "e": 30}

def test_intersection_search_space() -> None:
    search_space = opts.samplers.IntersectionSearchSpace()
    experiment = opts.create_experiment()

    # No trial.
    assert search_space.calculate(experiment) == {}
    assert search_space.calculate(experiment) == opts.samplers.intersection_search_space(experiment)

    # First trial.
    experiment.optimize(lambda t: t.suggest_uniform("y", -3, 3) + t.suggest_int("x", 0, 10), n_trials=1)
    assert search_space.calculate(experiment) == {
        "x": IntUniformDistribution(low=0, high=10),
        "y": UniformDistribution(low=-3, high=3),
    }
    assert search_space.calculate(experiment) == opts.samplers.intersection_search_space(experiment)

    # Returning sorted `OrderedDict` instead of `dict`.
    assert search_space.calculate(experiment, ordered_dict=True) == OrderedDict(
        [
            ("x", IntUniformDistribution(low=0, high=10)),
            ("y", UniformDistribution(low=-3, high=3)),
        ]
    )
    assert search_space.calculate(
        experiment, ordered_dict=True
    ) == opts.samplers.intersection_search_space(experiment, ordered_dict=True)

    # Second trial (only 'y' parameter is suggested in this trial).
    experiment.optimize(lambda t: t.suggest_uniform("y", -3, 3), n_trials=1)
    assert search_space.calculate(experiment) == {"y": UniformDistribution(low=-3, high=3)}
    assert search_space.calculate(experiment) == opts.samplers.intersection_search_space(experiment)

    # Failed or pruned trials are not considered in the calculation of
    # an intersection search space.
    def objective(trial: Trial, exception: Exception) -> float:

        trial.suggest_uniform("z", 0, 1)
        raise exception

    experiment.optimize(lambda t: objective(t, RuntimeError()), n_trials=1, catch=(RuntimeError,))
    experiment.optimize(lambda t: objective(t, opts.TrialStop()), n_trials=1)
    assert search_space.calculate(experiment) == {"y": UniformDistribution(low=-3, high=3)}
    assert search_space.calculate(experiment) == opts.samplers.intersection_search_space(experiment)

    # If two parameters have the same name but different distributions,
    # those are regarded as different parameters.
    experiment.optimize(lambda t: t.suggest_uniform("y", -1, 1), n_trials=1)
    assert search_space.calculate(experiment) == {}
    assert search_space.calculate(experiment) == opts.samplers.intersection_search_space(experiment)

    # The search space remains empty once it is empty.
    experiment.optimize(lambda t: t.suggest_uniform("y", -3, 3) + t.suggest_int("x", 0, 10), n_trials=1)
    assert search_space.calculate(experiment) == {}
    assert search_space.calculate(experiment) == opts.samplers.intersection_search_space(experiment)


def test_intersection_search_space_class_with_different_experiments() -> None:
    search_space = opts.samplers.IntersectionSearchSpace()

    with StorageSupplier("sqlite") as storage:
        experiment0 = opts.create_experiment(storage=storage)
        experiment1 = opts.create_experiment(storage=storage)

        search_space.calculate(experiment0)
        with pytest.raises(ValueError):
            # An `IntersectionSearchSpace` instance isn't supposed to be used for multiple studies.
            search_space.calculate(experiment1)

@parametrize_sampler
def test_nan_objective_value(sampler_class: Callable[[], BaseSampler]) -> None:

    experiment = opts.create_experiment(sampler=sampler_class())

    def objective(trial: Trial, base_value: float) -> float:

        return trial.suggest_uniform("x", 0.1, 0.2) + base_value

    # Non NaN objective values.
    for i in range(10, 1, -1):

        experiment.optimize(lambda t: objective(t, i), n_trials=1, catch=())
    assert int(experiment.best_value) == 2

    # NaN objective values.
    experiment.optimize(lambda t: objective(t, float("nan")), n_trials=1, catch=())
    assert int(experiment.best_value) == 2

    # Non NaN objective value.
    experiment.optimize(lambda t: objective(t, 1), n_trials=1, catch=())
    assert int(experiment.best_value) == 1

@parametrize_sampler
def test_partial_fixed_sampling(sampler_class: Callable[[], BaseSampler]) -> None:

    experiment = opts.create_experiment(sampler=sampler_class())

    def objective(trial: Trial) -> float:
        x = trial.suggest_float("x", -1, 1)
        y = trial.suggest_int("y", -1, 1)
        z = trial.suggest_float("z", -1, 1)
        return x + y + z

    # First trial.
    experiment.optimize(objective, n_trials=1)

    # Second trial. Here, the parameter ``y`` is fixed as 0.
    fixed_params = {"y": 0}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", opts.errors.ExperimentalWarning)
        experiment.sampler = PartialFixedSampler(fixed_params, experiment.sampler)
    experiment.optimize(objective, n_trials=1)
    trial_params = experiment.trials[-1].params
    assert trial_params["y"] == fixed_params["y"]