"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/22 11:11 上午
@Software: PyCharm
@File    : models.py
@E-mail  : victor.xsyang@gmail.com
"""
from datetime import datetime
from typing import Any
from typing import List
from typing import Optional

from sqlalchemy import asc
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import desc
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import orm
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from opts import samples

from opts._experiment_direction import ExperimentDirection

from opts.trial import TrialState

SCHEMA_VERSION = 12

MAX_INDEXED_STRING_LENGTH = 512
MAX_STRING_LENGTH = 2048
MAX_VERSION_LENGTH = 256

NOT_FOUND_MSG = "Record does not exist."

BaseModel: Any = declarative_base()


class ExperimentModel(BaseModel):
    __tablename__ = "experiments"
    experiment_id = Column(Integer, primary_key=True)
    experiment_name = Column(String(MAX_INDEXED_STRING_LENGTH), index=True, unique=True, nullable=False)
    direction = Column(Enum(ExperimentDirection), nullable=False)

    @classmethod
    def find_by_id(
            cls, experiment_id: int, session: orm.Session, for_update: bool = False
                   ) -> Optional["ExperimentModel"]:
        query = session.query(cls).filter(cls.experiment_id == experiment_id)
        if for_update:
            query = query.with_for_update()

        return query.one_or_none()

    @classmethod
    def find_or_raise_by_id(
            cls, experiment_id: int, session: orm.Session, for_update: bool = False
    ) -> "ExperimentModel":

        experiment = cls.find_by_id(experiment_id, session, for_update)
        if experiment is None:
            raise KeyError(NOT_FOUND_MSG)

        return experiment

    @classmethod
    def find_by_name(cls, experiment_name: str, session: orm.Session) -> Optional["ExperimentModel"]:

        experiment = session.query(cls).filter(cls.experiment_name == experiment_name).one_or_none()

        return experiment

    @classmethod
    def find_or_raise_by_name(cls, experiment_name: str, session: orm.Session) -> "ExperimentModel":

        experiment = cls.find_by_name(experiment_name, session)
        if experiment is None:
            raise KeyError(NOT_FOUND_MSG)

        return experiment

    @classmethod
    def all(cls, session: orm.Session) -> List["ExperimentModel"]:

        return session.query(cls).all()

class ExperimentUserAttributeModel(BaseModel):
    __tablename__ = "experiment_user_attributes"
    __table_args__: Any = (UniqueConstraint("experiment_id", "key"),)
    experiment_user_attribute_id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.experiment_id"))
    key = Column(String(MAX_INDEXED_STRING_LENGTH))
    value_json = Column(String(MAX_STRING_LENGTH))

    experiment = orm.relationship(
        ExperimentModel, backref=orm.backref("user_attributes", cascade="all, delete-orphan")
    )

    @classmethod
    def find_by_experiment_and_key(
        cls, experiment: ExperimentModel, key: str, session: orm.Session
    ) -> Optional["ExperimentUserAttributeModel"]:

        attribute = (
            session.query(cls)
            .filter(cls.experiment_id == experiment.experiment_id)
            .filter(cls.key == key)
            .one_or_none()
        )

        return attribute

    @classmethod
    def where_experiment_id(
        cls, experiment_id: int, session: orm.Session
    ) -> List["ExperimentUserAttributeModel"]:

        return session.query(cls).filter(cls.experiment_id == experiment_id).all()

class ExperimentSystemAttributeModel(BaseModel):
    __tablename__ = "experiment_system_attributes"
    __table_args__: Any = (UniqueConstraint("experiment_id", "key"),)
    experiment_system_attribute_id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.experiment_id"))
    key = Column(String(MAX_INDEXED_STRING_LENGTH))
    value_json = Column(String(MAX_STRING_LENGTH))

    experiment = orm.relationship(
        ExperimentModel, backref=orm.backref("system_attributes", cascade="all, delete-orphan")
    )

    @classmethod
    def find_by_experiment_and_key(
        cls, experiment: ExperimentModel, key: str, session: orm.Session
    ) -> Optional["ExperimentSystemAttributeModel"]:

        attribute = (
            session.query(cls)
            .filter(cls.experiment_id == experiment.experiment_id)
            .filter(cls.key == key)
            .one_or_none()
        )

        return attribute

    @classmethod
    def where_experiment_id(
        cls, experiment_id: int, session: orm.Session
    ) -> List["ExperimentSystemAttributeModel"]:

        return session.query(cls).filter(cls.experiment_id == experiment_id).all()

class TrialModel(BaseModel):
    __tablename__ = "trials"
    trial_id = Column(Integer, primary_key=True)
    # No `UniqueConstraint` is put on the `number` columns although it in practice is constrained
    # to be unique. This is to reduce code complexity as table-level locking would be required
    # otherwise. See https://github.com/optuna/optuna/pull/939#discussion_r387447632.
    number = Column(Integer)
    experiment_id = Column(Integer, ForeignKey("experiments.experiment_id"))
    state = Column(Enum(TrialState), nullable=False)
    value = Column(Float)
    datetime_start = Column(DateTime, default=datetime.now)
    datetime_complete = Column(DateTime)

    experiment = orm.relationship(
        ExperimentModel, backref=orm.backref("trials", cascade="all, delete-orphan")
    )

    @classmethod
    def find_by_id(
        cls, trial_id: int, session: orm.Session, for_update: bool = False
    ) -> Optional["TrialModel"]:

        query = session.query(cls).filter(cls.trial_id == trial_id)

        # "FOR UPDATE" clause is used for row-level locking.
        # Please note that SQLite3 doesn't support this clause.
        if for_update:
            query = query.with_for_update()

        return query.one_or_none()

    @classmethod
    def find_max_value_trial(cls, experiment_id: int, session: orm.Session) -> "TrialModel":

        trial = (
            session.query(cls)
            .filter(cls.experiment_id == experiment_id)
            .filter(cls.state == TrialState.COMPLETE)
            .order_by(desc(cls.value))
            .limit(1)
            .one_or_none()
        )
        if trial is None:
            raise ValueError(NOT_FOUND_MSG)
        return trial

    @classmethod
    def find_min_value_trial(cls, experiment_id: int, session: orm.Session) -> "TrialModel":

        trial = (
            session.query(cls)
            .filter(cls.experiment_id == experiment_id)
            .filter(cls.state == TrialState.COMPLETE)
            .order_by(asc(cls.value))
            .limit(1)
            .one_or_none()
        )
        if trial is None:
            raise ValueError(NOT_FOUND_MSG)
        return trial

    @classmethod
    def find_or_raise_by_id(cls, trial_id: int, session: orm.Session) -> "TrialModel":

        trial = cls.find_by_id(trial_id, session)
        if trial is None:
            raise KeyError(NOT_FOUND_MSG)

        return trial

    @classmethod
    def where_experiment(cls, experiment: ExperimentModel, session: orm.Session) -> List["TrialModel"]:

        trials = (
            session.query(cls).filter(cls.experiment_id == experiment.experiment_id).order_by(cls.trial_id).all()
        )

        return trials

    @classmethod
    def count(
        cls,
        session: orm.Session,
        experiment: Optional[ExperimentModel] = None,
        state: Optional[TrialState] = None,
    ) -> int:

        trial_count = session.query(func.count(cls.trial_id))
        if experiment is not None:
            trial_count = trial_count.filter(cls.experiment_id == experiment.experiment_id)
        if state is not None:
            trial_count = trial_count.filter(cls.state == state)

        return trial_count.scalar()

    def count_past_trials(self, session: orm.Session) -> int:

        trial_count = session.query(func.count(TrialModel.trial_id)).filter(
            TrialModel.experiment_id == self.experiment_id, TrialModel.trial_id < self.trial_id
        )
        return trial_count.scalar()

    @classmethod
    def all(cls, session: orm.Session) -> List["TrialModel"]:

        return session.query(cls).all()

    @classmethod
    def get_all_trial_ids_where_experiment(cls, experiment: ExperimentModel, session: orm.Session) -> List[int]:

        trials = (
            session.query(cls.trial_id)
            .filter(cls.experiment_id == experiment.experiment_id)
            .order_by(cls.trial_id)
            .all()
        )

        return [t.trial_id for t in trials]

class TrialUserAttributeModel(BaseModel):
    __tablename__ = "trial_user_attributes"
    __table_args__: Any = (UniqueConstraint("trial_id", "key"),)
    trial_user_attribute_id = Column(Integer, primary_key=True)
    trial_id = Column(Integer, ForeignKey("trials.trial_id"))
    key = Column(String(MAX_INDEXED_STRING_LENGTH))
    value_json = Column(String(MAX_STRING_LENGTH))

    trial = orm.relationship(
        TrialModel, backref=orm.backref("user_attributes", cascade="all, delete-orphan")
    )

    @classmethod
    def find_by_trial_and_key(
        cls, trial: TrialModel, key: str, session: orm.Session
    ) -> Optional["TrialUserAttributeModel"]:

        attribute = (
            session.query(cls)
            .filter(cls.trial_id == trial.trial_id)
            .filter(cls.key == key)
            .one_or_none()
        )

        return attribute

    @classmethod
    def where_experiment(
        cls, experiment: ExperimentModel, session: orm.Session
    ) -> List["TrialUserAttributeModel"]:

        trial_user_attributes = (
            session.query(cls).join(TrialModel).filter(TrialModel.experiment_id == experiment.experiment_id).all()
        )

        return trial_user_attributes

    @classmethod
    def where_trial(
        cls, trial: TrialModel, session: orm.Session
    ) -> List["TrialUserAttributeModel"]:

        return cls.where_trial_id(trial.trial_id, session)

    @classmethod
    def where_trial_id(
        cls, trial_id: int, session: orm.Session
    ) -> List["TrialUserAttributeModel"]:

        return session.query(cls).filter(cls.trial_id == trial_id).all()

    @classmethod
    def all(cls, session: orm.Session) -> List["TrialUserAttributeModel"]:

        return session.query(cls).all()

class TrialSystemAttributeModel(BaseModel):
    __tablename__ = "trial_system_attributes"
    __table_args__: Any = (UniqueConstraint("trial_id", "key"),)
    trial_system_attribute_id = Column(Integer, primary_key=True)
    trial_id = Column(Integer, ForeignKey("trials.trial_id"))
    key = Column(String(MAX_INDEXED_STRING_LENGTH))
    value_json = Column(String(MAX_STRING_LENGTH))

    trial = orm.relationship(
        TrialModel, backref=orm.backref("system_attributes", cascade="all, delete-orphan")
    )

    @classmethod
    def find_by_trial_and_key(
        cls, trial: TrialModel, key: str, session: orm.Session
    ) -> Optional["TrialSystemAttributeModel"]:

        attribute = (
            session.query(cls)
            .filter(cls.trial_id == trial.trial_id)
            .filter(cls.key == key)
            .one_or_none()
        )

        return attribute

    @classmethod
    def where_experiment(
        cls, experiment: ExperimentModel, session: orm.Session
    ) -> List["TrialSystemAttributeModel"]:

        trial_system_attributes = (
            session.query(cls).join(TrialModel).filter(TrialModel.experiment_id == experiment.experiment_id).all()
        )

        return trial_system_attributes

    @classmethod
    def where_trial(
        cls, trial: TrialModel, session: orm.Session
    ) -> List["TrialSystemAttributeModel"]:

        return cls.where_trial_id(trial.trial_id, session)

    @classmethod
    def where_trial_id(
        cls, trial_id: int, session: orm.Session
    ) -> List["TrialSystemAttributeModel"]:

        return session.query(cls).filter(cls.trial_id == trial_id).all()

    @classmethod
    def all(cls, session: orm.Session) -> List["TrialSystemAttributeModel"]:

        return session.query(cls).all()

class TrialParamModel(BaseModel):
    __tablename__ = "trial_params"
    __table_args__: Any = (UniqueConstraint("trial_id", "param_name"),)
    param_id = Column(Integer, primary_key=True)
    trial_id = Column(Integer, ForeignKey("trials.trial_id"))
    param_name = Column(String(MAX_INDEXED_STRING_LENGTH))
    param_value = Column(Float)
    distribution_json = Column(String(MAX_STRING_LENGTH))

    trial = orm.relationship(
        TrialModel, backref=orm.backref("params", cascade="all, delete-orphan")
    )

    def check_and_add(self, session: orm.Session) -> None:

        self._check_compatibility_with_previous_trial_param_distributions(session)
        session.add(self)

    def _check_compatibility_with_previous_trial_param_distributions(
        self, session: orm.Session
    ) -> None:

        trial = TrialModel.find_or_raise_by_id(self.trial_id, session)

        previous_record = (
            session.query(TrialParamModel)
            .join(TrialModel)
            .filter(TrialModel.experiment_id == trial.experiment_id)
            .filter(TrialParamModel.param_name == self.param_name)
            .first()
        )
        if previous_record is not None:
            samples.check_distribution_compatibility(
                samples.json_to_distribution(previous_record.distribution_json),
                samples.json_to_distribution(self.distribution_json),
            )

    @classmethod
    def find_by_trial_and_param_name(
        cls, trial: TrialModel, param_name: str, session: orm.Session
    ) -> Optional["TrialParamModel"]:

        param_distribution = (
            session.query(cls)
            .filter(cls.trial_id == trial.trial_id)
            .filter(cls.param_name == param_name)
            .one_or_none()
        )

        return param_distribution

    @classmethod
    def find_or_raise_by_trial_and_param_name(
        cls, trial: TrialModel, param_name: str, session: orm.Session
    ) -> "TrialParamModel":

        param_distribution = cls.find_by_trial_and_param_name(trial, param_name, session)

        if param_distribution is None:
            raise KeyError(NOT_FOUND_MSG)

        return param_distribution

    @classmethod
    def where_experiment(cls, experiment: ExperimentModel, session: orm.Session) -> List["TrialParamModel"]:

        trial_params = (
            session.query(cls).join(TrialModel).filter(TrialModel.experiment_id == experiment.experiment_id).all()
        )

        return trial_params

    @classmethod
    def where_trial(cls, trial: TrialModel, session: orm.Session) -> List["TrialParamModel"]:

        trial_params = session.query(cls).filter(cls.trial_id == trial.trial_id).all()

        return trial_params

    @classmethod
    def all(cls, session: orm.Session) -> List["TrialParamModel"]:

        return session.query(cls).all()

class TrialValueModel(BaseModel):
    __tablename__ = "trial_values"
    __table_args__: Any = (UniqueConstraint("trial_id", "step"),)
    trial_value_id = Column(Integer, primary_key=True)
    trial_id = Column(Integer, ForeignKey("trials.trial_id"))
    step = Column(Integer)
    value = Column(Float)

    trial = orm.relationship(
        TrialModel, backref=orm.backref("values", cascade="all, delete-orphan")
    )

    @classmethod
    def find_by_trial_and_step(
        cls, trial: TrialModel, step: int, session: orm.Session
    ) -> Optional["TrialValueModel"]:

        trial_value = (
            session.query(cls)
            .filter(cls.trial_id == trial.trial_id)
            .filter(cls.step == step)
            .one_or_none()
        )

        return trial_value

    @classmethod
    def where_experiment(cls, experiment: ExperimentModel, session: orm.Session) -> List["TrialValueModel"]:

        trial_values = (
            session.query(cls).join(TrialModel).filter(TrialModel.experiment_id == experiment.experiment_id).all()
        )

        return trial_values

    @classmethod
    def where_trial(cls, trial: TrialModel, session: orm.Session) -> List["TrialValueModel"]:

        trial_values = session.query(cls).filter(cls.trial_id == trial.trial_id).all()

        return trial_values

    @classmethod
    def all(cls, session: orm.Session) -> List["TrialValueModel"]:

        return session.query(cls).all()

class VersionInfoModel(BaseModel):
    __tablename__ = "version_info"
    # setting check constraint to ensure the number of rows is at most 1
    __table_args__: Any = (CheckConstraint("version_info_id=1"),)
    version_info_id = Column(Integer, primary_key=True, autoincrement=False, default=1)
    schema_version = Column(Integer)
    library_version = Column(String(MAX_VERSION_LENGTH))

    @classmethod
    def find(cls, session: orm.Session) -> "VersionInfoModel":

        version_info = session.query(cls).one_or_none()

        return version_info

if __name__ == '__main__':
    print("ok")