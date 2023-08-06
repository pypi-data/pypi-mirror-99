"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/2 3:20 下午
@Software: PyCharm
@File    : _redis.py
@E-mail  : victor.xsyang@gmail.com
"""
import copy
from datetime import datetime
import pickle
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import opts
from opts import samples
from opts import errors
from opts._experimental import experimental
from opts._imports import try_import
from opts._experiment_direction import ExperimentDirection
from opts._experiment_summary import ExperimentSummary
from opts.storages import BaseStorage
from opts.storages._base import DEFAULT_EXPERIMENT_NAME_PREFIX
from opts.trial import FrozenTrial
from opts.trial import TrialState
from opts.samples import BaseDistribution

_logger = opts.logger.get_logger(__name__)

with try_import() as _imports:
    import redis


@experimental("1.4.0")
class RedisStorage(BaseStorage):
    """Storage class for Redis backend.

    """

    def __init__(self, url: str) -> None:
        _imports.check()
        self._url = url
        self._redis = redis.Redis.from_url(url)

    def create_new_experiment(self, experiment_name: Optional[str] = None) -> int:
        if experiment_name is not None and self._redis.exists(self._key_experiment_name(experiment_name)):
            raise errors.DuplicatedExperimentError

        if not self._redis.exists("experiment_counter"):
            self._redis.set("experiment_counter", -1)
        experiment_id = self._redis.incr("experiment_counter", 1)
        self._redis.set("experiment_id:{:010d}:trial_number".format(experiment_id), -1)

        if experiment_name is None:
            experiment_name = "{}{:010d}".format(DEFAULT_EXPERIMENT_NAME_PREFIX, experiment_id)

        with self._redis.pipeline() as pipe:
            pipe.multi()
            pipe.set(self._key_experiment_name(experiment_name), pickle.dumps(experiment_id))
            pipe.set("experiment_id:{:010d}:experiment_name".format(experiment_id), pickle.dumps(experiment_name))
            pipe.set(
                "experiment_id:{:010d}:direction".format(experiment_id),
                pickle.dumps(ExperimentDirection.NOT_SET)
            )
            experiment_summary = ExperimentSummary(
                experiment_name=experiment_name,
                direction=ExperimentDirection.NOT_SET,
                best_trial=None,
                user_attrs={},
                system_attrs={},
                n_trials=0,
                datetime_start=None,
                experiment_id=experiment_id
            )
            pipe.rpush("experiment_list", pickle.dumps(experiment_id))
            pipe.set(self._key_experiment_summary(experiment_id), pickle.dumps(experiment_summary))
            pipe.execute()
        _logger.info("A new experiment created in Redis with name:{}".format(experiment_name))
        return experiment_id

    def delete_experiment(self, experiment_id: int) -> None:
        self._check_experiment_id(experiment_id)
        with self._redis.pipeline() as pipe:
            pipe.multi()
            pipe.delete(self._key_experiment_summary(experiment_id))
            pipe.lrem("experiment_list", 0, pickle.dumps(experiment_id))

            trial_ids = self._get_experiment_trials(experiment_id)
            for trial_id in trial_ids:
                pipe.delete("trial_id:{:010d}:frozentrial".format(trial_id))
                pipe.delete("trial_id:{:010d}:experiment_id".format(trial_id))
            pipe.delete("experiment_id:{:010d}:trial_list".format(experiment_id))
            pipe.delete("experiment_id:{:010d}:trial_number".format(experiment_id))

            experiment_name = self.get_experiment_name_from_id(experiment_id)
            pipe.delete("experiment_name:{}:experiment_id".format(experiment_name))
            pipe.delete("experiment_id:{:010d}:experiment_name".format(experiment_id))
            pipe.delete("experiment_id:{:010d}:direction".format(experiment_id))
            pipe.delete("experiment_id:{:010d}:best_trial_id".format(experiment_id))
            pipe.delete("experiment_id:{:010d}:params_distribution".format(experiment_id))
            pipe.execute()

    def _set_experiment_summary(self, experiment_id: int, experiment_summary: ExperimentSummary) -> None:
        self._redis.set(self._key_experiment_summary(experiment_id), pickle.dumps(experiment_summary))

    def _get_experiment_summary(self, experiment_id: int) -> ExperimentSummary:
        summary_pkl = self._redis.get(self._key_experiment_summary(experiment_id))
        assert summary_pkl is not None
        return pickle.loads(summary_pkl)

    def _del_experiment_summary(self, experiment_id: int) -> None:
        self._redis.delete(self._key_experiment_summary(experiment_id))

    def _get_experiment_trials(self, experiment_id: int) -> List[int]:
        self._check_experiment_id(experiment_id)
        experiment_trial_list_key = "experiment_id:{:010d}:trial_list".format(experiment_id)
        return [int(tid) for tid in self._redis.lrange(experiment_trial_list_key, 0, -1)]

    def get_all_trials(self, experiment_id: int, deepcopy: bool = True) -> List[FrozenTrial]:
        self._check_experiment_id(experiment_id)
        trials = []
        trial_ids = self._get_experiment_trials(experiment_id)
        for trial_id in trial_ids:
            frozen_trial = self.get_trial(trial_id)
            trials.append(frozen_trial)

        if deepcopy:
            return copy.deepcopy(trials)
        else:
            return trials

    def read_trials_from_remote_storage(self, experiment_id: int) -> None:
        self._check_experiment_id(experiment_id)

    def _check_experiment_id(self, experiment_id: int) -> None:
        if not self._redis.exists("experiment_id:{:010d}:experiment_name".format(experiment_id)):
            raise KeyError("experiment_id {} does not exist.".format(experiment_id))

    def _check_trial_id(self, trial_id: int) -> None:
        if not self._redis.exists(self._key_trial(trial_id)):
            raise KeyError("trial_id {} does not exist.".format(trial_id))

    def get_trial(self, trial_id: int) -> FrozenTrial:
        self._check_trial_id(trial_id)
        frozen_trial_pkl = self._redis.get(self._key_trial(trial_id))
        assert frozen_trial_pkl is not None
        return pickle.loads(frozen_trial_pkl)



    def set_experiment_direction(self, experiment_id: int, direction: ExperimentDirection) -> None:
        self._check_experiment_id(experiment_id)
        if self._redis.exists(self._key_experiment_direction(experiment_id)):
            direction_pkl = self._redis.get(self._key_experiment_direction(experiment_id))
            assert direction_pkl is not None
            current_direction = pickle.loads(direction_pkl)
            if current_direction != ExperimentDirection.NOT_SET and current_direction != direction:
                raise ValueError(
                    "Cannot overwrite experiment direction from {} to {}.".format(
                        current_direction, direction
                    )
                )

        with self._redis.pipeline() as pipe:
            pipe.multi()
            pipe.set(self._key_experiment_direction(experiment_id), pickle.dumps(direction))
            experiment_summary = self._get_experiment_summary(experiment_id)
            experiment_summary.direction = direction
            pipe.set(self._key_experiment_summary(experiment_id), pickle.dumps(experiment_summary))
            pipe.execute()

    def set_experiment_user_attr(self, experiment_id: int, key: str, value: Any) -> None:
        self._check_experiment_id(experiment_id)
        experiment_summary = self._get_experiment_summary(experiment_id)
        experiment_summary.user_attrs[key] = value
        self._set_experiment_summary(experiment_id, experiment_summary)

    def set_experiment_system_attr(self, experiment_id: int, key: str, value: Any) -> None:
        self._check_experiment_id(experiment_id)
        experiment_summary = self._get_experiment_summary(experiment_id)
        experiment_summary.system_attrs[key] = value
        self._set_experiment_summary(experiment_id, experiment_summary)

    def get_experiment_id_from_name(self, experiment_name: str) -> int:
        if not self._redis.exists(self._key_experiment_name(experiment_name)):
            raise KeyError("No such experiment {}".format(experiment_name))
        experiment_id_pkl = self._redis.get(self._key_experiment_name(experiment_name))
        assert experiment_id_pkl is not None
        return pickle.loads(experiment_id_pkl)

    def get_experiment_id_from_trial_id(self, trial_id: int) -> int:
        experiment_id_pkl = self._redis.get("trial_id:{:010d}:experiment_id".format(trial_id))
        if experiment_id_pkl is None:
            raise KeyError("No such trial: {}".format(trial_id))
        return pickle.loads(experiment_id_pkl)

    def get_experiment_name_from_id(self, experiment_id: int) -> str:
        self._check_experiment_id(experiment_id)
        experiment_name_pkl = self._redis.get("experiment_id:{:010d}:experiment_name".format(experiment_id))
        if experiment_name_pkl is None:
            raise KeyError("No such experiment: {}.".format(experiment_id))
        return pickle.loads(experiment_name_pkl)

    def get_experiment_direction(self, experiment_id: int) -> ExperimentDirection:
        direction_pkl = self._redis.get("experiment_id:{:010d}:direction".format(experiment_id))
        if direction_pkl is None:
            raise KeyError("No such experiment: {}.".format(experiment_id))
        return pickle.loads(direction_pkl)

    def get_experiment_user_attrs(self, experiment_id: int) -> Dict[str, Any]:
        self._check_experiment_id(experiment_id)
        experiment_summary = self._get_experiment_summary(experiment_id)
        return copy.deepcopy(experiment_summary.user_attrs)

    def get_experiment_system_attrs(self, experiment_id: int) -> Dict[str, Any]:
        self._check_experiment_id(experiment_id)
        experiment_summary = self._get_experiment_summary(experiment_id)
        return copy.deepcopy(experiment_summary.system_attrs)

    def _get_experiment_param_distribution(self, experiment_id: int) -> Dict:
        if self._redis.exists(self._key_experiment_param_distribution(experiment_id)):
            param_distribution_pkl = self._redis.get(self._key_experiment_param_distribution(experiment_id))
            assert param_distribution_pkl is not None
            return pickle.loads(param_distribution_pkl)
        else:
            return {}

    def _set_experiment_param_distribution(self, experiment_id: int, param_distribution: Dict) -> None:
        self._redis.set(
            self._key_experiment_param_distribution(experiment_id), pickle.dumps(param_distribution)
        )

    def get_all_experiment_summaries(self) -> List[ExperimentSummary]:
        experiment_summaries = []
        experiment_ids = [pickle.loads(sid) for sid in self._redis.lrange("experiment_list", 0, -1)]
        for experiment_id in experiment_ids:
            experiment_summary = self._get_experiment_summary(experiment_id)
            experiment_summaries.append(experiment_summary)
        return experiment_summaries

    def create_new_trial(self, experiment_id: int, template_trial: Optional[FrozenTrial] = None) -> int:
        self._check_experiment_id(experiment_id)
        if template_trial is None:
            trial = self._create_running_trial()
        else:
            trial = copy.deepcopy(template_trial)

        if not self._redis.exists("trial_counter"):
            self._redis.set("trial_counter", -1)

        trial_id = self._redis.incr("trial_counter", 1)
        trial_number = self._redis.incr("experiment_id:{:010d}:trial_number".format(experiment_id))
        trial.number = trial_number
        trial._trial_id = trial_id

        with self._redis.pipeline() as pipe:
            pipe.multi()
            pipe.set(self._key_trial(trial_id), pickle.dumps(trial))
            pipe.set("trial_id:{:010d}:experiment_id".format(trial_id), pickle.dumps(experiment_id))
            pipe.rpush("experiment_id:{:010d}:trial_list".format(experiment_id), trial_id)
            pipe.execute()

            pipe.multi()
            experiment_summary = self._get_experiment_summary(experiment_id)
            experiment_summary.n_trials = len(self._get_experiment_trials(experiment_id))
            min_datetime_start = min([t.datetime_start for t in self.get_all_trials(experiment_id)])
            experiment_summary.datetime_start = min_datetime_start
            pipe.set(self._key_experiment_summary(experiment_id), pickle.dumps(experiment_summary))
            pipe.execute()

        if trial.state.is_finished():
            self._update_cache(trial_id)
        return trial_id

    def set_trial_state(self, trial_id: int, state: TrialState) -> bool:
        self._check_trial_id(trial_id)
        trial = self.get_trial(trial_id)
        self.check_trial_is_updatable(trial_id, trial.state)
        if state == TrialState.RUNNING and trial.state != TrialState.WAITING:
            return False

        trial.state = state
        if state.is_finished():
            trial.datetime_complete = datetime.now()
            self._redis.set(self._key_trial(trial_id), pickle.dumps(trial))
            self._update_cache(trial_id)
        else:
            self._redis.set(self._key_trial(trial_id), pickle.dumps(trial))
        return True

    def set_trial_param(
            self,
            trial_id: int,
            param_name: str,
            param_value_internal: float,
            distribution: BaseDistribution
    ) -> None:
        self._check_trial_id(trial_id)
        self.check_trial_is_updatable(trial_id, self.get_trial(trial_id).state)
        experiment_id = self.get_experiment_id_from_trial_id(trial_id)
        param_distribution = self._get_experiment_param_distribution(experiment_id)
        if param_name in param_distribution:
            samples.check_distribution_compatibility(
                param_distribution[param_name],
                distribution
            )
        trial = self.get_trial(trial_id)
        with self._redis.pipeline() as pipe:
            pipe.multi()
            param_distribution[param_name] = distribution
            pipe.set(
                self._key_experiment_param_distribution(experiment_id),
                pickle.dumps(param_distribution)
            )
            trial.params[param_name] = distribution.to_external_repr(param_value_internal)
            trial.distributions[param_name] = distribution
            pipe.set(self._key_trial(trial_id), pickle.dumps(trial))
            pipe.execute()

    def get_trial_number_from_id(
            self,
            trial_id: int
    ) -> int:
        return self.get_trial(trial_id).number

    @staticmethod
    def _create_running_trial() -> FrozenTrial:
        return FrozenTrial(
            trial_id=-1,
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

    def _update_cache(self, trial_id: int) -> None:
        trial = self.get_trial(trial_id)
        if trial.state != TrialState.COMPLETE:
            return
        experiment_id = self.get_experiment_id_from_trial_id(trial_id)
        if not self._redis.exists("experiment_id:{:010d}:best_trial_id".format(experiment_id)):
            self._set_best_trial(experiment_id, trial_id)
            return

        best_value_or_none = self.get_best_trial(experiment_id).value
        assert best_value_or_none is not None
        assert trial.value is not None
        best_value = float(best_value_or_none)
        new_value = float(trial.value)

        assert new_value is not None

        if self.get_experiment_direction(experiment_id) == ExperimentDirection.MAXIMIZE:
            if new_value > best_value:
                self._set_best_trial(experiment_id, trial_id)
        else:
            if new_value < best_value:
                self._set_best_trial(experiment_id, trial_id)
        return

    def set_trial_intermediate_value(
            self,
            trial_id: int,
            step: int,
            intermediate_value: float
    ) -> None:
        self._check_trial_id(trial_id)
        frozen_trial = self.get_trial(trial_id)
        self.check_trial_is_updatable(trial_id, frozen_trial.state)
        frozen_trial.intermediate_values[step] = intermediate_value
        self._set_trial(trial_id, frozen_trial)

    def _set_trial(self, trial_id: int, trial: FrozenTrial) -> None:
        self._redis.set(self._key_trial(trial_id), pickle.dumps(trial))

    def _del_trial(self, trial_id: int) -> None:
        with self._redis.pipeline() as pipe:
            pipe.multi()
            pipe.delete(self._key_trial(trial_id))
            pipe.delete("trial_id:{:010d}:experiment_id".format(trial_id))
            pipe.execute()

    def _get_experiment_trials(self, experiment_id: int) -> List[int]:
        self._check_experiment_id(experiment_id)
        experiment_trial_list_key = "experiment_id:{:010d}:trial_list".format(experiment_id)
        return [int(tid) for tid in self._redis.lrange(experiment_trial_list_key, 0, -1)]


    def set_trial_user_attr(
            self,
            trial_id: int,
            key: str,
            value: Any
    ) -> None:
        self._check_trial_id(trial_id)
        trial = self.get_trial(trial_id)
        self.check_trial_is_updatable(trial_id, trial.state)
        trial.user_attrs[key] = value
        self._set_trial(trial_id, trial)

    def set_trial_system_attr(
            self,
            trial_id: int,
            key: str,
            value: Any
    ) -> None:
        self._check_trial_id(trial_id)
        trial = self.get_trial(trial_id)
        self.check_trial_is_updatable(trial_id, trial.state)
        trial.system_attrs[key] = value
        self._set_trial(trial_id, trial)


    def get_best_trial(self, experiment_id: int) -> FrozenTrial:
        if not self._redis.exists(self._key_best_trial(experiment_id)):
            all_trials = self.get_all_trials(experiment_id, deepcopy=False)
            all_trials = [t for t in all_trials if t.state is TrialState.COMPLETE]
            if len(all_trials) == 0:
                raise ValueError("No trials are completed yet.")

            if self.get_experiment_direction(experiment_id) == ExperimentDirection.MAXIMIZE:
                best_trial = max(all_trials, key=lambda  t: t.value)
            else:
                best_trial = min(all_trials, key=lambda t: t.value)

            self._set_best_trial(experiment_id, best_trial.number)
        else:
            best_trial_id_pkl = self._redis.get(self._key_best_trial(experiment_id))
            assert best_trial_id_pkl is not None
            best_trial_id = pickle.loads(best_trial_id_pkl)
            best_trial = self.get_trial(best_trial_id)
        return best_trial

    def get_trial_param(
            self,
            trial_id: int,
            param_name: str
    ) -> float:
        distribution = self.get_trial(trial_id).distributions[param_name]
        return distribution.to_internal_repr(self.get_trial(trial_id).params[param_name])

    def set_trial_value(self, trial_id: int, value: float) -> None:
        self._check_trial_id(trial_id)
        trial = self.get_trial(trial_id)
        self.check_trial_is_updatable(trial_id, trial.state)

        trial.value = value
        self._redis.set(self._key_trial(trial_id), pickle.dumps(trial))


    def _set_best_trial(self, experiment_id: int, trial_id: int) -> None:
        with self._redis.pipeline() as pipe:
            pipe.multi()
            pipe.set(self._key_best_trial(experiment_id), pickle.dumps(trial_id))

            experiment_summary = self._get_experiment_summary(experiment_id)
            experiment_summary.best_trial = self.get_trial(trial_id)
            pipe.set(self._key_experiment_summary(experiment_id), pickle.dumps(experiment_summary))
            pipe.execute()


    @staticmethod
    def _key_best_trial(experiment_id: int) -> str:
        return "experiment_id:{:010d}:best_trial_id".format(experiment_id)


    @staticmethod
    def _key_experiment_param_distribution(experiment_id: int) -> str:
        return "experiment_id:{:010d}:params_distribution".format(experiment_id)



    @staticmethod
    def _key_experiment_direction(experiment_id: int) -> str:
        return "experiment_id:{:010d}:direction".format(experiment_id)


    @staticmethod
    def _key_experiment_name(experiment_name: str) -> str:
        return "experiment_name:{}:experiment_id".format(experiment_name)

    @staticmethod
    def _key_experiment_summary(experiment_id: int) -> str:
        return "experiment_id:{:010d}:experiment_summary".format(experiment_id)

    @staticmethod
    def _key_trial(trial_id: int) -> str:
        return "trial_id:{:010d}:frozentrial".format(trial_id)

    def _check_experiment_id(self, experiment_id: int) -> None:
        if not self._redis.exists("experiment_id:{:010d}:experiment_name".format(experiment_id)):
            raise KeyError("experiment_id {} does not exist.".format(experiment_id))

    def _check_trial_id(self, trial_id: int) -> None:
        if not self._redis.exists(self._key_trial(trial_id)):
            raise KeyError("experiment_id {} does not exist.".format(trial_id))
