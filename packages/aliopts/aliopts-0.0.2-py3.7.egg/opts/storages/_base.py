"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/28 2:33 下午
@Software: PyCharm
@File    : _base.py
@E-mail  : victor.xsyang@gmail.com
"""
import abc
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from opts._experiment_direction import ExperimentDirection
from opts._experiment_summary import ExperimentSummary
from opts.samples import BaseDistribution
from opts.trial import FrozenTrial
from opts.trial import TrialState

DEFAULT_EXPERIMENT_NAME_PREFIX = "no-name-"


class BaseStorage(object, metaclass=abc.ABCMeta):
    """Base class for storages.

    """

    @abc.abstractmethod
    def create_new_experiment(self, experiment_name: Optional[str] = None) -> int:
        """Create a new experiment from a name.

        :param experiment_name:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_experiment(self, experiment_id: int) -> None:
        """Delete a experiment.

        :param experiment_id:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_experiment_user_attr(self, experiment_id: int, key: str, value: Any) -> None:
        """

        :param experiment_id:
        :param key:
        :param value:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_experiment_system_attr(self, experiment_id: int, key: str, value: Any) -> None:
        """Register an opts-internal attribute to a experiment.

        :param experiment_id:
        :param key:
        :param value:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_experiment_direction(self, experiment_id: int, direction: ExperimentDirection) -> None:
        """Register an optimization problem direction to a experiment.

        :param experiment_id:
        :param direction:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_experiment_id_from_name(self, experiment_name: str) -> int:
        """Read the ID of a experiment.

        :param experiment_name:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_experiment_id_from_trial_id(self, trial_id: int) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_experiment_name_from_id(self, experiment_id: int) -> str:
        """Read the experiment name of a experiment.

        :param experiment_id:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_experiment_direction(self, experiment_id: int) -> ExperimentDirection:
        """Read whether a experiment maximizes or minimizes an objective.

        :param experiment_id:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_experiment_user_attrs(self, experiment_id: int) -> Dict[str, Any]:
        """Read the user-defined attributes of a experiment.

        :param experiment_id:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_experiment_system_attrs(self, experiment_id: int) -> Dict[str, Any]:
        """Read the opts-internal attributes of a experiment.

        :param experiment_id:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_experiment_summaries(self) -> List[ExperimentSummary]:
        """Read a list of :class: `opts.experiment.Experiment` objects.

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create_new_trial(self, experiment_id: int, template_trial: Optional[FrozenTrial] = None) -> int:
        """Create and add a new trial to a experiment.

        :param experiment_id:
        :param template_trial:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_trial_state(self, trial_id: int, state: TrialState) -> bool:
        """Update state of a trial

        :param trial_id:
        :param state:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_trial_param(
            self,
            trial_id: int,
            param_name: str,
            param_value_internal: float,
            distribution: BaseDistribution
    ) -> None:
        """Set a parameter to trial.

        :param trial_id:
        :param param_name:
        :param param_value_internal:
        :param distribution:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_trial_number_from_id(
            self,
            trial_id: int
    ) -> int:
        """Read the trial number of a trial.

        :param trial_id:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_trial_param(
            self,
            trial_id: int,
            param_name: str
    ) -> float:
        """Read the parameter of a trial.

        :param trial_id:
        :param param_name:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_trial_value(self, trial_id: int, value: float) -> None:
        """Set a return value of an objective function.

        :param trial_id:
        :param value:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_trial_intermediate_value(
            self,
            trial_id: int,
            step: int,
            intermediate_value: float
    ) -> None:
        """Report an intermediate value of an objective function.


        :param trial_id:
        :param step:
        :param intermediate_value:
        :return:
        """

    @abc.abstractmethod
    def set_trial_user_attr(
            self,
            trial_id: int,
            key: str,
            value: Any
    ) -> None:
        """Set a user-defined attribute to a trial.

        :param trial_id:
        :param key:
        :param value:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_trial_system_attr(
            self,
            trial_id: int,
            key: str,
            value: Any
    ) -> None:
        """Set an opts-internal attribute to a trial.

        :param trial_id:
        :param key:
        :param value:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_trial(self, trial_id: int) -> FrozenTrial:
        """Read a trial.

        :param trial_id:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_trials(self, experiment_id: int, deepcopy: bool = True) -> List[FrozenTrial]:
        """Read all trials in a experiment.

        :param experiment_id:
        :param deepcopy:
        :return:
        """
        raise NotImplementedError

    def get_n_trials(self, experiment_id: int, state: Optional[TrialState] = None) -> int:
        """Count the number of trials in a experiment.

        :param experiment_id:
        :param state:
        :return:
        """
        if state is None:
            return len(self.get_all_trials(experiment_id, deepcopy=False))

        return len([t for t in self.get_all_trials(experiment_id, deepcopy=False) if t.state == state])

    def get_best_trial(self, experiment_id: int) -> FrozenTrial:
        """Return the trial with the best value in a experiment.

        :param experiment_id:
        :return:
        """
        all_trials = self.get_all_trials(experiment_id, deepcopy=False)
        all_trials = [t for t in all_trials if t.state is TrialState.COMPLETE]

        if len(all_trials) == 0:
            raise ValueError("No trials are completed yet.")

        if self.get_experiment_direction(experiment_id) == ExperimentDirection.MAXIMIZE:
            best_trial = max(all_trials, key=lambda t: t.value)
        else:
            best_trial = min(all_trials, key=lambda t: t.value)

        return best_trial

    def get_trial_params(self, trial_id: int) -> Dict[str, Any]:
        """Read the paramter dictionary of a trial.

        :param trial_id:
        :return:
        """
        return self.get_trial(trial_id).params

    def get_trial_user_attrs(self, trial_id: int) -> Dict[str, Any]:
        """Read the user-defined attributes of a trial.

        :param trial_id:
        :return:
        """
        return self.get_trial(trial_id).user_attrs

    def get_trial_system_attrs(self, trial_id: int) -> Dict[str, Any]:
        """

        :param trial_id:
        :return:
        """
        return self.get_trial(trial_id).system_attrs

    def read_trials_from_remote_storage(self, experiment_id: int) -> None:
        """Make an internal cache of trials up-to-date.

        :param experiment_id:
        :return:
        """
        raise NotImplementedError

    def remove_session(self) -> None:
        """Clean up all connections to a database.

        :return:
        """
        pass

    def check_trial_is_updatable(self, trial_id: int, trial_state: TrialState) -> None:
        """Check whether a trial state is updatable.

        :param trial_id:
        :param trial_state:
        :return:
        """
        if trial_state.is_finished():
            trial = self.get_trial(trial_id)
            raise RuntimeError(
                "Trial#{} has already finished and can not be updated.".format(trial.number)
            )
