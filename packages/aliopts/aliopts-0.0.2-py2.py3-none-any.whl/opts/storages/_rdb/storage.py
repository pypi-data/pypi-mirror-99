"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/22 10:39 上午
@Software: PyCharm
@File    : storage.py
@E-mail  : victor.xsyang@gmail.com
"""

import copy
from datetime import datetime
import json
import logging
import os
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
import uuid
import weakref

import alembic.command
import alembic.config
import alembic.migration
import alembic.script
from sqlalchemy import orm
from sqlalchemy.engine import create_engine
from sqlalchemy.engine import Engine  # NOQA
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import functions

import opts
from opts import samples
from opts import version
from opts._experiment_direction import ExperimentDirection
from opts._experiment_summary import ExperimentSummary
from opts.storages._base import BaseStorage
from opts.storages._base import DEFAULT_EXPERIMENT_NAME_PREFIX
from opts.storages._rdb import models
from opts.trial import FrozenTrial
from opts.trial import TrialState



_logger = opts.logger.get_logger(__name__)

class RDBStorage(BaseStorage):
    """Storage class for RDB backend.

    """
    def __init__(
            self,
            url: str,
            engine_kwargs: Optional[Dict[str, Any]] = None,
            skip_compatibility_check: bool = False
    ) -> None:
        self.engine_kwargs = engine_kwargs or {}
        self.url = self._fill_storage_url_template(url)
        self.skip_compatibility_check = skip_compatibility_check

        self._set_default_engine_kwargs_for_mysql(url, self.engine_kwargs)

        try:
            self.engine = create_engine(self.url, **self.engine_kwargs)
        except ImportError as e:
            raise ImportError(
                "Failed to import DB access module for the specified storage URL. "
                "Please install appropriate one."
            ) from e

        self.scoped_session = orm.scoped_session(orm.sessionmaker(bind=self.engine))
        models.BaseModel.metadata.create_all(self.engine)

        self._version_manager = _VersionManager(self.url, self.engine, self.scoped_session)
        if not skip_compatibility_check:
            self._version_manager.check_table_schema_compatibility()

        weakref.finalize(self, self._finalize)

    def __getstate__(self) -> Dict[Any, Any]:

        state = self.__dict__.copy()
        del state["scoped_session"]
        del state["engine"]
        del state["_version_manager"]
        return state

    def __setstate__(self, state: Dict[Any, Any]) -> None:

        self.__dict__.update(state)
        try:
            self.engine = create_engine(self.url, **self.engine_kwargs)
        except ImportError as e:
            raise ImportError(
                "Failed to import DB access module for the specified storage URL. "
                "Please install appropriate one."
            ) from e

        self.scoped_session = orm.scoped_session(orm.sessionmaker(bind=self.engine))
        models.BaseModel.metadata.create_all(self.engine)
        self._version_manager = _VersionManager(self.url, self.engine, self.scoped_session)
        if not self.skip_compatibility_check:
            self._version_manager.check_table_schema_compatibility()

    def create_new_experiment(self, experiment_name: Optional[str] = None) -> int:

        session = self.scoped_session()

        if experiment_name is None:
            experiment_name = self._create_unique_experiment_name(session)

        experiment = models.ExperimentModel(experiment_name=experiment_name, direction=ExperimentDirection.NOT_SET)
        session.add(experiment)
        if not self._commit_with_integrity_check(session):
            raise opts.errors.DuplicatedExperimentError(
                "Another experiment with name '{}' already exists. "
                "Please specify a different name, or reuse the existing one "
                "by setting `load_if_exists` (for Python API) or "
                "`--skip-if-exists` flag (for CLI).".format(experiment_name)
            )

        _logger.info("A new experiment created in RDB with name: {}".format(experiment.experiment_name))

        return experiment.experiment_id

    def delete_experiment(self, experiment_id: int) -> None:

        session = self.scoped_session()

        experiment = models.ExperimentModel.find_or_raise_by_id(experiment_id, session)
        session.delete(experiment)

        self._commit_with_integrity_check(session)

    @staticmethod
    def _create_unique_experiment_name(session: orm.Session) -> str:

        while True:
            experiment_uuid = str(uuid.uuid4())
            experiment_name = DEFAULT_EXPERIMENT_NAME_PREFIX + experiment_uuid
            experiment = models.ExperimentModel.find_by_name(experiment_name, session)
            if experiment is None:
                break

        return experiment_name

    # TODO(sano): Prevent simultaneously setting different direction in distributed environments.
    def set_experiment_direction(self, experiment_id: int, direction: ExperimentDirection) -> None:

        session = self.scoped_session()

        experiment = models.ExperimentModel.find_or_raise_by_id(experiment_id, session)

        if experiment.direction != ExperimentDirection.NOT_SET and experiment.direction != direction:
            raise ValueError(
                "Cannot overwrite experiment direction from {} to {}.".format(
                    experiment.direction, direction
                )
            )

        experiment.direction = direction

        self._commit(session)

    def set_experiment_user_attr(self, experiment_id: int, key: str, value: Any) -> None:

        session = self.scoped_session()

        experiment = models.ExperimentModel.find_or_raise_by_id(experiment_id, session)
        attribute = models.ExperimentUserAttributeModel.find_by_experiment_and_key(experiment, key, session)
        if attribute is None:
            attribute = models.ExperimentUserAttributeModel(
                experiment_id=experiment_id, key=key, value_json=json.dumps(value)
            )
            session.add(attribute)
        else:
            attribute.value_json = json.dumps(value)

        self._commit_with_integrity_check(session)

    def set_experiment_system_attr(self, experiment_id: int, key: str, value: Any) -> None:

        session = self.scoped_session()

        experiment = models.ExperimentModel.find_or_raise_by_id(experiment_id, session)
        attribute = models.ExperimentSystemAttributeModel.find_by_experiment_and_key(experiment, key, session)
        if attribute is None:
            attribute = models.ExperimentSystemAttributeModel(
                experiment_id=experiment_id, key=key, value_json=json.dumps(value)
            )
            session.add(attribute)
        else:
            attribute.value_json = json.dumps(value)

        self._commit_with_integrity_check(session)

    def get_experiment_id_from_name(self, experiment_name: str) -> int:

        session = self.scoped_session()

        experiment = models.ExperimentModel.find_or_raise_by_name(experiment_name, session)
        # Terminate transaction explicitly to avoid connection timeout during transaction.
        self._commit(session)

        return experiment.experiment_id

    def get_experiment_id_from_trial_id(self, trial_id: int) -> int:

        session = self.scoped_session()

        trial = models.TrialModel.find_or_raise_by_id(trial_id, session)
        # Terminate transaction explicitly to avoid connection timeout during transaction.
        self._commit(session)

        return trial.experiment_id

    def get_experiment_name_from_id(self, experiment_id: int) -> str:

        session = self.scoped_session()

        experiment = models.ExperimentModel.find_or_raise_by_id(experiment_id, session)
        # Terminate transaction explicitly to avoid connection timeout during transaction.
        self._commit(session)

        return experiment.experiment_name

    def get_experiment_direction(self, experiment_id: int) -> ExperimentDirection:

        session = self.scoped_session()

        experiment = models.ExperimentModel.find_or_raise_by_id(experiment_id, session)
        # Terminate transaction explicitly to avoid connection timeout during transaction.
        self._commit(session)

        return experiment.direction

    def get_experiment_user_attrs(self, experiment_id: int) -> Dict[str, Any]:

        session = self.scoped_session()

        # Ensure that that experiment exists.
        models.ExperimentModel.find_or_raise_by_id(experiment_id, session)
        attributes = models.ExperimentUserAttributeModel.where_experiment_id(experiment_id, session)
        user_attrs = {attr.key: json.loads(attr.value_json) for attr in attributes}
        # Terminate transaction explicitly to avoid connection timeout during transaction.
        self._commit(session)

        return user_attrs

    def get_experiment_system_attrs(self, experiment_id: int) -> Dict[str, Any]:
        session = self.scoped_session()

        # Ensure that that experiment exists.
        models.ExperimentModel.find_or_raise_by_id(experiment_id, session)
        attributes = models.ExperimentSystemAttributeModel.where_experiment_id(experiment_id, session)
        system_attrs = {attr.key: json.loads(attr.value_json) for attr in attributes}
        # Terminate transaction explicitly to avoid connection timeout during transaction.
        self._commit(session)

        return system_attrs

    def get_trial_user_attrs(self, trial_id: int) -> Dict[str, Any]:

        session = self.scoped_session()

        # Ensure trial exists.
        models.TrialModel.find_or_raise_by_id(trial_id, session)

        attributes = models.TrialUserAttributeModel.where_trial_id(trial_id, session)
        user_attrs = {attr.key: json.loads(attr.value_json) for attr in attributes}
        # Terminate transaction explicitly to avoid connection timeout during transaction.
        self._commit(session)

        return user_attrs

    def get_trial_system_attrs(self, trial_id: int) -> Dict[str, Any]:

        session = self.scoped_session()

        # Ensure trial exists.
        models.TrialModel.find_or_raise_by_id(trial_id, session)

        attributes = models.TrialSystemAttributeModel.where_trial_id(trial_id, session)
        system_attrs = {attr.key: json.loads(attr.value_json) for attr in attributes}
        # Terminate transaction explicitly to avoid connection timeout during transaction.
        self._commit(session)

        return system_attrs

    def get_all_experiment_summaries(self) -> List[ExperimentSummary]:
        session = self.scoped_session()

        summarized_trial = (
            session.query(
                models.TrialModel.experiment_id,
                functions.min(models.TrialModel.datetime_start).label("datetime_start"),
                functions.count(models.TrialModel.trial_id).label("n_trial"),
            )
                .group_by(models.TrialModel.experiment_id)
                .with_labels()
                .subquery()
        )
        experiment_summary_stmt = session.query(
            models.ExperimentModel.experiment_id,
            models.ExperimentModel.experiment_name,
            models.ExperimentModel.direction,
            summarized_trial.c.datetime_start,
            functions.coalesce(summarized_trial.c.n_trial, 0).label("n_trial"),
        ).select_from(orm.outerjoin(models.ExperimentModel, summarized_trial))

        experiment_summary = experiment_summary_stmt.all()
        experiment_summaries = []
        for experiment in experiment_summary:
            best_trial: Optional[models.TrialModel] = None
            try:
                if experiment.direction == ExperimentDirection.MAXIMIZE:
                    best_trial = models.TrialModel.find_max_value_trial(experiment.experiment_id, session)
                else:
                    best_trial = models.TrialModel.find_min_value_trial(experiment.experiment_id, session)
            except ValueError:
                best_trial_frozen: Optional[FrozenTrial] = None
            if best_trial:
                params = (
                    session.query(
                        models.TrialParamModel.param_name,
                        models.TrialParamModel.param_value,
                        models.TrialParamModel.distribution_json,
                    )
                        .filter(models.TrialParamModel.trial_id == best_trial.trial_id)
                        .all()
                )
                param_dict = {}
                param_distributions = {}
                for param in params:
                    distribution = samples.json_to_distribution(param.distribution_json)
                    param_dict[param.param_name] = distribution.to_external_repr(param.param_value)
                    param_distributions[param.param_name] = distribution
                user_attrs = session.query(models.TrialUserAttributeModel).filter(
                    models.TrialUserAttributeModel.trial_id == best_trial.trial_id
                )
                system_attrs = session.query(models.TrialSystemAttributeModel).filter(
                    models.TrialSystemAttributeModel.trial_id == best_trial.trial_id
                )
                intermediate = session.query(models.TrialValueModel).filter(
                    models.TrialValueModel.trial_id == best_trial.trial_id
                )
                best_trial_frozen = FrozenTrial(
                    best_trial.number,
                    TrialState.COMPLETE,
                    best_trial.value,
                    best_trial.datetime_start,
                    best_trial.datetime_complete,
                    param_dict,
                    param_distributions,
                    {i.key: json.loads(i.value_json) for i in user_attrs},
                    {i.key: json.loads(i.value_json) for i in system_attrs},
                    {value.step: value.value for value in intermediate},
                    best_trial.trial_id,
                )
            user_attrs = session.query(models.ExperimentUserAttributeModel).filter(
                models.ExperimentUserAttributeModel.experiment_id == experiment.experiment_id
            )
            system_attrs = session.query(models.ExperimentSystemAttributeModel).filter(
                models.ExperimentSystemAttributeModel.experiment_id == experiment.experiment_id
            )
            experiment_summaries.append(
                ExperimentSummary(
                    experiment_name=experiment.experiment_name,
                    direction=experiment.direction,
                    best_trial=best_trial_frozen,
                    user_attrs={i.key: json.loads(i.value_json) for i in user_attrs},
                    system_attrs={i.key: json.loads(i.value_json) for i in system_attrs},
                    n_trials=experiment.n_trial,
                    datetime_start=experiment.datetime_start,
                    experiment_id=experiment.experiment_id,
                )
            )

        # Terminate transaction explicitly to avoid connection timeout during transaction.
        self._commit(session)

        return experiment_summaries

    def create_new_trial(self, experiment_id: int, template_trial: Optional[FrozenTrial] = None) -> int:

        return self._create_new_trial(experiment_id, template_trial)._trial_id

    def _create_new_trial(
            self, experiment_id: int, template_trial: Optional[FrozenTrial] = None
    ) -> FrozenTrial:
        """Create a new trial and returns its trial_id and a :class:`~opts.trial.FrozenTrial`.

        """

        # Retry a couple of times. Deadlocks may occur in distributed environments.
        n_retries = 0
        while True:
            session = self.scoped_session()

            try:
                # Ensure that that experiment exists.
                #
                # Locking within a experiment is necessary since the creation of a trial is not an
                # atomic operation. More precisely, the trial number computed in
                # `_get_prepared_new_trial` is prone to race conditions without this lock.
                models.ExperimentModel.find_or_raise_by_id(experiment_id, session, for_update=True)

                trial = self._get_prepared_new_trial(experiment_id, template_trial, session)

                self._commit(session)

                break  # Successfully created trial.
            except OperationalError:
                session.rollback()

                if n_retries > 2:
                    raise

            n_retries += 1

        if template_trial:
            frozen = copy.deepcopy(template_trial)
            frozen.number = trial.number
            frozen.datetime_start = trial.datetime_start
            frozen._trial_id = trial.trial_id
        else:
            frozen = FrozenTrial(
                number=trial.number,
                state=trial.state,
                value=None,
                datetime_start=trial.datetime_start,
                datetime_complete=None,
                params={},
                distributions={},
                user_attrs={},
                system_attrs={},
                intermediate_values={},
                trial_id=trial.trial_id,
            )

        return frozen

    def _get_prepared_new_trial(
            self, experiment_id: int, template_trial: Optional[FrozenTrial], session: orm.Session
    ) -> models.TrialModel:
        if template_trial is None:
            trial = models.TrialModel(experiment_id=experiment_id, number=None, state=TrialState.RUNNING)
        else:
            # Because only `RUNNING` trials can be updated,
            # we temporarily set the state of the new trial to `RUNNING`.
            # After all fields of the trial have been updated,
            # the state is set to `template_trial.state`.
            temp_state = TrialState.RUNNING

            trial = models.TrialModel(
                experiment_id=experiment_id,
                number=None,
                state=temp_state,
                value=template_trial.value,
                datetime_start=template_trial.datetime_start,
                datetime_complete=template_trial.datetime_complete,
            )

        session.add(trial)

        # Flush the session cache to reflect the above addition operation to
        # the current RDB transaction.
        #
        # Without flushing, the following operations (e.g, `_set_trial_param_without_commit`)
        # will fail because the target trial doesn't exist in the storage yet.
        session.flush()

        if template_trial is not None:
            for param_name, param_value in template_trial.params.items():
                distribution = template_trial.distributions[param_name]
                param_value_in_internal_repr = distribution.to_internal_repr(param_value)
                self._set_trial_param_without_commit(
                    session, trial.trial_id, param_name, param_value_in_internal_repr, distribution
                )

            for key, value in template_trial.user_attrs.items():
                self._set_trial_user_attr_without_commit(session, trial.trial_id, key, value)

            for key, value in template_trial.system_attrs.items():
                self._set_trial_system_attr_without_commit(session, trial.trial_id, key, value)

            for step, intermediate_value in template_trial.intermediate_values.items():
                self._set_trial_intermediate_value_without_commit(
                    session, trial.trial_id, step, intermediate_value
                )

            trial.state = template_trial.state

        trial.number = trial.count_past_trials(session)
        session.add(trial)

        return trial

    def _update_trial(
            self,
            trial_id: int,
            state: Optional[TrialState] = None,
            value: Optional[float] = None,
            intermediate_values: Optional[Dict[int, float]] = None,
            params: Optional[Dict[str, Any]] = None,
            distributions_: Optional[Dict[str, samples.BaseDistribution]] = None,
            user_attrs: Optional[Dict[str, Any]] = None,
            system_attrs: Optional[Dict[str, Any]] = None,
            datetime_complete: Optional[datetime] = None,
    ) -> bool:
        """Sync latest trial updates to a database.
        """

        session = self.scoped_session()

        trial_model = (
            session.query(models.TrialModel)
                .filter(models.TrialModel.trial_id == trial_id)
                .one_or_none()
        )
        if trial_model is None:
            session.rollback()
            raise KeyError(models.NOT_FOUND_MSG)
        if trial_model.state.is_finished():
            session.rollback()
            raise RuntimeError("Cannot change attributes of finished trial.")
        if (
                state
                and trial_model.state != state
                and state == TrialState.RUNNING
                and trial_model.state != TrialState.WAITING
        ):
            session.rollback()
            return False

        if state:
            trial_model.state = state

        if datetime_complete:
            trial_model.datetime_complete = datetime_complete

        if value is not None:
            trial_model.value = value

        if user_attrs:
            trial_user_attrs = (
                session.query(models.TrialUserAttributeModel)
                    .filter(models.TrialUserAttributeModel.trial_id == trial_id)
                    .all()
            )
            trial_user_attrs_dict = {attr.key: attr for attr in trial_user_attrs}
            for k, v in user_attrs.items():
                if k in trial_user_attrs_dict:
                    trial_user_attrs_dict[k].value_json = json.dumps(v)
                    session.add(trial_user_attrs_dict[k])
            trial_model.user_attributes.extend(
                models.TrialUserAttributeModel(key=k, value_json=json.dumps(v))
                for k, v in user_attrs.items()
                if k not in trial_user_attrs_dict
            )
        if system_attrs:
            trial_system_attrs = (
                session.query(models.TrialSystemAttributeModel)
                    .filter(models.TrialSystemAttributeModel.trial_id == trial_id)
                    .all()
            )
            trial_system_attrs_dict = {attr.key: attr for attr in trial_system_attrs}
            for k, v in system_attrs.items():
                if k in trial_system_attrs_dict:
                    trial_system_attrs_dict[k].value_json = json.dumps(v)
                    session.add(trial_system_attrs_dict[k])
            trial_model.system_attributes.extend(
                models.TrialSystemAttributeModel(key=k, value_json=json.dumps(v))
                for k, v in system_attrs.items()
                if k not in trial_system_attrs_dict
            )
        if intermediate_values:
            value_models = (
                session.query(models.TrialValueModel)
                    .filter(models.TrialValueModel.trial_id == trial_id)
                    .all()
            )
            value_dict = {value_model.step: value_model for value_model in value_models}
            for s, v in intermediate_values.items():
                if s in value_dict:
                    value_dict[s].value = v
                    session.add(value_dict[s])
            trial_model.values.extend(
                models.TrialValueModel(step=s, value=v)
                for s, v in intermediate_values.items()
                if s not in value_dict
            )
        if params and distributions_:
            trial_param = (
                session.query(models.TrialParamModel)
                    .filter(models.TrialParamModel.trial_id == trial_id)
                    .all()
            )
            trial_param_dict = {attr.param_name: attr for attr in trial_param}
            for name, v in params.items():
                if name in trial_param_dict:
                    trial_param_dict[name].distribution_json = samples.distribution_to_json(
                        distributions_[name]
                    )
                    trial_param_dict[name].param_value = v
                    session.add(trial_param_dict[name])
            trial_model.params.extend(
                models.TrialParamModel(
                    param_name=param_name,
                    param_value=param_value,
                    distribution_json=samples.distribution_to_json(
                        distributions_[param_name]
                    ),
                )
                for param_name, param_value in params.items()
                if param_name not in trial_param_dict
            )
        session.add(trial_model)
        self._commit(session)

        return True

    def set_trial_state(self, trial_id: int, state: TrialState) -> bool:

        session = self.scoped_session()

        trial = models.TrialModel.find_by_id(trial_id, session, for_update=True)
        if trial is None:
            session.rollback()
            raise KeyError(models.NOT_FOUND_MSG)

        self.check_trial_is_updatable(trial_id, trial.state)

        if state == TrialState.RUNNING and trial.state != TrialState.WAITING:
            session.rollback()
            return False

        trial.state = state
        if state.is_finished():
            trial.datetime_complete = datetime.now()

        return self._commit_with_integrity_check(session)

    def set_trial_param(
            self,
            trial_id: int,
            param_name: str,
            param_value_internal: float,
            distribution: samples.BaseDistribution,
    ) -> None:

        session = self.scoped_session()

        self._set_trial_param_without_commit(
            session, trial_id, param_name, param_value_internal, distribution
        )

        self._commit_with_integrity_check(session)

    def _set_trial_param_without_commit(
            self,
            session: orm.Session,
            trial_id: int,
            param_name: str,
            param_value_internal: float,
            distribution: samples.BaseDistribution,
    ) -> None:

        trial = models.TrialModel.find_or_raise_by_id(trial_id, session)
        self.check_trial_is_updatable(trial_id, trial.state)

        trial_param = models.TrialParamModel.find_by_trial_and_param_name(
            trial, param_name, session
        )

        if trial_param is not None:
            # Raise error in case distribution is incompatible.
            samples.check_distribution_compatibility(
                samples.json_to_distribution(trial_param.distribution_json), distribution
            )

            trial_param.param_value = param_value_internal
            trial_param.distribution_json = samples.distribution_to_json(distribution)
        else:
            trial_param = models.TrialParamModel(
                trial_id=trial_id,
                param_name=param_name,
                param_value=param_value_internal,
                distribution_json=samples.distribution_to_json(distribution),
            )

            trial_param.check_and_add(session)

    def _check_and_set_param_distribution(
            self,
            experiment_id: int,
            trial_id: int,
            param_name: str,
            param_value_internal: float,
            distribution: samples.BaseDistribution,
    ) -> None:

        session = self.scoped_session()

        # Acquire lock.
        #
        # Assume that experiment exists.
        models.ExperimentModel.find_by_id(experiment_id, session, for_update=True)

        models.TrialModel.find_or_raise_by_id(trial_id, session)

        previous_record = (
            session.query(models.TrialParamModel)
                .join(models.TrialModel)
                .filter(models.TrialModel.experiment_id == experiment_id)
                .filter(models.TrialParamModel.param_name == param_name)
                .first()
        )
        if previous_record is not None:
            samples.check_distribution_compatibility(
                samples.json_to_distribution(previous_record.distribution_json),
                distribution,
            )

        session.add(
            models.TrialParamModel(
                trial_id=trial_id,
                param_name=param_name,
                param_value=param_value_internal,
                distribution_json=samples.distribution_to_json(distribution),
            )
        )

        # Release lock.
        session.commit()

    def get_trial_param(self, trial_id: int, param_name: str) -> float:

        session = self.scoped_session()

        trial = models.TrialModel.find_or_raise_by_id(trial_id, session)
        trial_param = models.TrialParamModel.find_or_raise_by_trial_and_param_name(
            trial, param_name, session
        )
        # Terminate transaction explicitly to avoid connection timeout during transaction.
        self._commit(session)

        return trial_param.param_value

    def set_trial_value(self, trial_id: int, value: float) -> None:

        session = self.scoped_session()

        trial = models.TrialModel.find_or_raise_by_id(trial_id, session)
        self.check_trial_is_updatable(trial_id, trial.state)

        trial.value = value

        self._commit(session)

    def set_trial_intermediate_value(
            self, trial_id: int, step: int, intermediate_value: float
    ) -> None:

        session = self.scoped_session()

        self._set_trial_intermediate_value_without_commit(
            session, trial_id, step, intermediate_value
        )

        self._commit_with_integrity_check(session)

    def _set_trial_intermediate_value_without_commit(
            self, session: orm.Session, trial_id: int, step: int, intermediate_value: float
    ) -> None:

        trial = models.TrialModel.find_or_raise_by_id(trial_id, session)
        self.check_trial_is_updatable(trial_id, trial.state)

        trial_value = models.TrialValueModel.find_by_trial_and_step(trial, step, session)
        if trial_value is None:
            trial_value = models.TrialValueModel(
                trial_id=trial_id, step=step, value=intermediate_value
            )
            session.add(trial_value)
        else:
            trial_value.value = intermediate_value

    def set_trial_user_attr(self, trial_id: int, key: str, value: Any) -> None:

        session = self.scoped_session()

        self._set_trial_user_attr_without_commit(session, trial_id, key, value)

        self._commit_with_integrity_check(session)

    def _set_trial_user_attr_without_commit(
            self, session: orm.Session, trial_id: int, key: str, value: Any
    ) -> None:

        trial = models.TrialModel.find_or_raise_by_id(trial_id, session)
        self.check_trial_is_updatable(trial_id, trial.state)

        attribute = models.TrialUserAttributeModel.find_by_trial_and_key(trial, key, session)
        if attribute is None:
            attribute = models.TrialUserAttributeModel(
                trial_id=trial_id, key=key, value_json=json.dumps(value)
            )
            session.add(attribute)
        else:
            attribute.value_json = json.dumps(value)

    def set_trial_system_attr(self, trial_id: int, key: str, value: Any) -> None:

        session = self.scoped_session()

        self._set_trial_system_attr_without_commit(session, trial_id, key, value)

        self._commit_with_integrity_check(session)

    def _set_trial_system_attr_without_commit(
            self, session: orm.Session, trial_id: int, key: str, value: Any
    ) -> None:

        trial = models.TrialModel.find_or_raise_by_id(trial_id, session)
        self.check_trial_is_updatable(trial_id, trial.state)

        attribute = models.TrialSystemAttributeModel.find_by_trial_and_key(trial, key, session)
        if attribute is None:
            attribute = models.TrialSystemAttributeModel(
                trial_id=trial_id, key=key, value_json=json.dumps(value)
            )
            session.add(attribute)
        else:
            attribute.value_json = json.dumps(value)

    def get_trial_number_from_id(self, trial_id: int) -> int:

        trial_number = self.get_trial(trial_id).number
        return trial_number

    def get_trial(self, trial_id: int) -> FrozenTrial:

        session = self.scoped_session()

        trial_model = (
            session.query(models.TrialModel)
                .filter(models.TrialModel.trial_id == trial_id)
                .one_or_none()
        )

        if not trial_model:
            raise KeyError("No trial with trial-id {} found.".format(trial_id))

        frozen_trial = self._build_frozen_trial_from_trial_model(trial_model)

        self._commit(session)

        return frozen_trial

    def get_all_trials(self, experiment_id: int, deepcopy: bool = True) -> List[FrozenTrial]:

        trials = self._get_trials(experiment_id, set())

        return copy.deepcopy(trials) if deepcopy else trials

    def _get_trials(self, experiment_id: int, excluded_trial_ids: Set[int]) -> List[FrozenTrial]:

        session = self.scoped_session()

        # Ensure that the experiment exists.
        models.ExperimentModel.find_or_raise_by_id(experiment_id, session)

        trial_ids = (
            session.query(models.TrialModel.trial_id)
                .filter(models.TrialModel.experiment_id == experiment_id)
                .all()
        )
        trial_ids = set(
            trial_id_tuple[0]
            for trial_id_tuple in trial_ids
            if trial_id_tuple[0] not in excluded_trial_ids
        )
        try:
            trial_models = (
                session.query(models.TrialModel)
                    .options(orm.selectinload(models.TrialModel.params))
                    .options(orm.selectinload(models.TrialModel.values))
                    .options(orm.selectinload(models.TrialModel.user_attributes))
                    .options(orm.selectinload(models.TrialModel.system_attributes))
                    .filter(
                    models.TrialModel.trial_id.in_(trial_ids),
                    models.TrialModel.experiment_id == experiment_id,
                )
                    .all()
            )
        except OperationalError as e:
            # Likely exceeding the number of maximum allowed variables using IN. This number differ
            # between database dialects. For SQLite for instance, see
            # https://www.sqlite.org/limits.html and the section describing
            # SQLITE_MAX_VARIABLE_NUMBER.

            _logger.warning(
                "Caught an error from sqlalchemy: {}. Falling back to a slower alternative. "
                "".format(str(e))
            )

            trial_models = (
                session.query(models.TrialModel)
                    .options(orm.selectinload(models.TrialModel.params))
                    .options(orm.selectinload(models.TrialModel.values))
                    .options(orm.selectinload(models.TrialModel.user_attributes))
                    .options(orm.selectinload(models.TrialModel.system_attributes))
                    .filter(models.TrialModel.experiment_id == experiment_id)
                    .all()
            )
            trial_models = [t for t in trial_models if t.trial_id in trial_ids]

        trials = [self._build_frozen_trial_from_trial_model(trial) for trial in trial_models]

        self._commit(session)

        return trials

    @staticmethod
    def _build_frozen_trial_from_trial_model(trial: models.TrialModel) -> FrozenTrial:
        return FrozenTrial(
            number=trial.number,
            state=trial.state,
            value=trial.value,
            datetime_start=trial.datetime_start,
            datetime_complete=trial.datetime_complete,
            params={
                p.param_name: samples.json_to_distribution(
                    p.distribution_json
                ).to_external_repr(p.param_value)
                for p in trial.params
            },
            distributions={
                p.param_name: samples.json_to_distribution(p.distribution_json)
                for p in trial.params
            },
            user_attrs={attr.key: json.loads(attr.value_json) for attr in trial.user_attributes},
            system_attrs={
                attr.key: json.loads(attr.value_json) for attr in trial.system_attributes
            },
            intermediate_values={value.step: value.value for value in trial.values},
            trial_id=trial.trial_id,
        )

    def get_best_trial(self, experiment_id: int) -> FrozenTrial:

        session = self.scoped_session()
        if self.get_experiment_direction(experiment_id) == ExperimentDirection.MAXIMIZE:
            trial = models.TrialModel.find_max_value_trial(experiment_id, session)
        else:
            trial = models.TrialModel.find_min_value_trial(experiment_id, session)

        # Terminate transaction explicitly to avoid connection timeout during transaction.
        self._commit(session)

        return self.get_trial(trial.trial_id)

    def read_trials_from_remote_storage(self, experiment_id: int) -> None:
        # Make sure that the given experiment exists.
        session = self.scoped_session()
        models.ExperimentModel.find_or_raise_by_id(experiment_id, session)
        self._commit(session)

    @staticmethod
    def _set_default_engine_kwargs_for_mysql(url: str, engine_kwargs: Dict[str, Any]) -> None:

        # Skip if RDB is not MySQL.
        if not url.startswith("mysql"):
            return

        # Do not overwrite value.
        if "pool_pre_ping" in engine_kwargs:
            return

        # If True, the connection pool checks liveness of connections at every checkout.
        # Without this option, trials that take longer than `wait_timeout` may cause connection
        # errors. For further details, please refer to the following document:
        # https://docs.sqlalchemy.org/en/13/core/pooling.html#pool-disconnects-pessimistic
        engine_kwargs["pool_pre_ping"] = True
        _logger.debug("pool_pre_ping=True was set to engine_kwargs to prevent connection timeout.")

    @staticmethod
    def _fill_storage_url_template(template: str) -> str:

        return template.format(SCHEMA_VERSION=models.SCHEMA_VERSION)

    @staticmethod
    def _commit_with_integrity_check(session: orm.Session) -> bool:

        try:
            session.commit()
        except IntegrityError as e:
            _logger.debug(
                "Ignoring {}. This happens due to a timing issue among threads/processes/nodes. "
                "Another one might have committed a record with the same key(s).".format(repr(e))
            )
            session.rollback()
            return False

        return True

    @staticmethod
    def _commit(session: orm.Session) -> None:

        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            message = (
                "An exception is raised during the commit. "
                "This typically happens due to invalid data in the commit, "
                "e.g. exceeding max length."
            )
            raise opts.errors.StorageInternalError(message) from e

    def remove_session(self) -> None:
        """Removes the current session.

        A session is stored in SQLAlchemy's ThreadLocalRegistry for each thread. This method
        closes and removes the session which is associated to the current thread. Particularly,
        under multi-thread use cases, it is important to call this method *from each thread*.
        Otherwise, all sessions and their associated DB connections are destructed by a thread
        that occasionally invoked the garbage collector. By default, it is not allowed to touch
        a SQLite connection from threads other than the thread that created the connection.
        Therefore, we need to explicitly close the connection from each thread.

        """

        self.scoped_session.remove()

    def _finalize(self) -> None:

        # This destructor calls remove_session to explicitly close the DB connection. We need this
        # because DB connections created in SQLAlchemy are not automatically closed by reference
        # counters, so it is not guaranteed that they are released by correct threads (for more
        # information, please see the docstring of remove_session).

        if hasattr(self, "scoped_session"):
            self.remove_session()

    def upgrade(self) -> None:
        """Upgrade the storage schema."""

        self._version_manager.upgrade()

    def get_current_version(self) -> str:
        """Return the schema version currently used by this storage."""

        return self._version_manager.get_current_version()

    def get_head_version(self) -> str:
        """Return the latest schema version."""

        return self._version_manager.get_head_version()

    def get_all_versions(self) -> List[str]:
        """Return the schema version list."""

        return self._version_manager.get_all_versions()


class _VersionManager(object):
    def __init__(self, url: str, engine: Engine, scoped_session: orm.scoped_session) -> None:

        self.url = url
        self.engine = engine
        self.scoped_session = scoped_session

        self._init_version_info_model()
        self._init_alembic()

    def _init_version_info_model(self) -> None:

        session = self.scoped_session()

        version_info = models.VersionInfoModel.find(session)
        if version_info is not None:
            # Terminate transaction explicitly to avoid connection timeout during transaction.
            RDBStorage._commit(session)
            return

        version_info = models.VersionInfoModel(
            schema_version=models.SCHEMA_VERSION, library_version=version.__version__
        )

        session.add(version_info)
        RDBStorage._commit_with_integrity_check(session)

    def _init_alembic(self) -> None:

        logging.getLogger("alembic").setLevel(logging.WARN)

        context = alembic.migration.MigrationContext.configure(self.engine.connect())
        is_initialized = context.get_current_revision() is not None

        if is_initialized:
            # The `alembic_version` table already exists and is not empty.
            return

        if self._is_alembic_supported():
            revision = self.get_head_version()
        else:
            # The storage has been created before alembic is introduced.
            revision = self._get_base_version()

        self._set_alembic_revision(revision)

    def _set_alembic_revision(self, revision: str) -> None:

        context = alembic.migration.MigrationContext.configure(self.engine.connect())
        script = self._create_alembic_script()
        context.stamp(script, revision)

    def check_table_schema_compatibility(self) -> None:

        session = self.scoped_session()

        # NOTE: After invocation of `_init_version_info_model` method,
        #       it is ensured that a `VersionInfoModel` entry exists.
        version_info = models.VersionInfoModel.find(session)
        # Terminate transaction explicitly to avoid connection timeout during transaction.
        RDBStorage._commit(session)

        assert version_info is not None

        current_version = self.get_current_version()
        head_version = self.get_head_version()
        if current_version == head_version:
            return

        message = (
            "The runtime optuna version {} is no longer compatible with the table schema "
            "(set up by optuna {}). ".format(version.__version__, version_info.library_version)
        )
        known_versions = self.get_all_versions()
        if current_version in known_versions:
            message += (
                "Please execute `$ optuna storage upgrade --storage $STORAGE_URL` "
                "for upgrading the storage."
            )
        else:
            message += (
                "Please try updating optuna to the latest version by `$ pip install -U optuna`."
            )

        raise RuntimeError(message)

    def get_current_version(self) -> str:

        context = alembic.migration.MigrationContext.configure(self.engine.connect())
        version = context.get_current_revision()
        assert version is not None

        return version

    def get_head_version(self) -> str:

        script = self._create_alembic_script()
        return script.get_current_head()

    def _get_base_version(self) -> str:

        script = self._create_alembic_script()
        return script.get_base()

    def get_all_versions(self) -> List[str]:

        script = self._create_alembic_script()
        return [r.revision for r in script.walk_revisions()]

    def upgrade(self) -> None:

        config = self._create_alembic_config()
        alembic.command.upgrade(config, "head")

    def _is_alembic_supported(self) -> bool:

        session = self.scoped_session()

        version_info = models.VersionInfoModel.find(session)
        # Terminate transaction explicitly to avoid connection timeout during transaction.
        RDBStorage._commit(session)

        if version_info is None:
            # `None` means this storage was created just now.
            return True

        return version_info.schema_version == models.SCHEMA_VERSION

    def _create_alembic_script(self) -> alembic.script.ScriptDirectory:

        config = self._create_alembic_config()
        script = alembic.script.ScriptDirectory.from_config(config)
        return script

    def _create_alembic_config(self) -> alembic.config.Config:

        alembic_dir = os.path.join(os.path.dirname(__file__), "alembic")

        config = alembic.config.Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
        config.set_main_option("script_location", escape_alembic_config_value(alembic_dir))
        config.set_main_option("sqlalchemy.url", escape_alembic_config_value(self.url))
        return config


def escape_alembic_config_value(value: str) -> str:
    # We must escape '%' in a value string because the character
    # is regarded as the trigger of variable expansion.
    # Please see the documentation of `configparser.BasicInterpolation` for more details.
    return value.replace("%", "%%")

if __name__ == '__main__':
    print("ok")