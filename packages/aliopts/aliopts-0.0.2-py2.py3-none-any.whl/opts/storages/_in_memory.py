"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/29 4:49 下午
@Software: PyCharm
@File    : _in_memory.py
@E-mail  : victor.xsyang@gmail.com
"""
import copy
from datetime import datetime
import threading
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
import uuid

import opts
from opts import samples
from opts._experiment_direction import ExperimentDirection
from opts._experiment_summary import ExperimentSummary
from opts.errors import DuplicatedExperimentError
from opts.storages import BaseStorage
from opts.storages._base import DEFAULT_EXPERIMENT_NAME_PREFIX
from opts.trial import FrozenTrial
from opts.trial import TrialState
from opts.samples import BaseDistribution
from opts import samples

_logger = opts.logger.get_logger(__name__)


class _ExperimentInfo:
    def __init__(self, name: str) -> None:
        self.trials: List[FrozenTrial] = []
        self.param_distribution: Dict[str, samples.BaseDistribution] = {}
        self.user_attrs: Dict[str, Any] = {}
        self.system_attrs: Dict[str, Any] = {}
        self.name: str = name
        self.direction = ExperimentDirection.NOT_SET
        self.best_trial_id: Optional[int] = None


class InMemoryStorage(BaseStorage):
    """Storage class that stores data in memory of the Python process.

    """

    def __init__(self) -> None:
        self._trial_id_to_experiment_id_and_number: Dict[int, Tuple[int, int]] = {}
        self._experiment_name_to_id: Dict[str, int] = {}
        self._experiments: Dict[int, _ExperimentInfo] = {}

        self._max_experiment_id = -1
        self._max_trial_id = -1

        self._lock = threading.RLock()

    def __getstate__(self) -> Dict[Any, Any]:
        state = self.__dict__.copy()
        del state["_lock"]
        return state

    def __setstate__(self, state: Dict[Any, Any]) -> None:
        self.__dict__.update(state)
        self._lock = threading.RLock()

    def create_new_experiment(self, experiment_name: Optional[str] = None) -> int:

        with self._lock:
            experiment_id = self._max_experiment_id + 1
            self._max_experiment_id += 1

            if experiment_name is not None:
                if experiment_name in self._experiment_name_to_id:
                    raise DuplicatedExperimentError
            else:
                experiment_uuid = str(uuid.uuid4())
                experiment_name = DEFAULT_EXPERIMENT_NAME_PREFIX + experiment_uuid
            self._experiments[experiment_id] = _ExperimentInfo(experiment_name)
            self._experiment_name_to_id[experiment_name] = experiment_id

            _logger.info("A new experiment created in memory with name: {}".format(experiment_name))

            return experiment_id

    def delete_experiment(self, experiment_id: int) -> None:
        with self._lock:
            self._check_experiment_id(experiment_id)

            for trial in self._experiments[experiment_id].trials:
                del self._trial_id_to_experiment_id_and_number[trial._trial_id]
            experiment_name = self._experiments[experiment_id].name
            del self._experiment_name_to_id[experiment_name]
            del self._experiments[experiment_id]

    def set_experiment_direction(self, experiment_id: int, direction: ExperimentDirection) -> None:
        with self._lock:
            self._check_experiment_id(experiment_id)
            experiment = self._experiments[experiment_id]
            if experiment.direction != ExperimentDirection.NOT_SET and experiment.direction != direction:
                raise ValueError(
                    "Cannot overwrite experiment direction from {} to {}.".format(
                        experiment.direction, direction
                    )
                )
            experiment.direction = direction

    def set_experiment_user_attr(self, experiment_id: int, key: str, value: Any) -> None:
        with self._lock:
            self._check_experiment_id(experiment_id)
            self._experiments[experiment_id].user_attrs[key] = value

    def set_experiment_system_attr(self, experiment_id: int, key: str, value: Any) -> None:
        with self._lock:
            self._check_experiment_id(experiment_id)
            self._experiments[experiment_id].system_attrs[key] = value

    def get_experiment_id_from_trial_id(self, trial_id: int) -> int:
        with self._lock:
            self._check_experiment_id(trial_id)
            return self._trial_id_to_experiment_id_and_number[trial_id][0]

    def get_experiment_name_from_id(self, experiment_id: int) -> str:
        with self._lock:
            self._check_experiment_id(experiment_id)
            return self._experiments[experiment_id].name

    def get_experiment_direction(self, experiment_id: int) -> ExperimentDirection:
        with self._lock:
            self._check_experiment_id(experiment_id)
            return self._experiments[experiment_id].direction

    def get_experiment_id_from_name(self, experiment_name: str) -> int:
        with self._lock:
            if experiment_name not in self._experiment_name_to_id:
                raise KeyError("No such experiment {}.".format(experiment_name))

            return self._experiment_name_to_id[experiment_name]

    def get_experiment_system_attrs(self, experiment_id: int) -> Dict[str, Any]:
        with self._lock:
            self._check_experiment_id(experiment_id)
            return self._experiments[experiment_id].system_attrs

    def get_experiment_user_attrs(self, experiment_id: int) -> Dict[str, Any]:
        with self._lock:
            self._check_experiment_id(experiment_id)
            return self._experiments[experiment_id].user_attrs

    def get_all_experiment_summaries(self) -> List[ExperimentSummary]:
        with self._lock:
            return [self._build_experiment_summary(experiment_id) for experiment_id in self._experiments.keys()]

    def _build_experiment_summary(self, experiment_id: int) -> ExperimentSummary:
        experiment = self._experiments[experiment_id]
        return ExperimentSummary(
            experiment_name=experiment.name,
            direction=experiment.direction,
            best_trial=copy.deepcopy(self._get_trial(experiment.best_trial_id))
            if experiment.best_trial_id is not None
            else None,
            user_attrs=copy.deepcopy(experiment.user_attrs),
            system_attrs=copy.deepcopy(experiment.system_attrs),
            n_trials=len(experiment.trials),
            datetime_start=min(
                [trial.datetime_start for trial in self.get_all_trials(experiment_id, deepcopy=False)]
            )
            if experiment.trials
            else None,
            experiment_id=experiment_id
        )

    def create_new_trial(self, experiment_id: int, template_trial: Optional[FrozenTrial] = None) -> int:
        with self._lock:
            self._check_experiment_id(experiment_id)
            if template_trial is None:
                trial = self._create_running_trial()
                # print("trial", trial)
            else:
                trial = copy.deepcopy(template_trial)
            trial_id = self._max_trial_id + 1
            self._max_trial_id += 1
            trial.number = len(self._experiments[experiment_id].trials)
            trial._trial_id = trial_id
            self._trial_id_to_experiment_id_and_number[trial_id] = (experiment_id, trial.number)
            self._experiments[experiment_id].trials.append(trial)
            self._update_cache(trial_id, experiment_id)
            return trial_id

    def set_trial_state(self, trial_id: int, state: TrialState) -> bool:
        with self._lock:
            trial = self._get_trial(trial_id)
            self.check_trial_is_updatable(trial_id, trial.state)

            trial = copy.copy(trial)
            self.check_trial_is_updatable(trial_id, trial.state)

            if state == TrialState.RUNNING and trial.state != TrialState.WAITING:
                return False

            trial.state = state
            if state.is_finished():
                trial.datetime_complete = datetime.now()
                self._set_trial(trial_id, trial)
                experiment_id = self._trial_id_to_experiment_id_and_number[trial_id][0]
                # 更新best value及best params
                self._update_cache(trial_id, experiment_id)
            else:
                self._set_trial(trial_id, trial)

            return True

    def set_trial_param(
            self,
            trial_id: int,
            param_name: str,
            param_value_internal: float,
            distribution: BaseDistribution
    ) -> None:
        with self._lock:
            trial = self._get_trial(trial_id)
            self.check_trial_is_updatable(trial_id, trial.state)
            experiment_id = self._trial_id_to_experiment_id_and_number[trial_id][0]
            if param_name in self._experiments[experiment_id].param_distribution:
                samples.check_distribution_compatibility(
                    self._experiments[experiment_id].param_distribution[param_name],
                    distribution
                )
        self._experiments[experiment_id].param_distribution[param_name] = distribution

        trial = copy.copy(trial)
        trial.params = copy.copy(trial.params)
        trial.params[param_name] = distribution.to_external_repr(param_value_internal)
        trial.distributions = copy.copy(trial.distributions)
        trial.distributions[param_name] = distribution
        self._set_trial(trial_id, trial)

    def get_trial_number_from_id(
            self,
            trial_id: int
    ) -> int:
        with self._lock:
            self._check_trial_id(trial_id)
            return self._trial_id_to_experiment_id_and_number[trial_id][1]

    def get_best_trial(self, experiment_id: int) -> FrozenTrial:

        with self._lock:
            self._check_experiment_id(experiment_id)

            best_trial_id = self._experiments[experiment_id].best_trial_id
            if best_trial_id is None:
                raise ValueError("No trials are completed yet.")
            return self.get_trial(best_trial_id)

    def get_trial_param(
            self,
            trial_id: int,
            param_name: str
    ) -> float:
        with self._lock:
            trial = self._get_trial(trial_id)
            distribution = trial.distributions[param_name]
            return distribution.to_internal_repr(trial.params[param_name])

    def set_trial_value(self, trial_id: int, value: float) -> None:
        with self._lock:
            trial = self._get_trial(trial_id)
            self.check_trial_is_updatable(trial_id, trial.state)

            trial = copy.copy(trial)
            self.check_trial_is_updatable(trial_id, trial.state)

            trial.value = value
            self._set_trial(trial_id, trial)

    def set_trial_user_attr(
            self,
            trial_id: int,
            key: str,
            value: Any
    ) -> None:
        with self._lock:
            self._check_trial_id(trial_id)
            trial = self._get_trial(trial_id)
            self.check_trial_is_updatable(trial_id, trial.state)

            trial = copy.copy(trial)
            trial.user_attrs = copy.copy(trial.user_attrs)
            trial.user_attrs[key] = value
            self._set_trial(trial_id, trial)

    def set_trial_system_attr(
            self,
            trial_id: int,
            key: str,
            value: Any
    ) -> None:
        with self._lock:
            trial = self._get_trial(trial_id)
            self.check_trial_is_updatable(trial_id, trial.state)

            trial = copy.copy(trial)
            trial.system_attrs = copy.copy(trial.system_attrs)
            trial.system_attrs[key] = value
            self._set_trial(trial_id, trial)

    def _check_experiment_id(self, experiment_id: int) -> None:
        if experiment_id not in self._experiments:
            raise KeyError("No trial with experiment_id {} exists.".format(experiment_id))

    def _get_trial(self, trial_id: int) -> FrozenTrial:
        self._check_trial_id(trial_id)
        experiment_id, trial_number = self._trial_id_to_experiment_id_and_number[trial_id]
        return self._experiments[experiment_id].trials[trial_number]

    def _set_trial(self, trial_id: int, trial: FrozenTrial) -> None:
        experiment_id, trial_number = self._trial_id_to_experiment_id_and_number[trial_id]
        self._experiments[experiment_id].trials[trial_number] = trial

    def _check_trial_id(self, trial_id: int) -> None:
        if trial_id not in self._trial_id_to_experiment_id_and_number:
            raise KeyError("No trial with trial_id {} exists.".format(trial_id))

    @staticmethod
    def _create_running_trial() -> FrozenTrial:
        return FrozenTrial(
            trial_id=1,
            number=-1,
            state=TrialState.RUNNING,
            params={},
            distributions={},
            user_attrs={},
            system_attrs={},
            value=None,
            intermediate_values={},
            datetime_start=datetime.now(),
            datetime_complete=None
        )

    def _update_cache(self, trial_id: int, experiment_id: int) -> None:
        trial = self._get_trial(trial_id)
        if trial.state != TrialState.COMPLETE:
            return

        best_trial_id = self._experiments[experiment_id].best_trial_id
        if best_trial_id is None:
            self._experiments[experiment_id].best_trial_id = trial_id
            return
        best_trial = self._get_trial(best_trial_id)
        assert best_trial is not None
        best_value = best_trial.value
        new_value = trial.value
        if best_value is None:
            self._experiments[experiment_id].best_trial_id = trial_id
            return

        assert new_value is not None

        if self.get_experiment_direction(experiment_id) == ExperimentDirection.MAXIMIZE:
            if best_value < new_value:
                self._experiments[experiment_id].best_trial_id = trial_id
        else:
            if best_value > new_value:
                self._experiments[experiment_id].best_trial_id = trial_id

    def set_trial_intermediate_value(
            self,
            trial_id: int,
            step: int,
            intermediate_value: float
    ) -> None:
        with self._lock:
            trial = self._get_trial(trial_id)
            self.check_trial_is_updatable(trial_id, trial.state)

            trial = copy.copy(trial)
            trial.intermediate_values = copy.copy(trial.intermediate_values)
            trial.intermediate_values[step] = intermediate_value
            self._set_trial(trial_id, trial)

    def get_trial(self, trial_id: int) -> FrozenTrial:
        with self._lock:
            return self._get_trial(trial_id)

    def get_all_trials(self, experiment_id: int, deepcopy: bool = True) -> List[FrozenTrial]:
        with self._lock:
            self._check_experiment_id(experiment_id)
            if deepcopy:
                return copy.deepcopy(self._experiments[experiment_id].trials)
            else:
                return self._experiments[experiment_id].trials

    def get_n_trials(self, experiment_id: int, state: Optional[TrialState] = None) -> int:
        with self._lock:
            self._check_experiment_id(experiment_id)
            if state is None:
                return len(self._experiments[experiment_id].trials)

            return sum(
                trial.state == state for trial in self.get_all_trials(experiment_id, deepcopy=False)
            )

    def read_trials_from_remote_storage(self, experiment_id: int) -> None:
        self._check_experiment_id(experiment_id)
