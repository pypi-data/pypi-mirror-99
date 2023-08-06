"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/26 3:04 下午
@Software: PyCharm
@File    : _experiment_summary.py
@E-mail  : victor.xsyang@gmail.com
"""
import datetime
from typing import Any
from typing import Dict
from typing import Optional

from opts import logger
from opts import trial
from opts._experiment_direction import ExperimentDirection

_logger = logger.get_logger(__name__)


class ExperimentSummary(object):
    """Basic attributes and aggregated results of :class: `opts.experiment.Experiment`.

    """

    def __init__(
            self,
            experiment_name: str,
            direction: ExperimentDirection,
            best_trial: Optional[trial.FrozenTrial],
            user_attrs: Dict[str, Any],
            system_attrs: Dict[str, Any],
            n_trials: int,
            datetime_start: Optional[datetime.datetime],
            experiment_id: int,
    ):
        self.experiment_name = experiment_name
        self.direction = direction
        self.best_trial = best_trial
        self.user_attrs = user_attrs
        self.system_attrs = system_attrs
        self.n_trials = n_trials
        self.datetime_start = datetime_start
        self._experiment_id = experiment_id

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExperimentSummary):
            return NotImplemented

        return self._experiment_id < other._experiment_id

    def __lt__(self, other: Any) -> bool:

        if not isinstance(other, ExperimentSummary):
            return NotImplemented

        return self._experiment_id < other._experiment_id

    def __le__(self, other: Any) -> bool:

        if not isinstance(other, ExperimentSummary):
            return NotImplemented

        return self._experiment_id <= other._experiment_id
