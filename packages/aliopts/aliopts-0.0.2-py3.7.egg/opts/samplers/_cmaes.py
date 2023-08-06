"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/10 10:09 上午
@Software: PyCharm
@File    : _cmaes.py
@E-mail  : victor.xsyang@gmail.com
"""
import copy
import math
import pickle
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
import warnings

from cmaes import CMA
import numpy as np

import opts
from opts import logger
from opts._experiment_direction import ExperimentDirection
from opts.samples import BaseDistribution
from opts.errors import ExperimentalWarning
from opts.samplers import BaseSampler
from opts.trial import FrozenTrial
from opts.trial import TrialState
from opts.experiment import Experiment

_logger = logger.get_logger(__name__)

_EPS = 1e-10

_SYSTEM_ATTR_MAX_LENGTH = 2045


class CmaEsSampler(BaseSampler):
    """A Sampler using CMA-ES algorithm.

    """

    def __init__(
            self,
            x0: Optional[Dict[str, Any]] = None,
            sigma0: Optional[float] = None,
            n_startup_trials: int = 1,
            independent_sampler: Optional[BaseSampler] = None,
            warn_independent_sampling: bool = True,
            seed: Optional[int] = None,
            *,
            consider_stop_trials: bool = False,
            restart_strategy: Optional[str] = None,
            inc_popsize: int = 2
    ) -> None:
        self._x0 = x0
        self._sigma0 = sigma0
        self._independent_sampler = independent_sampler or opts.samplers.RandomSampler(seed=seed)
        self._n_startup_trials = n_startup_trials
        self._warn_independent_sampling = warn_independent_sampling
        self._cma_rng = np.random.RandomState(seed)
        self._search_space = opts.samplers.IntersectionSearchSpace()
        self._consider_stop_trials = consider_stop_trials
        self._restart_strategy = restart_strategy
        self._inc_popsize = inc_popsize

        if self._restart_strategy:
            warnings.warn(
                "`restart_strategy` option is an experiment feature."
                " The interface can change in the feature.",
                ExperimentalWarning,
            )

        if self._consider_stop_trials:
            warnings.warn(
                "`consider_stop_trials` option is an experimental feature."
                "The interface can change in the feature.",
                ExperimentalWarning
            )

        if restart_strategy not in (
                "ipop",
                None
        ):
            raise ValueError(
                "restart_strategy = {} is unsupported. Please specify: 'ipop' or None.".format(
                    restart_strategy
                )
            )

    def reseed_rng(self) -> None:
        self._independent_sampler.reseed_rng()

    def infer_relative_search_space(
            self, experiment: "opts.Experiment",
            trial: "opts.trial.FrozenTrial") -> Dict[str, BaseDistribution]:
        search_space: Dict[str, BaseDistribution] = {}
        for name, distribution in self._search_space.calculate(experiment).items():
            if distribution.single():
                continue

            if not isinstance(
                    distribution,
                    (
                            opts.samples.UniformDistribution,
                            opts.samples.LogUniformDistribution,
                            opts.samples.DiscreteUniformDistribution,
                            opts.samples.IntUniformDistribution,
                            opts.samples.IntLogUniformDistribution
                    ),
            ):
                continue
            search_space[name] = distribution
        return search_space

    def sample_relative(
            self, experiment: "opts.Experiment", trial: "opts.trial.FrozenTrial",
            search_space: Dict[str, BaseDistribution]
    ) -> Dict[str, Any]:
        if len(search_space) == 0:
            return {}

        completed_trials = self._get_trials(experiment)
        if len(completed_trials) < self._n_startup_trials:
            return {}

        if len(search_space) == 1:
            _logger.info(
                "`CmaEsSampler` only supports two or more dimensional continuous "
                "search space. `{}` is used instead of `CmaEsSampler`.".format(
                    self._independent_sampler.__class__.__name__
                )
            )
            self._warn_independent_sampling = False
            return {}

        ordered_keys = [key for key in search_space]
        ordered_keys.sort()

        optimizer, n_restarts = self._restore_optimizer(completed_trials)
        if optimizer is None:
            n_restarts = 0
            optimizer = self._init_optimizer(search_space, ordered_keys)

        if self._restart_strategy is None:
            generation_attr_key = "cma:generation"
        else:
            generation_attr_key = "cma:restart_{}:generation".format(n_restarts)

        if optimizer.dim != len(ordered_keys):
            _logger.info(
                "`CmaEsSampler` does not support dynamic search space."
                "`{}` is used instead of `CmaEsSampler`.".format(
                    self._independent_sampler.__class__.__name__
                )
            )
            self._warn_independent_sampling = False
            return {}
        solution_trials = [
            t
            for t in completed_trials
            if optimizer.generation == t.system_attrs.get(generation_attr_key, -1)
        ]
        if len(solution_trials) >= optimizer.population_size:
            solutions: List[Tuple[np.ndarray, float]] = []
            for t in solution_trials[: optimizer.population_size]:
                assert t.value is not None, "completed trials must have a value"
                x = np.array(
                    [
                        _to_cma_param(search_space[k], t.params[k]) for k in ordered_keys
                    ],
                    dtype=float
                )
                y = t.value if experiment.direction == ExperimentDirection.MINIMIZE else -t.value
                solutions.append((x, y))

            optimizer.tell(solutions)

            if self._restart_strategy == "ipop" and optimizer.should_stop():
                n_restarts += 1
                generation_attr_key = "cma:restart_{}:generation".format(n_restarts)
                popsize = optimizer.population_size * self._inc_popsize
                optimizer = self._init_optimizer(
                    search_space, ordered_keys, population_size=popsize, randomize_start_point=True
                )

            # Store optimizer
            optimizer_str = pickle.dumps(optimizer).hex()
            optimizer_attrs = _split_optimizer_str(optimizer_str)
            for key in optimizer_attrs:
                experiment._storage.set_trial_system_attr(trial._trial_id, key, optimizer_attrs[key])

        seed = self._cma_rng.randint(1, 2 ** 16) + trial.number
        optimizer._rng = np.random.RandomState(seed)
        params = optimizer.ask()

        experiment._storage.set_trial_system_attr(
            trial._trial_id,
            generation_attr_key,
            optimizer.generation
        )
        experiment._storage.set_trial_system_attr(
            trial._trial_id,
            "cma:n_restarts",
            n_restarts
        )
        external_values = {
            k: _to_opts_param(search_space[k], p) for k, p in zip(ordered_keys, params)
        }
        return external_values

    def _init_optimizer(
        self,
        search_space: Dict[str, BaseDistribution],
        ordered_keys: List[str],
        population_size: Optional[int] = None,
        randomize_start_point: bool = False,
    ) -> CMA:
        if randomize_start_point:
            # `_initialize_x0_randomly ` returns internal representations.
            x0 = _initialize_x0_randomly(self._cma_rng, search_space)
            mean = np.array([x0[k] for k in ordered_keys], dtype=float)
        elif self._x0 is None:
            # `_initialize_x0` returns internal representations.
            x0 = _initialize_x0(search_space)
            mean = np.array([x0[k] for k in ordered_keys], dtype=float)
        else:
            # `self._x0` is external representations.
            mean = np.array(
                [_to_cma_param(search_space[k], self._x0[k]) for k in ordered_keys], dtype=float
            )

        if self._sigma0 is None:
            sigma0 = _initialize_sigma0(search_space)
        else:
            sigma0 = self._sigma0

        # Avoid ZeroDivisionError in cmaes.
        sigma0 = max(sigma0, _EPS)
        bounds = _get_search_space_bound(ordered_keys, search_space)
        n_dimension = len(ordered_keys)
        return CMA(
            mean=mean,
            sigma=sigma0,
            bounds=bounds,
            seed=self._cma_rng.randint(1, 2 ** 31 - 2),
            n_max_resampling=10 * n_dimension,
            population_size=population_size,
        )

    def _restore_optimizer(
            self,
            completed_trials: "List[opts.trial.FrozenTrial]",
    ) -> Tuple[Optional[CMA], int]:
        for trial in reversed(completed_trials):
            optimizer_attrs = {
                key: value
                for key, value in trial.system_attrs.items()
                if key.startswith("cma:optimizer")
            }
            if len(optimizer_attrs) == 0:
                continue

            optimizer_str = optimizer_attrs.get("cma:optimizer", None)
            if optimizer_str is None:
                optimizer_str = _concat_optimizer_attrs(optimizer_attrs)

            n_restarts: int = trial.system_attrs.get("cma:n_restarts", 0)
            return pickle.loads(bytes.fromhex(optimizer_str)), n_restarts
        return None, 0

    def _init_optimœizer(
            self,
            search_space: Dict[str, BaseDistribution],
            ordered_keys: List[str],
            population_size: Optional[int] = None,
            randomize_start_point: bool = False
    ) -> CMA:
        if randomize_start_point:
            x0 = _initialize_x0_randomly(self._cma_rng, search_space)
            mean = np.array([x0[k] for k in ordered_keys], dtype=float)
        elif self._x0 is None:
            x0 = _initialize_x0(search_space)
            mean = np.array([x0[k] for k in ordered_keys], dtype=float)
        else:
            mean = np.array(
                [_to_cma_param(search_space[k], self._x0[k]) for k in ordered_keys], dtype=float
            )
        if self._sigma0 is None:
            sigma0 = _initialize_sigma0(search_space)
        else:
            sigma0 = self._sigma0

        # Avoid ZeroDivisionError in cmaes.
        sigma0 = max(sigma0, _EPS)
        bounds = _get_search_space_bound(ordered_keys, search_space)
        n_dimension = len(ordered_keys)
        return CMA(
            mean=mean,
            sigma=sigma0,
            bounds=bounds,
            seed=self._cma_rng.randint(1, 2 ** 31 - 2),
            n_max_resampling=10 * n_dimension,
            population_size=population_size
        )

    def sample_independent(
            self,
            experiment: "opts.Experiment",
            trial: "opts.trial.FrozenTrial",
            param_name: str,
            param_distribution: BaseDistribution
                           ) -> Any:
        if self._warn_independent_sampling:
            complete_trials = self._get_trials(experiment)
            if len(complete_trials) > self._n_startup_trials:
                self._log_independent_sampling(trial, param_name)

        return self._independent_sampler.sample_independent(
            experiment, trial, param_name, param_distribution
        )

    def _log_independent_sampling(self, trial: FrozenTrial, param_name: str) -> None:
        _logger.warning(
            "The parameter '{}' in trial#{} is sampled independently "
            "by using `{}` instead of `CmaEsSampler` "
            "(optimization performance may be degraded). "
            "`CmaEsSampler` does not support dynamic search space or `CategoricalDistribution`. "
            "You can suppress this warning by setting `warn_independent_sampling` "
            "to `False` in the constructor of `CmaEsSampler`, "
            "if this independent sampling is intended behavior.".format(
                param_name, trial.number, self._independent_sampler.__class__.__name__
            )
        )

    def _get_trials(self, experiment: "opts.Experiment") -> List[FrozenTrial]:
        complete_trial = []
        for t in experiment.get_trials(deepcopy=False):
            if t.state == TrialState.COMPLETE:
                complete_trial.append(t)
            elif (
                t.state == TrialState.STOP
                and len(t.intermediate_values) > 0
                and self._consider_stop_trials
            ):
                _, value = max(t.intermediate_values.items())
                if value is None:
                    continue
                copied_t = copy.deepcopy(t)
                copied_t.value = value
                complete_trial.append(copied_t)
        return complete_trial




def _concat_optimizer_attrs(optimizer_attrs: Dict[str, str]) -> str:
    return "".join(
        optimizer_attrs["cma:optimizer:{}".format(i)] for i in range(len(optimizer_attrs))
    )


def _initialize_x0_randomly(
        rng: np.random.RandomState, search_space: Dict[str, BaseDistribution]
) -> Dict[str, float]:
    x0 = {}
    for name, distribution in search_space.items():
        if isinstance(
                distribution,
                (
                        opts.samples.UniformDistribution,
                        opts.samples.DiscreteUniformDistribution,
                        opts.samples.IntLogUniformDistribution
                ),
        ):
            x0[name] = distribution.low + rng.rand() * (distribution.high - distribution.low)
        elif isinstance(
                distribution,
                (
                        opts.samples.IntLogUniformDistribution,
                        opts.samples.LogUniformDistribution
                ),
        ):
            log_high = math.log(distribution.high)
            log_low = math.log(distribution.low)
            x0[name] = log_low + rng.rand() * (log_high - log_low)
        else:
            raise NotImplementedError(
                "The distribution {} is not implemented.".format(distribution)
            )
    return x0


def _initialize_x0(search_space: Dict[str, BaseDistribution]) -> Dict[str, float]:
    x0 = {}
    for name, distribution in search_space.items():
        if isinstance(
                distribution,
                (
                        opts.samples.UniformDistribution,
                        opts.samples.DiscreteUniformDistribution,
                        opts.samples.IntUniformDistribution
                )
        ):
            x0[name] = distribution.low + (distribution.high - distribution.low) / 2
        elif isinstance(
                distribution,
                (
                        opts.samples.LogUniformDistribution,
                        opts.samples.IntLogUniformDistribution
                ),
        ):
            log_high = math.log(distribution.high)
            log_low = math.log(distribution.low)
            x0[name] = log_low + (log_high - log_low) / 2
        else:
            raise NotImplementedError(
                "The distribution {} is not implemented.".format(distribution)
            )
    return x0


def _to_cma_param(distribution: BaseDistribution, opts_param: Any) -> float:
    if isinstance(
            distribution, opts.samples.LogUniformDistribution
    ):
        return math.log(opts_param)
    if isinstance(distribution, opts.samples.IntUniformDistribution):
        return float(opts_param)

    if isinstance(distribution, opts.samples.IntLogUniformDistribution):
        return math.log(opts_param)
    return opts_param


def _initialize_sigma0(search_space: Dict[str, BaseDistribution]) -> float:
    sigma0 = []
    for name, distribution in search_space.items():
        if isinstance(distribution, opts.samples.UniformDistribution):
            sigma0.append((distribution.high - distribution.low) / 6)
        elif isinstance(distribution, opts.samples.DiscreteUniformDistribution):
            sigma0.append((distribution.high - distribution.low) / 6)
        elif isinstance(distribution, opts.samples.IntUniformDistribution):
            sigma0.append((distribution.high - distribution.low) / 6)
        elif isinstance(distribution, opts.samples.IntLogUniformDistribution):
            log_high = math.log(distribution.high)
            log_low = math.log(distribution.low)
            sigma0.append((log_high - log_low) / 6)
        elif isinstance(distribution, opts.samples.LogUniformDistribution):
            log_high = math.log(distribution.high)
            log_low = math.log(distribution.low)
            sigma0.append((log_high - log_low) / 6)
        else:
            raise NotImplementedError(
                "The distribution {} is not implemented.".format(distribution)
            )
    return min(sigma0)


def _get_search_space_bound(
        keys: List[str], search_space: Dict[str, BaseDistribution]
) -> np.ndarray:
    bounds = []
    for param_name in keys:
        dist = search_space[param_name]
        if isinstance(
                dist,
                (
                        opts.samples.UniformDistribution,
                        opts.samples.LogUniformDistribution
                ),
        ):
            bounds.append([_to_cma_param(dist, dist.low), _to_cma_param(dist, dist.high) - _EPS])
        elif isinstance(
                dist,
                (
                        opts.samples.DiscreteUniformDistribution,
                        opts.samples.IntUniformDistribution,
                        opts.samples.IntLogUniformDistribution
                )
        ):
            bounds.append([_to_cma_param(dist, dist.low), _to_cma_param(dist, dist.high)])
        else:
            raise NotImplementedError("The distribution {} is not implemented.".format(dist))
    return np.array(bounds, dtype=float)


def _split_optimizer_str(optimizer_str: str) -> Dict[str, str]:
    optimizer_len = len(optimizer_str)
    attrs = {}
    for i in range(math.ceil(optimizer_len / _SYSTEM_ATTR_MAX_LENGTH)):
        start = i * _SYSTEM_ATTR_MAX_LENGTH
        end = min((i + 1) * _SYSTEM_ATTR_MAX_LENGTH, optimizer_len)
        attrs["cma:optimizer:{}".format(i)] = optimizer_str[start:end]
    return attrs


def _to_opts_param(distribution: BaseDistribution, cma_param: float) -> Any:
    if isinstance(distribution, opts.samples.LogUniformDistribution):
        return math.exp(cma_param)
    if isinstance(distribution, opts.samples.DiscreteUniformDistribution):
        v = np.round(cma_param / distribution.q) * distribution.q + distribution.low
        return float(min(max(v, distribution.low), distribution.high))
    if isinstance(distribution, opts.samples.IntUniformDistribution):
        r = np.round((cma_param - distribution.low) / distribution.step)
        v = r * distribution.step + distribution.low
        return int(v)
    if isinstance(distribution, opts.samples.IntLogUniformDistribution):
        r = np.round(cma_param - math.log(distribution.low))
        v = r + math.log(distribution.low)
        return int(math.exp(v))
    return cma_param
