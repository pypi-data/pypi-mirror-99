"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/27 6:43 下午
@Software: PyCharm
@File    : cma.py
@E-mail  : victor.xsyang@gmail.com
"""
import math
import random
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set

import numpy

import opts
from opts import samples
from opts import logger
from opts._deprecated import deprecated
from opts._imports import try_import
from opts.samples import BaseDistribution
from opts.samples import CategoricalDistribution
from opts.samples import DiscreteUniformDistribution
from opts.samples import IntLogUniformDistribution
from opts.samples import IntUniformDistribution
from opts.samples import LogUniformDistribution
from opts.samples import UniformDistribution
from opts.samplers import BaseSampler
from opts.experiment import Experiment
from opts.experiment import ExperimentDirection
from opts.trial import FrozenTrial
from opts.trial import TrialState

with try_import() as _imports:
    import cma

_logger = logger.get_logger(__name__)

_EPS = 1e-10

class PyCmaSampler(BaseSampler):
    """A Sampler using cma library as the backend.
    """

    def __init__(
        self,
        x0: Optional[Dict[str, Any]] = None,
        sigma0: Optional[float] = None,
        cma_stds: Optional[Dict[str, float]] = None,
        seed: Optional[int] = None,
        cma_opts: Optional[Dict[str, Any]] = None,
        n_startup_trials: int = 1,
        independent_sampler: Optional[BaseSampler] = None,
        warn_independent_sampling: bool = True,
    ) -> None:

        _imports.check()

        self._x0 = x0
        self._sigma0 = sigma0
        self._cma_stds = cma_stds
        if seed is None:
            seed = random.randint(1, 2 ** 32)
        self._cma_opts = cma_opts or {}
        self._cma_opts["seed"] = seed
        self._cma_opts.setdefault("verbose", -2)
        self._n_startup_trials = n_startup_trials
        self._independent_sampler = independent_sampler or opts.samplers.RandomSampler(seed=seed)
        self._warn_independent_sampling = warn_independent_sampling
        self._search_space = opts.samplers.IntersectionSearchSpace()

    def reseed_rng(self) -> None:

        self._cma_opts["seed"] = random.randint(1, 2 ** 32)
        self._independent_sampler.reseed_rng()

    def infer_relative_search_space(
        self, experiment: Experiment, trial: FrozenTrial
    ) -> Dict[str, BaseDistribution]:

        search_space = {}
        for name, distribution in self._search_space.calculate(experiment).items():
            if distribution.single():
                # `cma` cannot handle distributions that contain just a single value, so we skip
                # them. Note that the parameter values for such distributions are sampled in
                # `Trial`.
                continue

            search_space[name] = distribution

        return search_space

    def sample_independent(
        self,
        experiment: Experiment,
        trial: FrozenTrial,
        param_name: str,
        param_distribution: BaseDistribution,
    ) -> float:

        if self._warn_independent_sampling:
            complete_trials = [t for t in experiment.trials if t.state == TrialState.COMPLETE]
            if len(complete_trials) >= self._n_startup_trials:
                self._log_independent_sampling(trial, param_name)

        return self._independent_sampler.sample_independent(
            experiment, trial, param_name, param_distribution
        )

    def sample_relative(
        self, experiment: Experiment, trial: FrozenTrial, search_space: Dict[str, BaseDistribution]
    ) -> Dict[str, float]:

        if len(search_space) == 0:
            return {}

        if len(search_space) == 1:
            _logger.info(
                "`PyCmaSampler` does not support optimization of 1-D search space. "
                "`{}` is used instead of `PyCmaSampler`.".format(
                    self._independent_sampler.__class__.__name__
                )
            )
            self._warn_independent_sampling = False
            return {}

        complete_trials = [t for t in experiment.trials if t.state == TrialState.COMPLETE]
        if len(complete_trials) < self._n_startup_trials:
            return {}

        if self._x0 is None:
            self._x0 = self._initialize_x0(search_space)

        if self._sigma0 is None:
            sigma0 = self._initialize_sigma0(search_space)
        else:
            sigma0 = self._sigma0
        # Avoid ZeroDivisionError in cma.CMAEvolutionStrategy.
        sigma0 = max(sigma0, _EPS)

        optimizer = _Optimizer(search_space, self._x0, sigma0, self._cma_stds, self._cma_opts)
        trials = experiment.trials
        last_told_trial_number = optimizer.tell(trials, experiment.direction)
        return optimizer.ask(trials, last_told_trial_number)

    @staticmethod
    def _initialize_x0(search_space: Dict[str, BaseDistribution]) -> Dict[str, Any]:

        x0 = {}
        for name, distribution in search_space.items():
            if isinstance(distribution, UniformDistribution):
                x0[name] = numpy.mean([distribution.high, distribution.low])
            elif isinstance(distribution, DiscreteUniformDistribution):
                x0[name] = numpy.mean([distribution.high, distribution.low])
            elif isinstance(distribution, IntUniformDistribution):
                x0[name] = int(numpy.mean([distribution.high, distribution.low]))
            elif isinstance(distribution, (LogUniformDistribution, IntLogUniformDistribution)):
                log_high = math.log(distribution.high)
                log_low = math.log(distribution.low)
                x0[name] = math.exp(numpy.mean([log_high, log_low]))
            elif isinstance(distribution, CategoricalDistribution):
                index = (len(distribution.choices) - 1) // 2
                x0[name] = distribution.choices[index]
            else:
                raise NotImplementedError(
                    "The distribution {} is not implemented.".format(distribution)
                )
        return x0

    @staticmethod
    def _initialize_sigma0(search_space: Dict[str, BaseDistribution]) -> float:

        sigma0s = []
        for name, distribution in search_space.items():
            if isinstance(distribution, UniformDistribution):
                sigma0s.append((distribution.high - distribution.low) / 6)
            elif isinstance(distribution, DiscreteUniformDistribution):
                sigma0s.append((distribution.high - distribution.low) / 6)
            elif isinstance(distribution, IntUniformDistribution):
                sigma0s.append((distribution.high - distribution.low) / 6)
            elif isinstance(distribution, (LogUniformDistribution, IntLogUniformDistribution)):
                log_high = math.log(distribution.high)
                log_low = math.log(distribution.low)
                sigma0s.append((log_high - log_low) / 6)
            elif isinstance(distribution, CategoricalDistribution):
                sigma0s.append((len(distribution.choices) - 1) / 6)
            else:
                raise NotImplementedError(
                    "The distribution {} is not implemented.".format(distribution)
                )
        return min(sigma0s)

    def _log_independent_sampling(self, trial: FrozenTrial, param_name: str) -> None:

        _logger.warning(
            "The parameter '{}' in trial#{} is sampled independently "
            "by using `{}` instead of `PyCmaSampler` "
            "(optimization performance may be degraded). "
            "`PyCmaSampler` does not support dynamic search space or `CategoricalDistribution`. "
            "You can suppress this warning by setting `warn_independent_sampling` "
            "to `False` in the constructor of `PyCmaSampler`, "
            "if this independent sampling is intended behavior.".format(
                param_name, trial.number, self._independent_sampler.__class__.__name__
            )
        )


class _Optimizer(object):
    def __init__(
        self,
        search_space: Dict[str, BaseDistribution],
        x0: Dict[str, Any],
        sigma0: float,
        cma_stds: Optional[Dict[str, float]],
        cma_opts: Dict[str, Any],
    ) -> None:

        self._search_space = search_space
        self._param_names = list(sorted(self._search_space.keys()))

        lows = []
        highs = []
        for param_name in self._param_names:
            dist = self._search_space[param_name]
            if isinstance(dist, CategoricalDistribution):
                # Handle categorical values by ordinal representation.
                # TODO(Yanase): Support one-hot representation.
                lows.append(-0.5)
                highs.append(len(dist.choices) - 0.5)
            elif isinstance(dist, UniformDistribution) or isinstance(dist, LogUniformDistribution):
                lows.append(self._to_cma_params(search_space, param_name, dist.low))
                highs.append(self._to_cma_params(search_space, param_name, dist.high) - _EPS)
            elif isinstance(dist, DiscreteUniformDistribution):
                r = dist.high - dist.low
                lows.append(0 - 0.5 * dist.q)
                highs.append(r + 0.5 * dist.q)
            elif isinstance(dist, IntUniformDistribution):
                lows.append(dist.low - 0.5 * dist.step)
                highs.append(dist.high + 0.5 * dist.step)
            elif isinstance(dist, IntLogUniformDistribution):
                lows.append(self._to_cma_params(search_space, param_name, dist.low - 0.5))
                highs.append(self._to_cma_params(search_space, param_name, dist.high + 0.5))
            else:
                raise NotImplementedError("The distribution {} is not implemented.".format(dist))

        # Set initial params.
        initial_cma_params = []
        for param_name in self._param_names:
            initial_cma_params.append(
                self._to_cma_params(self._search_space, param_name, x0[param_name])
            )
        cma_option = {
            "BoundaryHandler": cma.BoundTransform,
            "bounds": [lows, highs],
        }

        if cma_stds:
            cma_option["CMA_stds"] = [cma_stds.get(name, 1.0) for name in self._param_names]

        cma_opts.update(cma_option)

        self._es = cma.CMAEvolutionStrategy(initial_cma_params, sigma0, cma_opts)

    def tell(self, trials: List[FrozenTrial], experiment_direction: ExperimentDirection) -> int:

        complete_trials = self._collect_target_trials(trials, target_states={TrialState.COMPLETE})

        popsize = self._es.popsize
        generation = len(complete_trials) // popsize
        last_told_trial_number = -1
        for i in range(generation):
            xs = []
            ys = []
            for t in complete_trials[i * popsize: (i + 1) * popsize]:
                x = [
                    self._to_cma_params(self._search_space, name, t.params[name])
                    for name in self._param_names
                ]
                xs.append(x)
                ys.append(t.value)
                last_told_trial_number = t.number
            if experiment_direction == ExperimentDirection.MAXIMIZE:
                ys = [-1 * y if y is not None else y for y in ys]

            # Calling `ask` is required to avoid RuntimeError which claims that `tell` should only
            # be called once per iteration.
            self._es.ask()
            self._es.tell(xs, ys)
        return last_told_trial_number

    def ask(self, trials: List[FrozenTrial], last_told_trial_number: int) -> Dict[str, Any]:

        individual_index = len(self._collect_target_trials(trials, last_told_trial_number))
        popsize = self._es.popsize

        # individual_index may exceed the population size due to the parallel execution of multiple
        # trials. In such cases, `cma.cma.CMAEvolutionStrategy.ask` is called multiple times in an
        # iteration, and that may affect the optimization performance of CMA-ES.
        # In addition, please note that some trials may suggest the same parameters when multiple
        # samplers invoke this method simultaneously.
        while individual_index >= popsize:
            individual_index -= popsize
            self._es.ask()
        cma_params = self._es.ask()[individual_index]

        ret_val = {}
        for param_name, value in zip(self._param_names, cma_params):
            ret_val[param_name] = self._to_opts_params(self._search_space, param_name, value)
        return ret_val

    def _is_compatible(self, trial: FrozenTrial) -> bool:

        # Thanks to `intersection_search_space()` function, in sequential optimization,
        # the parameters of complete trials are always compatible with the search space.
        #
        # However, in distributed optimization, incompatible trials may complete on a worker
        # just after an intersection search space is calculated on another worker.

        for name, distribution in self._search_space.items():
            if name not in trial.params:
                return False

            samples.check_distribution_compatibility(distribution, trial.distributions[name])
            param_value = trial.params[name]
            param_internal_value = distribution.to_internal_repr(param_value)
            if not distribution._contains(param_internal_value):
                return False

        return True

    def _collect_target_trials(
        self,
        trials: List[FrozenTrial],
        last_told: int = -1,
        target_states: Optional[Set[TrialState]] = None,
    ) -> List[FrozenTrial]:

        target_trials = [t for t in trials if t.number > last_told]
        target_trials = [t for t in target_trials if self._is_compatible(t)]
        if target_states is not None:
            target_trials = [t for t in target_trials if t.state in target_states]

        return target_trials

    @staticmethod
    def _to_cma_params(
        search_space: Dict[str, BaseDistribution], param_name: str, opts_param_value: Any
    ) -> float:

        dist = search_space[param_name]
        if isinstance(dist, (LogUniformDistribution, IntLogUniformDistribution)):
            return math.log(opts_param_value)
        elif isinstance(dist, DiscreteUniformDistribution):
            return opts_param_value - dist.low
        elif isinstance(dist, CategoricalDistribution):
            return dist.choices.index(opts_param_value)
        return opts_param_value

    @staticmethod
    def _to_opts_params(
        search_space: Dict[str, BaseDistribution], param_name: str, cma_param_value: float
    ) -> Any:

        dist = search_space[param_name]
        if isinstance(dist, LogUniformDistribution):
            return math.exp(cma_param_value)
        if isinstance(dist, DiscreteUniformDistribution):
            v = numpy.round(cma_param_value / dist.q) * dist.q + dist.low
            # v may slightly exceed range due to round-off errors.
            return float(min(max(v, dist.low), dist.high))
        if isinstance(dist, IntUniformDistribution):
            r = numpy.round((cma_param_value - dist.low) / dist.step)
            v = r * dist.step + dist.low
            return int(v)
        if isinstance(dist, IntLogUniformDistribution):
            exp_value = math.exp(cma_param_value)
            v = numpy.round(exp_value)
            return int(min(max(v, dist.low), dist.high))

        if isinstance(dist, CategoricalDistribution):
            v = int(numpy.round(cma_param_value))
            return dist.choices[v]
        return cma_param_value


@deprecated("2.0.0", text="This class is renamed to :class:`~opts.frameworks.PyCmaSampler`.")
class CmaEsSampler(PyCmaSampler):
    """Wrapper class of PyCmaSampler for backward compatibility."""

    def __init__(
        self,
        x0: Optional[Dict[str, Any]] = None,
        sigma0: Optional[float] = None,
        cma_stds: Optional[Dict[str, float]] = None,
        seed: Optional[int] = None,
        cma_opts: Optional[Dict[str, Any]] = None,
        n_startup_trials: int = 1,
        independent_sampler: Optional[BaseSampler] = None,
        warn_independent_sampling: bool = True,
    ) -> None:

        super(CmaEsSampler, self).__init__(
            x0=x0,
            sigma0=sigma0,
            cma_stds=cma_stds,
            seed=seed,
            cma_opts=cma_opts,
            n_startup_trials=n_startup_trials,
            independent_sampler=independent_sampler,
            warn_independent_sampling=warn_independent_sampling,
        )
