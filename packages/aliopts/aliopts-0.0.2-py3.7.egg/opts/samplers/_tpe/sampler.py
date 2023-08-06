"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/15 3:43 下午
@Software: PyCharm
@File    : sampler.py
@E-mail  : victor.xsyang@gmail.com
"""
import math
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
import warnings

import numpy as np
import scipy.special
from scipy.stats import truncnorm

from opts import samples
from opts._experiment_direction import ExperimentDirection
from opts.samples import BaseDistribution
from opts.errors import ExperimentalWarning
from opts.logger import get_logger
from opts.samplers import BaseSampler
from opts.samplers import IntersectionSearchSpace
from opts.samplers import RandomSampler
from opts.samplers._tpe.multivariate_parzen_estimator import _MultivariateParzenEstimator
from opts.samplers._tpe.parzen_estimator import _ParzenEstimator
from opts.samplers._tpe.parzen_estimator import _ParzenEstimatorParameters
from opts.experiment import Experiment
from opts.trial import FrozenTrial
from opts.trial import TrialState

EPS = 1e-12
_DISTRIBUTION_CLASSES = (
    samples.UniformDistribution,
    samples.LogUniformDistribution,
    samples.DiscreteUniformDistribution,
    samples.IntUniformDistribution,
    samples.IntLogUniformDistribution,
    samples.CategoricalDistribution
)
_logger = get_logger(__name__)


def default_gamma(x: int) -> int:
    return min(int(np.ceil(0.1 * x)), 25)


def hyperopt_default_gamma(x: int) -> int:
    return min(int(np.ceil(0.25 * np.sqrt(x))), 25)


def default_weights(x: int) -> np.ndarray:
    if x == 0:
        return np.asarray([])
    elif x < 25:
        return np.ones(x)
    else:
        ramp = np.linspace(1.0 / x, 1.0, num=x - 25)
        flat = np.ones(25)
        return np.concatenate([ramp, flat], axis=0)


class TPESampler(BaseSampler):
    """Sampler using TPE(Tree-structured Parzen Estimator) algorithm.
    This sampler is based on *independent sampling*.
    """

    def __init__(
            self,
            consider_prior: bool = True,
            prior_weight: float = 1.0,
            consider_magic_clip: bool = True,
            consider_endpoints: bool = False,
            n_startup_trials: int = 10,
            n_ei_candidates: int = 24,
            gamma: Callable[[int], int] = default_gamma,
            weights: Callable[[int], np.ndarray] = default_weights,
            seed: Optional[int] = None,
            *,
            multivariate: bool = False,
            warn_independent_sampling: bool = True
    ) -> None:
        self._parzen_estimator_parameters = _ParzenEstimatorParameters(
            consider_prior, prior_weight, consider_magic_clip, consider_endpoints, weights
        )
        self._prior_weight = prior_weight
        self._n_startup_trials = n_startup_trials
        self._n_ei_candidates = n_ei_candidates
        self._gamma = gamma
        self._weights = weights

        self._warn_independent_sampling = warn_independent_sampling
        self._rng = np.random.RandomState(seed)
        self._random_sampler = RandomSampler(seed=seed)

        self._multivariate = multivariate
        self._search_space = IntersectionSearchSpace()

        if multivariate:
            warnings.warn(
                "``multivariate`` option is an experimental feature."
                " The interface can change in the future.",
                ExperimentalWarning,
            )

    def reseed_rng(self) -> None:
        self._rng = np.random.RandomState()
        self._random_sampler.reseed_rng()

    def infer_relative_search_space(
            self, experiment: Experiment,
            trial: FrozenTrial) -> Dict[str, BaseDistribution]:
        if not self._multivariate:
            return {}

        search_space: Dict[str, BaseDistribution] = {}
        for name, distribution in self._search_space.calculate(experiment).items():
            if not isinstance(distribution, _DISTRIBUTION_CLASSES):
                if self._warn_independent_sampling:
                    complete_trials = experiment._storage.get_all_trials(
                        experiment._experiment_id, deepcopy=False
                    )
                    if len(complete_trials) >= self._n_startup_trials:
                        self._log_independent_sampling(trial, name)
                continue
            search_space[name] = distribution
        return search_space

    def _log_independent_sampling(self,
                                  trial: FrozenTrial,
                                  param_name: str) -> None:
        _logger.warning(
            "The parameter '{}' in trial#{} is sampled independently "
            "instead of being sampled by multivariate TPE sampler. "
            "(optimization performance may be degraded). "
            "You can suppress this warning by setting `warn_independent_sampling` "
            "to `False` in the constructor of `TPESampler`, "
            "if this independent sampling is intended behavior.".format(param_name, trial.number)
        )

    def sample_relative(
            self, experiment: Experiment, trial: FrozenTrial,
            search_space: Dict[str, BaseDistribution]
    ) -> Dict[str, Any]:
        if search_space == {}:
            return {}

        param_name = list(search_space.keys())
        values, scores = _get_multivariate_observation_pairs(experiment, param_name)

        # if the number of samples is insufficient, we run random trial.
        n = len(scores)
        if n < self._n_startup_trials:
            return {}

        # divide data into below and above
        below, above = self._split_multivariate_observation_pairs(values, scores)
        mpe_below = _MultivariateParzenEstimator(
            below, search_space, self._parzen_estimator_parameters
        )
        mpe_above = _MultivariateParzenEstimator(
            above, search_space, self._parzen_estimator_parameters
        )

        samples_below = mpe_below.sample(self._rng, self._n_ei_candidates)
        log_likelihoods_below = mpe_below.log_pdf(samples_below)
        log_likelihoods_above = mpe_above.log_pdf(samples_below)
        ret = TPESampler._compare_multivariate(
            samples_below, log_likelihoods_below, log_likelihoods_above
        )
        for param_name, dist in search_space.items():
            ret[param_name] = dist.to_external_repr(ret[param_name])
        return ret

    def _split_multivariate_observation_pairs(
            self,
            config_vals: Dict[str, List[Optional[float]]],
            loss_vals: List[Tuple[float, float]]
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:

        config_vals = {k: np.asarray(v, dtype=float) for k, v in config_vals.items()}
        loss_vals = np.asarray(loss_vals, dtype=[("step", float), ("score", float)])

        n_below = self._gamma(len(loss_vals))
        index_loss_ascending = np.argsort(loss_vals)
        index_below = np.sort(index_loss_ascending[:n_below])
        index_above = np.sort(index_loss_ascending[n_below:])
        below = {}
        above = {}
        for param_name, param_val in config_vals.items():
            below[param_name] = param_val[index_below]
            above[param_name] = param_val[index_above]
        return below, above

    def sample_independent(
            self,
            experiment: Experiment,
            trial: FrozenTrial,
            param_name: str,
            param_distribution: BaseDistribution
    ) -> Any:

        values, scores = _get_observation_pairs(experiment, param_name)

        n = len(values)
        if n < self._n_startup_trials:
            return self._random_sampler.sample_independent(
                experiment, trial, param_name, param_distribution
            )

        below_param_values, above_param_values = self._split_observation_pairs(values, scores)

        if isinstance(param_distribution, samples.UniformDistribution):
            return self._sample_uniform(param_distribution, below_param_values, above_param_values)
        elif isinstance(param_distribution, samples.LogUniformDistribution):
            return self._sample_loguniform(
                param_distribution, below_param_values, above_param_values
            )
        elif isinstance(param_distribution, samples.DiscreteUniformDistribution):
            return self._sample_discrete_uniform(
                param_distribution, below_param_values, above_param_values
            )
        elif isinstance(param_distribution, samples.IntUniformDistribution):
            return self._sample_int(param_distribution, below_param_values, above_param_values)
        elif isinstance(param_distribution, samples.IntLogUniformDistribution):
            return self._sample_int_loguniform(
                param_distribution, below_param_values, above_param_values
            )
        elif isinstance(param_distribution, samples.CategoricalDistribution):
            index = self._sample_categorical_index(
                param_distribution, below_param_values, above_param_values
            )
            return param_distribution.choices[index]
        else:
            distribution_list = [
                samples.UniformDistribution.__name__,
                samples.LogUniformDistribution.__name__,
                samples.DiscreteUniformDistribution.__name__,
                samples.IntUniformDistribution.__name__,
                samples.IntLogUniformDistribution.__name__,
                samples.CategoricalDistribution.__name__
            ]
            raise NotImplementedError(
                "The distribution {} is not implemented. "
                "The parameter distribution should be one of the {}".format(
                    param_distribution, distribution_list
                )
            )

    def _sample_categorical_index(
            self,
            distribution: samples.CategoricalDistribution,
            below: np.ndarray,
            above: np.ndarray
    ) -> int:
        choices = distribution.choices
        below = list(map(int, below))
        above = list(map(int, above))
        upper = len(choices)

        size = (self._n_ei_candidates,)
        weights_below = self._weights(len(below))
        counts_below = np.bincount(below, minlength=upper, weights=weights_below)
        weighted_below = counts_below + self._prior_weight
        weighted_below /= weighted_below.sum()
        sample_items_below = self._sample_from_categorical_dist(weighted_below, size)
        log_likelihoods_below = TPESampler._categorical_log_pdf(sample_items_below, weighted_below)

        weights_above = self._weights(len(above))
        counts_above = np.bincount(above, minlength=upper, weights=weights_above)
        weighted_above = counts_above + self._prior_weight
        weighted_above /= weighted_above.sum()
        log_likelihoods_above = TPESampler._categorical_log_pdf(sample_items_below, weighted_above)

        return int(
            TPESampler._compare(
                sample_items=sample_items_below, log_l=log_likelihoods_below, log_g=log_likelihoods_above
            )[0]
        )

    @classmethod
    def _categorical_log_pdf(cls, sample_item: np.ndarray, p: np.ndarray) -> np.ndarray:
        if sample_item.size:
            return np.log(np.asarray(p)[sample_item])
        else:
            return np.asarray([])

    def _sample_from_categorical_dist(
            self, probabilities: np.ndarray, size: Tuple[int]) -> np.ndarray:
        if size == (0,):
            return np.asarray([], dtype=float)
        assert len(size)

        if probabilities.size == 1 and isinstance(probabilities[0], np.ndarray):
            probabilities = probabilities[0]
        assert probabilities.ndim == 1

        n_draws = np.prod(size).item()
        sample_item = self._rng.multinomial(n=1, pvals=probabilities, size=n_draws)
        assert sample_item.shape == size + probabilities.shape
        return_val = np.dot(sample_item, np.arange(probabilities.size)).reshape(size)
        return return_val

    @classmethod
    def _logsum_rows(cls, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x)
        m = x.max(axis=1)
        return np.log(np.exp(x - m[:, None]).sum(axis=1)) + m

    @classmethod
    def normal_cdf(cls, x: float, mu: np.ndarray, sigma: np.ndarray) -> np.ndarray:
        mu, sigma = map(np.asarray, (mu, sigma))
        denominator = x - mu
        numerator = np.maximum(np.sqrt(2) * sigma, EPS)
        z = denominator / numerator
        return 0.5 * (1 + scipy.special.erf(z))

    @classmethod
    def _compare(cls, sample_items: np.ndarray, log_l: np.ndarray, log_g: np.ndarray) -> np.ndarray:

        sample_items, log_l, log_g = map(np.asarray, (sample_items, log_l, log_g))
        if sample_items.size:
            score = log_l - log_g
            if sample_items.size != score.size:
                raise ValueError(
                    "The size of the 'samples' and that of the 'score' "
                    "should be same. "
                    "But (samples.size, score.size) = ({}, {})".format(sample_items.size, score.size)
                )
            best = np.argmax(score)
            return np.asarray([sample_items[best]] * sample_items.size)
        else:
            return np.asarray([])

    @classmethod
    def _compare_multivariate(
            cls,
            multivariate_samples: Dict[str, np.ndarray],
            log_l: np.ndarray,
            log_g: np.ndarray
    ) -> Dict[str, Union[float, int]]:
        sample_size = next(iter(multivariate_samples.values())).size
        if sample_size:
            score = log_l - log_g
            if sample_size != score.size:
                raise ValueError(
                    "The size of the 'samples' and that of the 'score' "
                    "should be same. "
                    "But (samples.size, score.size) = ({}, {})".format(sample_size, score.size)
                )
            best = np.argmax(score)
            return {k: v[best].item() for k, v in multivariate_samples.items()}
        else:
            raise ValueError(
                "The size of 'samples' should be more than 0."
                "But samples.size = {}".format(sample_size)
            )

    @staticmethod
    def hyperopt_parameters() -> Dict[str, Any]:
        """Return the default parameters of hyperopt

        :return:
        """
        return {
            "consider_prior": True,
            "prior_weight": 1.0,
            "consider_magic_clip": True,
            "consider_endpoints": False,
            "n_startup_trials": 20,
            "n_ei_candidates": 24,
            "gamma": hyperopt_default_gamma,
            "weights": default_weights
        }

    def _split_observation_pairs(
            self, config_vals: List[Optional[float]], loss_vals: List[Tuple[float, float]]
    ) -> Tuple[np.ndarray, np.ndarray]:

        config_vals = np.asarray(config_vals)
        loss_vals = np.asarray(loss_vals, dtype=[("step", float), ("score", float)])

        n_below = self._gamma(len(config_vals))
        loss_ascending = np.argsort(loss_vals)
        below = config_vals[np.sort(loss_ascending[:n_below])]
        below = np.asarray([v for v in below if v is not None], dtype=float)
        above = config_vals[np.sort(loss_ascending[n_below:])]
        above = np.asarray([v for v in above if v is not None], dtype=float)
        return below, above

    def _sample_uniform(
            self, distribution: samples.UniformDistribution, below: np.ndarray, above: np.ndarray
    ) -> float:
        low = distribution.low
        high = distribution.high
        return self._sample_numberical(low, high, below, above)

    def _sample_loguniform(
            self,
            distribution: samples.LogUniformDistribution,
            below: np.ndarray,
            above: np.ndarray
    ) -> float:
        low = distribution.low
        high = distribution.high
        return self._sample_numberical(low, high, below, above, is_log=True)

    def _sample_discrete_uniform(
            self,
            distribution: samples.DiscreteUniformDistribution,
            below: np.ndarray,
            above: np.ndarray
    ) -> float:
        q = distribution.q
        r = distribution.high - distribution.low
        low = 0 - 0.5 * q
        high = r + 0.5 * q
        above -= distribution.low
        high -= distribution.low
        best_sample = self._sample_numberical(low, high, below, above, q=q) + distribution.low
        return min(max(best_sample, distribution.low), distribution.high)

    def _sample_int(
            self,
            distribution: samples.IntUniformDistribution,
            below: np.ndarray,
            above: np.ndarray
    ) -> int:
        d = samples.DiscreteUniformDistribution(
            low=distribution.low, high=distribution.high, q=distribution.step
        )
        return int(self._sample_discrete_uniform(d, below, above))

    def _sample_int_loguniform(
            self,
            distribution: samples.IntLogUniformDistribution,
            below: np.ndarray,
            above: np.ndarray
    ) -> int:
        low = distribution.low - 0.5
        high = distribution.high + 0.5

        sample = self._sample_numberical(low, high, below, above, is_log=True)
        best_sample = np.round(sample)
        return int(min(max(best_sample, distribution.low), distribution.high))

    def _sample_numberical(
            self,
            low: float,
            high: float,
            below: np.ndarray,
            above: np.ndarray,
            q: Optional[float] = None,
            is_log: bool = False
    ) -> float:
        if is_log:
            low = np.log(low)
            high = np.log(high)
            below = np.log(below)
            above = np.log(above)

        size = (self._n_ei_candidates,)

        parzen_estimator_below = _ParzenEstimator(
            mus=below, low=low, high=high, parameters=self._parzen_estimator_parameters
        )

        sample_items_below = self._sample_from_gmm(
            parazen_estimator=parzen_estimator_below, low=low, high=high, q=q, size=size
        )
        log_likelihoods_below = self._gmm_log_pdf(
            sample_items=sample_items_below,
            parzen_estimator=parzen_estimator_below,
            low=low,
            high=high,
            q=q
        )

        parzen_estimator_above = _ParzenEstimator(
            mus=above, low=low, high=high, parameters=self._parzen_estimator_parameters
        )

        log_likelihoods_above = self._gmm_log_pdf(
            sample_items=sample_items_below,
            parzen_estimator=parzen_estimator_above,
            low=low,
            high=high,
            q=q
        )

        ret = float(
            TPESampler._compare(
                sample_items=sample_items_below,
                log_l=log_likelihoods_below,
                log_g=log_likelihoods_above
            )[0]
        )
        return math.exp(ret) if is_log else ret

    def _gmm_log_pdf(
            self,
            sample_items: np.ndarray,
            parzen_estimator: _ParzenEstimator,
            low: float,
            high: float,
            q: Optional[float] = None
    ) -> np.ndarray:
        weights = parzen_estimator.weights
        mus = parzen_estimator.mus
        sigmas = parzen_estimator.sigmas
        sample_items, weights, mus, sigmas = map(np.asarray, (sample_items, weights, mus, sigmas))
        if sample_items.size == 0:
            return np.asarray([], dtype=float)
        if weights.ndim != 1:
            raise ValueError(
                "The 'weights' should be 1-dimension. "
                "But weights.shape = {}".format(weights.shape)
            )
        if mus.ndim != 1:
            raise ValueError(
                "The 'mus' should be 1-dimension. But mus.shape = {}".format(mus.shape)
            )

        if sigmas.ndim != 1:
            raise ValueError(
                "The 'sigmas' should be 1-dimension. But sigmas.shape = {}".format(sigmas.shape)

            )

        # print("ssss", weights, TPESampler._normal_cdf(high, mus, sigmas),TPESampler._normal_cdf(low, mus, sigmas))


        p_accept = np.sum(
            weights
            * (
                    TPESampler._normal_cdf(high, mus, sigmas)
                    - TPESampler._normal_cdf(low, mus, sigmas)
            )
        )
        if q is None:
            distance = sample_items[..., None] - mus
            mahalanobis = (distance / np.maximum(sigmas, EPS)) ** 2
            Z = np.sqrt(2 * np.pi) * sigmas
            coefficient = weights / Z / p_accept
            return TPESampler._logsum_rows(-0.5 * mahalanobis + np.log(coefficient))
        else:
            cdf_func = TPESampler._normal_cdf
            upper_bound = np.minimum(sample_items + q / 2.0, high)
            lower_bound = np.maximum(sample_items - q / 2.0, low)
            probabilities = np.sum(
                weights[..., None]
                * (
                        cdf_func(upper_bound[None], mus[..., None], sigmas[..., None])
                        - cdf_func(lower_bound[None], mus[..., None], sigmas[..., None])
                ),
                axis=0,
            )
            return np.log(probabilities + EPS)

    @classmethod
    def _normal_cdf(cls, x: float, mu: np.ndarray, sigma: np.ndarray) -> np.ndarray:
        mu, sigma = map(np.asarray, (mu, sigma))
        denominator = x - mu
        numerator = np.maximum(np.sqrt(2) * sigma, EPS)
        z = denominator / numerator
        return 0.5 * (1 + scipy.special.erf(z))



    def _sample_from_gmm(
            self,
            parazen_estimator: _ParzenEstimator,
            low: float,
            high: float,
            q: Optional[float] = None,
            size: Tuple = ()
    ) -> np.ndarray:
        weights = parazen_estimator.weights
        mus = parazen_estimator.mus
        sigmas = parazen_estimator.sigmas
        weights, mus, sigmas = map(np.asarray, (weights, mus, sigmas))
        if low >= high:
            raise ValueError(
                "The 'low' should be lower than the 'high'. "
                "But (low, high) = ({}, {}).".format(low, high)
            )

        active = np.argmax(self._rng.multinomial(1, weights, size=size), axis=-1)
        trunc_low = (low - mus[active]) / sigmas[active]
        trunc_high = (high - mus[active]) / sigmas[active]
        sample_items = np.full((), fill_value=high + 1.0, dtype=np.float64)
        while (sample_items >= high).any():
            sample_items = np.where(
                sample_items < high,
                sample_items,
                truncnorm.rvs(
                    trunc_low,
                    trunc_high,
                    size=size,
                    loc=mus[active],
                    scale=sigmas[active],
                    random_state=self._rng
                ),
            )
        if q is None:
            return sample_items
        else:
            return np.round(sample_items / q) * q


def _get_multivariate_observation_pairs(
        experiment: Experiment,
        param_names: List[str]
) -> Tuple[Dict[str, List[Optional[float]]], List[Tuple[float, float]]]:
    sign = 1
    if experiment.direction == ExperimentDirection.MAXIMIZE:
        sign = -1

    scores = []
    values: Dict[str, List[Optional[float]]] = {param_name: [] for param_name in param_names}
    for trial in experiment._storage.get_all_trials(experiment._experiment_id, deepcopy=False):
        # extract score from the trial
        if trial.state is TrialState.COMPLETE and trial.value is not None:
            score = (-float("inf"), sign * trial.value)
        elif trial.state is TrialState.STOP:
            if len(trial.intermediate_values) > 0:
                step, intermediate_value = max(trial.intermediate_values.items())
                if math.isnan(intermediate_value):
                    score = (-step, float("inf"))
                else:
                    score = (-step, sign * intermediate_value)
            else:
                score = (float("inf"), 0.0)
        else:
            continue
        scores.append(score)
        for param_name in param_names:
            assert param_name in trial.params
            distribution = trial.distributions[param_name]
            param_value = distribution.to_internal_repr(trial.params[param_name])
            values[param_name].append(param_value)
    return values, scores


def _get_observation_pairs(
        experiment: Experiment,
        param_name: str
) -> Tuple[List[Optional[float]], List[Tuple[float, float]]]:
    """Get observation pairs from the experiment.

    :param experiment:
    :param param_name:
    :return:
    """
    sign = 1
    # print("direction", experiment.direction)
    if experiment.direction == ExperimentDirection.MAXIMIZE:
        sign = -1

    values = []
    scores = []
    for trial in experiment._storage.get_all_trials(experiment._experiment_id, deepcopy=False):

        if trial.state is TrialState.COMPLETE and trial.value is not None:
            score = (-float("inf"), sign * trial.value)
        elif trial.state is TrialState.STOP:
            if len(trial.intermediate_values) > 0:
                step, intermediate_value = max(trial.intermediate_values.items())
                if math.isnan(intermediate_value):
                    score = (-step, float("inf"))
                else:
                    score = (-step, sign * intermediate_value)
            else:
                score = (float("inf"), 0.0)
        else:
            continue

        param_value: Optional[float] = None
        if param_name in trial.params:
            distribution = trial.distributions[param_name]
            param_value = distribution.to_internal_repr(trial.params[param_name])

        values.append(param_value)
        scores.append(score)
    return values, scores
