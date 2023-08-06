"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/25 5:06 下午
@Software: PyCharm
@File    : _hyperband.py
@E-mail  : victor.xsyang@gmail.com
"""
import math
from typing import List
from typing import Optional
from typing import Union

import opts
from opts import logger
from opts.stoppers._base import BaseStopper
from opts.stoppers._successive_halving import SuccessiveHalvingStopper
from opts.trial._state import TrialState

_logger = logger.get_logger(__name__)


class HyperbandStopper(BaseStopper):
    """Stopper using Hyperband

    """

    def __init__(
            self,
            min_resource: int = 1,
            max_resource: Union[str, int] = "auto",
            reduction_factor: int = 3,
    ) -> None:

        self._min_resource = min_resource
        self._max_resource = max_resource
        self._reduction_factor = reduction_factor
        self._stoppers: List[SuccessiveHalvingStopper] = []
        self._total_trial_allocation_budget = 0
        self._trial_allocation_budgets: List[int] = []
        self._n_brackets: Optional[int] = None

        if not isinstance(self._max_resource, int) and self._max_resource != "auto":
            raise ValueError(
                "The 'max_resource' should be integer or 'auto'. "
                "But max_resource = {}".format(self._max_resource)
            )

    def stop(self, experiment: "opts.experiment.Experiment", trial: "opts.trail.FrozenTrial") -> bool:
        if len(self._stoppers) == 0:
            self._try_initialization(experiment)
            if len(self._stoppers) == 0:
                return False

        bracket_id = self._get_bracket_id(experiment, trial)
        _logger.debug("{}th bracket is selected".format(bracket_id))
        bracket_experiment = self._create_bracket_experiment(experiment, bracket_id)
        return self._stoppers[bracket_id].stop(bracket_experiment, trial)

    def _try_initialization(self, experiment: "opts.experiment.Experiment") -> None:
        if self._max_resource == "auto":
            trials = experiment.get_trials(deepcopy=False)
            n_steps = [
                t.last_step
                for t in trials
                if t.state == TrialState.COMPLETE and t.last_step is not None
            ]

            if not n_steps:
                return

            self._max_resource = max(n_steps) + 1

        assert isinstance(self._max_resource, int)

        if self._n_brackets is None:
            # In the original paper http://www.jmlr.org/papers/volume18/16-558/16-558.pdf, the
            # inputs of Hyperband are `R`: max resource and `\eta`: reduction factor. The
            # number of brackets (this is referred as `s_{max} + 1` in the paper) is calculated
            # by s_{max} + 1 = \floor{\log_{\eta} (R)} + 1 in Algorithm 1 of the original paper.
            # In this implementation, we combine this formula and that of ASHA paper
            # https://arxiv.org/abs/1502.07943 as
            # `n_brackets = floor(log_{reduction_factor}(max_resource / min_resource)) + 1`
            self._n_brackets = (
                    math.floor(
                        math.log(self._max_resource / self._min_resource, self._reduction_factor)
                    )
                    + 1
            )

        _logger.debug("Hyperband has {} brackets".format(self._n_brackets))

        for bracket_id in range(self._n_brackets):
            trial_allocation_budget = self._calculate_trial_allocation_budget(bracket_id)
            self._total_trial_allocation_budget += trial_allocation_budget
            self._trial_allocation_budgets.append(trial_allocation_budget)

            stopper = SuccessiveHalvingStopper(
                min_resource=self._min_resource,
                reduction_factor=self._reduction_factor,
                min_early_stopping_rate=bracket_id,
            )
            self._stoppers.append(stopper)

    def _calculate_trial_allocation_budget(self, bracket_id: int) -> int:
        """Compute the trial allocated budget for a bracket of ``bracket_id``.

        In the `original paper <http://www.jmlr.org/papers/volume18/16-558/16-558.pdf>`, the
        number of trials per one bracket is referred as ``n`` in Algorithm 1. Since we do not know
        the total number of trials in the leaning scheme of Optuna, we calculate the ratio of the
        number of trials here instead.
        """

        assert self._n_brackets is not None
        s = self._n_brackets - 1 - bracket_id
        return math.ceil(self._n_brackets * (self._reduction_factor ** s) / (s + 1))

    def _get_bracket_id(
            self, experiment: "opts.experiment.Experiment", trial: "opts.trial.FrozenTrial"
    ) -> int:
        """Compute the index of bracket for a trial of ``trial_number``.

        The index of a bracket is noted as :math:`s` in
        `Hyperband paper <http://www.jmlr.org/papers/volume18/16-558/16-558.pdf>`_.
        """

        if len(self._stoppers) == 0:
            return 0

        assert self._n_brackets is not None
        n = (
                hash("{}_{}".format(experiment.experiment_name, trial.number))
                % self._total_trial_allocation_budget
        )
        for bracket_id in range(self._n_brackets):
            n -= self._trial_allocation_budgets[bracket_id]
            if n < 0:
                return bracket_id

        assert False, "This line should be unreachable."

    def _create_bracket_experiment(
            self, experiment: "opts.experiment.Experiment", bracket_id: int
    ) -> "opts.experiment.Experiment":
        # This class is assumed to be passed to
        # `SuccessiveHalvingPruner.prune` in which `get_trials`,
        # `direction`, and `storage` are used.
        # But for safety, prohibit the other attributes explicitly.
        class _BracketExperiment(opts.experiment.Experiment):

            _VALID_ATTRS = (
                "get_trials",
                "direction",
                "_storage",
                "_experiment_id",
                "stopper",
                "experiment_name",
                "_bracket_id",
                "sampler",
                "trials",
            )

            def __init__(self, experiment: "opts.experiment.Experiment", bracket_id: int) -> None:
                super().__init__(
                    experiment_name=experiment.experiment_name,
                    storage=experiment._storage,
                    sampler=experiment.sampler,
                    stopper=experiment.stopper,
                )
                self._bracket_id = bracket_id

            def get_trials(self, deepcopy: bool = True) -> List["opts.trial.FrozenTrial"]:
                trials = super().get_trials(deepcopy=deepcopy)
                stopper = self.stopper
                assert isinstance(stopper, HyperbandStopper)
                return [t for t in trials if stopper._get_bracket_id(self, t) == self._bracket_id]

            def __getattribute__(self, attr_name):  # type: ignore
                if attr_name not in _BracketExperiment._VALID_ATTRS:
                    raise AttributeError(
                        "_BracketExperiment does not have attribute of '{}'".format(attr_name)
                    )
                else:
                    return object.__getattribute__(self, attr_name)

        return _BracketExperiment(experiment, bracket_id)
