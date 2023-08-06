"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/9 10:59 上午
@Software: PyCharm
@File    : _cached_storage.py
@E-mail  : victor.xsyang@gmail.com
"""
import copy
import datetime
import threading
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

from opts import samples
from opts._experiment_direction import ExperimentDirection
from opts._experiment_summary import ExperimentSummary
from opts.storages import BaseStorage
from opts.storages._rdb.storage import RDBStorage
from opts.trial import FrozenTrial
from opts.trial import TrialState
from opts.samples import BaseDistribution


class _TrialUpdate:
    def __init__(self) -> None:
        self.state: Optional[TrialState] = None
        self.value: Optional[float] = None
        self.intermediate_values: Dict[int, float] = {}
        self.user_attrs: Dict[str, Any] = {}
        self.system_attrs: Dict[str, Any] = {}
        self.params: Dict[str, Any] = {}
        self.distributions: Dict[str, samples.BaseDistribution] = {}
        self.datetime_complete: Optional[datetime.datetime] = None


class _ExperimentInfo:
    def __init__(self) -> None:
        # Trial number to corresponding FrozenTrial.
        self.trials: Dict[int, FrozenTrial] = {}
        # A list of trials which do not require storage access to read latest attributes.
        self.owned_or_finished_trial_ids: Set[int] = set()
        # Cache any writes which are not reflected to the actual storage yet in updates.
        self.updates: Dict[int, _TrialUpdate] = {}
        # Cache distributions to avoid storage access on distribution consistency check.
        self.param_distribution: Dict[str, samples.BaseDistribution] = {}
        self.direction: ExperimentDirection = ExperimentDirection.NOT_SET
        self.name: Optional[str] = None


class _CachedStorage(BaseStorage):
    def __init__(self, backend: RDBStorage) -> None:
        self._backend = backend
        self._experiments: Dict[int, _ExperimentInfo] = {}
        self._trial_id_to_experiment_id_and_number: Dict[int, Tuple[int, int]] = {}
        self._lock = threading.Lock()

    def __getstate__(self) -> Dict[Any, Any]:
        state = self.__dict__.copy()
        del state["_lock"]
        return state

    def __setstate__(self, state: Dict[Any, Any]) -> None:
        self.__dict__.update(state)
        self._lock = threading.Lock()

    def create_new_experiment(self, experiment_name: Optional[str] = None) -> int:
        experiment_id = self._backend.create_new_experiment(experiment_name)
        with self._lock:
            experiment = _ExperimentInfo()
            experiment.name = experiment_name
            self._experiments[experiment_id] = experiment
        return experiment_id

    def delete_experiment(self, experiment_id: int) -> None:

        with self._lock:
            if experiment_id in self._experiments:
                for trial_id in self._experiments[experiment_id].trials:
                    if trial_id in self._trial_id_to_experiment_id_and_number:
                        del self._trial_id_to_experiment_id_and_number[trial_id]
                del self._experiments[experiment_id]

        self._backend.delete_experiment(experiment_id)

    def set_experiment_direction(self, experiment_id: int, direction: ExperimentDirection) -> None:

        with self._lock:
            if experiment_id in self._experiments:
                current_direction = self._experiments[experiment_id].direction
                if direction == current_direction:
                    return
                elif current_direction == ExperimentDirection.NOT_SET:
                    self._experiments[experiment_id].direction = direction
                    self._backend.set_experiment_direction(experiment_id, direction)
                    return

        self._backend.set_experiment_direction(experiment_id, direction)

    def set_experiment_user_attr(self, experiment_id: int, key: str, value: Any) -> None:
        self._backend.set_experiment_user_attr(experiment_id, key, value)

    def set_experiment_system_attr(self, experiment_id: int, key: str, value: Any) -> None:
        self._backend.set_experiment_system_attr(experiment_id, key, value)

    def get_experiment_id_from_name(self, experiment_name: str) -> int:
        return self._backend.get_experiment_id_from_name(experiment_name)

    def get_experiment_id_from_trial_id(self, trial_id: int) -> int:
        with self._lock:
            if trial_id in self._trial_id_to_experiment_id_and_number:
                return self._trial_id_to_experiment_id_and_number[trial_id][0]

        return self._backend.get_experiment_id_from_trial_id(trial_id)

    def get_experiment_name_from_id(self, experiment_id: int) -> str:
        with self._lock:
            if experiment_id in self._experiments:
                name = self._experiments[experiment_id].name
                if name is not None:
                    return name

        name = self._backend.get_experiment_name_from_id(experiment_id)
        with self._lock:
            if experiment_id not in self._experiments:
                self._experiments[experiment_id] = _ExperimentInfo()
            self._experiments[experiment_id].name = name
        return name

    def get_experiment_direction(self, experiment_id: int) -> ExperimentDirection:
        with self._lock:
            if experiment_id in self._experiments:
                direction = self._experiments[experiment_id].direction
                if direction != ExperimentDirection.NOT_SET:
                    return direction

        direction = self._backend.get_experiment_direction(experiment_id)
        with self._lock:
            if experiment_id not in self._experiments:
                self._experiments[experiment_id] = _ExperimentInfo()
            self._experiments[experiment_id].direction = direction
        return direction

    def get_experiment_user_attrs(self, experiment_id: int) -> Dict[str, Any]:
        return self._backend.get_experiment_user_attrs(experiment_id)

    def get_experiment_system_attrs(self, experiment_id: int) -> Dict[str, Any]:

        return self._backend.get_experiment_system_attrs(experiment_id)

    def get_all_experiment_summaries(self) -> List[ExperimentSummary]:
        return self._backend.get_all_experiment_summaries()

    def create_new_trial(self, experiment_id: int, template_trial: Optional[FrozenTrial] = None) -> int:
        frozen_trial = self._backend._create_new_trial(experiment_id, template_trial)
        trial_id = frozen_trial._trial_id
        with self._lock:
            if experiment_id not in self._experiments:
                self._experiments[experiment_id] = _ExperimentInfo()
            experiment = self._experiments[experiment_id]
            self._add_trials_to_cache(experiment_id, [frozen_trial])
            # Running trials can be modified from only one worker.
            # If the state is RUNNING, since this worker is an owner of the trial, we do not need
            # to access to the storage to get the latest attributes of the trial.
            # Since finished trials will not be modified by any worker, we do not
            # need storage access for them, too.
            # WAITING trials are exception and they can be modified from arbitral worker.
            # Thus, we cannot add them to a list of cached trials.
            if frozen_trial.state != TrialState.WAITING:
                experiment.owned_or_finished_trial_ids.add(frozen_trial._trial_id)
        return trial_id

    def set_trial_state(self, trial_id: int, state: TrialState) -> bool:
        with self._lock:
            cached_trial = self._get_cached_trial(trial_id)
            if cached_trial is not None:
                self._check_trial_is_updatable(cached_trial)
                updates = self._get_updates(trial_id)
                cached_trial.state = state
                updates.state = state
                if cached_trial.state.is_finished():
                    updates.datetime_complete = datetime.datetime.now()
                    cached_trial.datetime_complete = datetime.datetime.now()
                return self._flush_trial(trial_id)

        ret = self._backend.set_trial_state(trial_id, state)
        if (
            ret
            and state == TrialState.RUNNING
            and trial_id in self._trial_id_to_experiment_id_and_number
        ):
            # Cache when the local thread pop WAITING trial and start evaluation.
            with self._lock:
                experiment_id, _ = self._trial_id_to_experiment_id_and_number[trial_id]
                self._add_trials_to_cache(experiment_id, [self._backend.get_trial(trial_id)])
                self._experiments[experiment_id].owned_or_finished_trial_ids.add(trial_id)
        return ret

    def set_trial_param(
            self,
            trial_id: int,
            param_name: str,
            param_value_internal: float,
            distribution: BaseDistribution
    ) -> None:
        with self._lock:
            cached_trial = self._get_cached_trial(trial_id)
            if cached_trial is not None:
                self._check_trial_is_updatable(cached_trial)

                experiment_id, _ = self._trial_id_to_experiment_id_and_number[trial_id]
                cached_dist = self._experiments[experiment_id].param_distribution.get(param_name, None)
                if cached_dist:
                    samples.check_distribution_compatibility(cached_dist, distribution)
                else:
                    # On cache miss, check compatibility against previous trials in the database
                    # and INSERT immediately to prevent other processes from creating incompatible
                    # ones. By INSERT, it is assumed that no previous entry has been persisted
                    # already.
                    self._backend._check_and_set_param_distribution(
                        experiment_id, trial_id, param_name, param_value_internal, distribution
                    )
                    self._experiments[experiment_id].param_distribution[param_name] = distribution

                params = copy.copy(cached_trial.params)
                params[param_name] = distribution.to_external_repr(param_value_internal)
                cached_trial.params = params

                dists = copy.copy(cached_trial.distributions)
                dists[param_name] = distribution
                cached_trial.distributions = dists

                if cached_dist:  # Already persisted in case of cache miss so no need to update.
                    updates = self._get_updates(trial_id)
                    updates.params[param_name] = param_value_internal
                    updates.distributions[param_name] = distribution
                return

        self._backend.set_trial_param(trial_id, param_name, param_value_internal, distribution)

    def get_trial_number_from_id(self, trial_id: int) -> int:

        return self.get_trial(trial_id).number

    def get_best_trial(self, experiment_id: int) -> FrozenTrial:

        return self._backend.get_best_trial(experiment_id)

    def get_trial_param(self, trial_id: int, param_name: str) -> float:

        trial = self.get_trial(trial_id)
        return trial.distributions[param_name].to_internal_repr(trial.params[param_name])

    def set_trial_value(self, trial_id: int, value: float) -> None:

        with self._lock:
            cached_trial = self._get_cached_trial(trial_id)
            if cached_trial is not None:
                self._check_trial_is_updatable(cached_trial)
                updates = self._get_updates(trial_id)
                cached_trial.value = value
                updates.value = value
                return

        self._backend._update_trial(trial_id, value=value)

    def set_trial_intermediate_value(
        self, trial_id: int, step: int, intermediate_value: float
    ) -> None:

        with self._lock:
            cached_trial = self._get_cached_trial(trial_id)
            if cached_trial is not None:
                self._check_trial_is_updatable(cached_trial)
                updates = self._get_updates(trial_id)
                intermediate_values = copy.copy(cached_trial.intermediate_values)
                intermediate_values[step] = intermediate_value
                cached_trial.intermediate_values = intermediate_values
                updates.intermediate_values[step] = intermediate_value
                self._flush_trial(trial_id)
                return

        self._backend.set_trial_intermediate_value(trial_id, step, intermediate_value)

    def set_trial_user_attr(self, trial_id: int, key: str, value: Any) -> None:

        with self._lock:
            cached_trial = self._get_cached_trial(trial_id)
            if cached_trial is not None:
                self._check_trial_is_updatable(cached_trial)
                updates = self._get_updates(trial_id)
                attrs = copy.copy(cached_trial.user_attrs)
                attrs[key] = value
                cached_trial.user_attrs = attrs
                updates.user_attrs[key] = value
                self._flush_trial(trial_id)
                return

        self._backend._update_trial(trial_id, user_attrs={key: value})

    def set_trial_system_attr(self, trial_id: int, key: str, value: Any) -> None:

        with self._lock:
            cached_trial = self._get_cached_trial(trial_id)
            if cached_trial is not None:
                self._check_trial_is_updatable(cached_trial)
                updates = self._get_updates(trial_id)
                attrs = copy.copy(cached_trial.system_attrs)
                attrs[key] = value
                cached_trial.system_attrs = attrs
                updates.system_attrs[key] = value
                self._flush_trial(trial_id)
                return

        self._backend._update_trial(trial_id, system_attrs={key: value})

    def _get_cached_trial(self, trial_id: int) -> Optional[FrozenTrial]:
        if trial_id not in self._trial_id_to_experiment_id_and_number:
            return None
        experiment_id, number = self._trial_id_to_experiment_id_and_number[trial_id]
        experiment = self._experiments[experiment_id]
        return experiment.trials[number] if trial_id in experiment.owned_or_finished_trial_ids else None

    def _get_updates(self, trial_id: int) -> _TrialUpdate:
        experiment_id, number = self._trial_id_to_experiment_id_and_number[trial_id]
        updates = self._experiments[experiment_id].updates.get(number, None)
        if updates is not None:
            return updates
        updates = _TrialUpdate()
        self._experiments[experiment_id].updates[number] = updates
        return updates

    def get_trial(self, trial_id: int) -> FrozenTrial:

        with self._lock:
            trial = self._get_cached_trial(trial_id)
            if trial is not None:
                return trial

        return self._backend.get_trial(trial_id)

    def get_all_trials(self, experiment_id: int, deepcopy: bool = True) -> List[FrozenTrial]:
        if experiment_id not in self._experiments:
            self.read_trials_from_remote_storage(experiment_id)

        with self._lock:
            experiment = self._experiments[experiment_id]
            # We need to sort trials by their number because some samplers assume this behavior.
            # The following two lines are latency-sensitive.
            trials = list(sorted(experiment.trials.values(), key=lambda t: t.number))
            return copy.deepcopy(trials) if deepcopy else trials

    def read_trials_from_remote_storage(self, experiment_id: int) -> None:
        with self._lock:
            if experiment_id not in self._experiments:
                self._experiments[experiment_id] = _ExperimentInfo()
            experiment = self._experiments[experiment_id]
            trials = self._backend._get_trials(
                experiment_id, excluded_trial_ids=experiment.owned_or_finished_trial_ids
            )
            if trials:
                self._add_trials_to_cache(experiment_id, trials)
                for trial in trials:
                    if trial.state.is_finished():
                        experiment.owned_or_finished_trial_ids.add(trial._trial_id)

    def _flush_trial(self, trial_id: int) -> bool:
        if trial_id not in self._trial_id_to_experiment_id_and_number:
            # The trial has not been managed by this class.
            return True
        experiment_id, number = self._trial_id_to_experiment_id_and_number[trial_id]
        experiment = self._experiments[experiment_id]
        updates = experiment.updates.get(number, None)
        if updates is None:
            # The trial is up-to-date.
            return True
        del experiment.updates[number]
        return self._backend._update_trial(
            trial_id=trial_id,
            value=updates.value,
            intermediate_values=updates.intermediate_values,
            state=updates.state,
            params=updates.params,
            distributions_=updates.distributions,
            user_attrs=updates.user_attrs,
            system_attrs=updates.system_attrs,
            datetime_complete=updates.datetime_complete,
        )

    def _add_trials_to_cache(self, experiment_id: int, trials: List[FrozenTrial]) -> None:
        experiment = self._experiments[experiment_id]
        for trial in trials:
            self._trial_id_to_experiment_id_and_number[trial._trial_id] = (
                experiment_id,
                trial.number,
            )
            experiment.trials[trial.number] = trial

    @staticmethod
    def _check_trial_is_updatable(trial: FrozenTrial) -> None:
        if trial.state.is_finished():
            raise RuntimeError(
                "Trial#{} has already finished and can not be updated.".format(trial.number)
            )
