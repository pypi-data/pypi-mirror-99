"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/26 3:26 下午
@Software: PyCharm
@File    : test_cmaes.py
@E-mail  : victor.xsyang@gmail.com
"""
import pickle
from typing import Any
from typing import Dict
from typing import List
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from cmaes import CMA
import numpy as np
import pytest

import opts
from opts import create_trial
from opts.samplers._cmaes import _concat_optimizer_attrs
from opts.samplers._cmaes import _initialize_sigma0
from opts.samplers._cmaes import _initialize_x0
from opts.samplers._cmaes import _initialize_x0_randomly
from opts.samplers._cmaes import _split_optimizer_str
from opts.testing.distribution import UnsupportedDistribution
from opts.testing.sampler import DeterministicRelativeSampler
from opts.trial import FrozenTrial
from opts.trial import TrialState


def test_consider_stopped_trials_experimental_warning() -> None:
    with pytest.warns(opts.errors.ExperimentalWarning):
        opts.samplers.CmaEsSampler(consider_stop_trials=True)


def test_init_cmaes_opts() -> None:
    sampler = opts.samplers.CmaEsSampler(
        x0={"x": 0, "y": 0},
        sigma0=0.1,
        seed=1,
        n_startup_trials=1,
        independent_sampler=DeterministicRelativeSampler({}, {}),
    )
    experiment = opts.create_experiment(sampler=sampler)

    with patch("opts.samplers._cmaes.CMA") as cma_class:
        cma_obj = MagicMock()
        cma_obj.ask.return_value = np.array((-1, -1))
        cma_obj.generation = 0
        cma_obj.population_size = 5
        cma_class.return_value = cma_obj
        experiment.optimize(
            lambda t: t.suggest_uniform("x", -1, 1) + t.suggest_uniform("y", -1, 1), n_trials=2
        )

        assert cma_class.call_count == 1

        _, actual_kwargs = cma_class.call_args
        assert np.array_equal(actual_kwargs["mean"], np.array([0, 0]))
        assert actual_kwargs["sigma"] == 0.1
        assert np.allclose(actual_kwargs["bounds"], np.array([(-1, 1), (-1, 1)]))
        assert actual_kwargs["seed"] == np.random.RandomState(1).randint(1, 2 ** 32)
        assert actual_kwargs["n_max_resampling"] == 10 * 2
        assert actual_kwargs["population_size"] is None


def test_infer_relative_search_space_1d() -> None:
    sampler = opts.samplers.CmaEsSampler()
    experiment = opts.create_experiment(sampler=sampler)

    # The distribution has only one candidate.
    experiment.optimize(lambda t: t.suggest_int("x", 1, 1), n_trials=1)
    assert sampler.infer_relative_search_space(experiment, experiment.best_trial) == {}


def test_sample_relative_1d() -> None:
    independent_sampler = DeterministicRelativeSampler({}, {})
    sampler = opts.samplers.CmaEsSampler(independent_sampler=independent_sampler)
    experiment = opts.create_experiment(sampler=sampler)

    # If search space is one dimensional, the independent sampler is always used.
    with patch.object(
            independent_sampler, "sample_independent", wraps=independent_sampler.sample_independent
    ) as mock_object:
        experiment.optimize(lambda t: t.suggest_int("x", -1, 1), n_trials=2)
        assert mock_object.call_count == 2


def test_sample_relative_n_startup_trials() -> None:
    independent_sampler = DeterministicRelativeSampler({}, {})
    sampler = opts.samplers.CmaEsSampler(
        n_startup_trials=2, independent_sampler=independent_sampler
    )
    experiment = opts.create_experiment(sampler=sampler)

    def objective(t: opts.Trial) -> float:
        value = t.suggest_int("x", -1, 1) + t.suggest_int("y", -1, 1)
        if t.number == 0:
            raise Exception("first trial is failed")
        return float(value)

    # The independent sampler is used for Trial#0 (FAILED), Trial#1 (COMPLETE)
    # and Trial#2 (COMPLETE). The CMA-ES is used for Trial#3 (COMPLETE).
    with patch.object(
            independent_sampler, "sample_independent", wraps=independent_sampler.sample_independent
    ) as mock_independent, patch.object(
        sampler, "sample_relative", wraps=sampler.sample_relative
    ) as mock_relative:
        experiment.optimize(objective, n_trials=4, catch=(Exception,))
        assert mock_independent.call_count == 6  # The objective function has two parameters.
        assert mock_relative.call_count == 4


def test_initialize_x0_with_unsupported_distribution() -> None:
    with pytest.raises(NotImplementedError):
        _initialize_x0({"x": UnsupportedDistribution()})

    with pytest.raises(NotImplementedError):
        _initialize_x0_randomly(np.random.RandomState(1), {"x": UnsupportedDistribution()})


def test_initialize_sigma0_with_unsupported_distribution() -> None:
    with pytest.raises(NotImplementedError):
        _initialize_sigma0({"x": UnsupportedDistribution()})


def test_reseed_rng() -> None:
    sampler = opts.samplers.CmaEsSampler()

    with patch.object(
            sampler._independent_sampler, "reseed_rng", wraps=sampler._independent_sampler.reseed_rng
    ) as mock_object:
        sampler.reseed_rng()
        assert mock_object.call_count == 1


def test_get_trials() -> None:
    with patch("opts.Experiment.get_trials", new=Mock(side_effect=lambda deepcopy: _create_trials())):
        sampler = opts.samplers.CmaEsSampler(consider_stop_trials=False)
        experiment = opts.create_experiment(sampler=sampler)
        trials = sampler._get_trials(experiment)
        assert len(trials) == 1

        sampler = opts.samplers.CmaEsSampler(consider_stop_trials=True)
        experiment = opts.create_experiment(sampler=sampler)
        trials = sampler._get_trials(experiment)
        assert len(trials) == 2
        assert trials[0].value == 1.0
        assert trials[1].value == 2.0


def _create_trials() -> List[FrozenTrial]:
    trials = []
    trials.append(
        FrozenTrial(
            number=0,
            value=1.0,
            state=opts.trial.TrialState.COMPLETE,
            user_attrs={},
            system_attrs={},
            params={},
            distributions={},
            intermediate_values={},
            datetime_start=None,
            datetime_complete=None,
            trial_id=0,
        )
    )
    trials.append(
        FrozenTrial(
            number=1,
            value=None,
            state=opts.trial.TrialState.STOP,
            user_attrs={},
            system_attrs={},
            params={},
            distributions={},
            intermediate_values={0: 2.0},
            datetime_start=None,
            datetime_complete=None,
            trial_id=0,
        )
    )
    return trials

def test_population_size_is_multiplied_when_enable_ipop() -> None:
    inc_popsize = 2
    sampler = opts.samplers.CmaEsSampler(
        x0={"x": 0, "y": 0},
        sigma0=0.1,
        seed=1,
        n_startup_trials=1,
        independent_sampler=DeterministicRelativeSampler({}, {}),
        restart_strategy="ipop",
        inc_popsize=inc_popsize,
    )
    experiment = opts.create_experiment(sampler=sampler)

    def objective(trial: opts.Trial) -> float:
        _ = trial.suggest_uniform("x", -1, 1)
        _ = trial.suggest_uniform("y", -1, 1)
        return 1.0

    with patch("opts.samplers._cmaes.CMA") as cma_class_mock, patch(
        "opts.samplers._cmaes.pickle"
    ) as pickle_mock:
        pickle_mock.dump.return_value = b"serialized object"

        should_stop_mock = MagicMock()
        should_stop_mock.return_value = True

        cma_obj = CMA(
            mean=np.array([-1, -1], dtype=float),
            sigma=1.3,
            bounds=np.array([[-1, 1], [-1, 1]], dtype=float),
        )
        cma_obj.should_stop = should_stop_mock
        cma_class_mock.return_value = cma_obj

        popsize = cma_obj.population_size
        experiment.optimize(objective, n_trials=2 + popsize)
        assert cma_obj.should_stop.call_count == 1

        _, actual_kwargs = cma_class_mock.call_args
        assert actual_kwargs["population_size"] == inc_popsize * popsize

def test_restore_optimizer_keeps_backward_compatibility() -> None:
    sampler = opts.samplers.CmaEsSampler()
    optimizer = CMA(np.zeros(2), sigma=1.3)
    optimizer_str = pickle.dumps(optimizer).hex()

    completed_trials = [
        create_trial(state=TrialState.COMPLETE, value=0.1),
        create_trial(
            state=TrialState.COMPLETE,
            value=0.1,
            system_attrs={"cma:optimizer": optimizer_str, "cma:n_restarts": 1},
        ),
        create_trial(state=TrialState.COMPLETE, value=0.1),
    ]
    optimizer, n_restarts = sampler._restore_optimizer(completed_trials)
    assert isinstance(optimizer, CMA)
    assert n_restarts == 1

    def test_restore_optimizer_keeps_backward_compatibility() -> None:
        sampler = opts.samplers.CmaEsSampler()
        optimizer = CMA(np.zeros(2), sigma=1.3)
        optimizer_str = pickle.dumps(optimizer).hex()

        completed_trials = [
            create_trial(state=TrialState.COMPLETE, value=0.1),
            create_trial(
                state=TrialState.COMPLETE,
                value=0.1,
                system_attrs={"cma:optimizer": optimizer_str, "cma:n_restarts": 1},
            ),
            create_trial(state=TrialState.COMPLETE, value=0.1),
        ]
        optimizer, n_restarts = sampler._restore_optimizer(completed_trials)
        assert isinstance(optimizer, CMA)
        assert n_restarts == 1


def test_restore_optimizer_keeps_backward_compatibility() -> None:
    sampler = opts.samplers.CmaEsSampler()
    optimizer = CMA(np.zeros(2), sigma=1.3)
    optimizer_str = pickle.dumps(optimizer).hex()

    completed_trials = [
        create_trial(state=TrialState.COMPLETE, value=0.1),
        create_trial(
            state=TrialState.COMPLETE,
            value=0.1,
            system_attrs={"cma:optimizer": optimizer_str, "cma:n_restarts": 1},
        ),
        create_trial(state=TrialState.COMPLETE, value=0.1),
    ]
    optimizer, n_restarts = sampler._restore_optimizer(completed_trials)
    assert isinstance(optimizer, CMA)
    assert n_restarts == 1


def test_restore_optimizer_from_substrings() -> None:
    sampler = opts.samplers.CmaEsSampler()
    optimizer = CMA(np.zeros(10), sigma=1.3)
    optimizer_str = pickle.dumps(optimizer).hex()

    system_attrs: Dict[str, Any] = _split_optimizer_str(optimizer_str)
    assert len(system_attrs) > 1
    system_attrs["cma:n_restarts"] = 1

    completed_trials = [
        create_trial(state=TrialState.COMPLETE, value=0.1),
        create_trial(
            state=TrialState.COMPLETE,
            value=0.1,
            system_attrs=system_attrs,
        ),
        create_trial(state=TrialState.COMPLETE, value=0.1),
    ]
    optimizer, n_restarts = sampler._restore_optimizer(completed_trials)
    assert isinstance(optimizer, CMA)
    assert n_restarts == 1

@pytest.mark.parametrize(
    "dummy_optimizer_str,attr_len",
    [
        ("012", 1),
        ("01234", 1),
        ("012345", 2),
    ],
)
def test_split_and_concat_optimizer_string(dummy_optimizer_str: str, attr_len: int) -> None:
    with patch("opts.samplers._cmaes._SYSTEM_ATTR_MAX_LENGTH", 5):
        attrs = _split_optimizer_str(dummy_optimizer_str)
        assert len(attrs) == attr_len
        actual = _concat_optimizer_attrs(attrs)
        assert dummy_optimizer_str == actual
