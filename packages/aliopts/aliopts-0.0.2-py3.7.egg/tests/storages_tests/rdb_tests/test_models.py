"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/23 10:09 上午
@Software: PyCharm
@File    : test_models.py
@E-mail  : victor.xsyang@gmail.com
"""
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from opts._experiment_direction import ExperimentDirection
from opts.storages._rdb.models import BaseModel
from opts.storages._rdb.models import ExperimentModel
from opts.storages._rdb.models import ExperimentSystemAttributeModel
from opts.storages._rdb.models import TrialModel
from opts.storages._rdb.models import TrialSystemAttributeModel
from opts.storages._rdb.models import TrialUserAttributeModel
from opts.storages._rdb.models import VersionInfoModel
from opts.trial import TrialState

@pytest.fixture
def session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    BaseModel.metadata.create_all(engine)
    return Session(bind=engine)


class TestExperimentSystemAttributeModel(object):
    @staticmethod
    def test_find_by_experiment_and_key(session: Session) -> None:
        experiment = ExperimentModel(experiment_id=1, experiment_name="test-experiment")
        session.add(
            ExperimentSystemAttributeModel(experiment_id=experiment.experiment_id, key="sample-key", value_json="1")
        )
        session.commit()

        attr = ExperimentSystemAttributeModel.find_by_experiment_and_key(experiment, "sample-key", session)
        assert attr is not None and "1" == attr.value_json

        assert ExperimentSystemAttributeModel.find_by_experiment_and_key(experiment, "not-found", session) is None

    @staticmethod
    def test_where_experiment_id(session: Session) -> None:
        sample_experiment = ExperimentModel(experiment_id=1, experiment_name="test-experiment")
        empty_experiment = ExperimentModel(experiment_id=2, experiment_name="test-experiment")

        session.add(
            ExperimentSystemAttributeModel(
                experiment_id=sample_experiment.experiment_id, key="sample-key", value_json="1"
            )
        )

        assert 1 == len(ExperimentSystemAttributeModel.where_experiment_id(sample_experiment.experiment_id, session))
        assert 0 == len(ExperimentSystemAttributeModel.where_experiment_id(empty_experiment.experiment_id, session))
        # Check the case of unknown study_id.
        assert 0 == len(ExperimentSystemAttributeModel.where_experiment_id(-1, session))

    @staticmethod
    def test_cascade_delete_on_experiment(session: Session) -> None:
        experiment_id = 1
        experiment = ExperimentModel(
            experiment_id=experiment_id, experiment_name="test-experiment", direction=ExperimentDirection.MINIMIZE
        )
        experiment.system_attributes.append(
            ExperimentSystemAttributeModel(experiment_id=experiment_id, key="sample-key1", value_json="1")
        )
        experiment.system_attributes.append(
            ExperimentSystemAttributeModel(experiment_id=experiment_id, key="sample-key2", value_json="2")
        )
        session.add(experiment)
        session.commit()

        assert 2 == len(ExperimentSystemAttributeModel.where_experiment_id(experiment_id, session))

        session.delete(experiment)
        session.commit()

        assert 0 == len(ExperimentSystemAttributeModel.where_experiment_id(experiment_id, session))


class TestTrialModel(object):
    @staticmethod
    def test_default_datetime(session: Session) -> None:

        datetime_1 = datetime.now()

        session.add(TrialModel(state=TrialState.RUNNING))
        session.commit()

        datetime_2 = datetime.now()

        trial_model = session.query(TrialModel).first()
        assert datetime_1 < trial_model.datetime_start < datetime_2
        assert trial_model.datetime_complete is None

    @staticmethod
    def test_count(session: Session) -> None:

        experiment_1 = ExperimentModel(experiment_id=1, experiment_name="test-study-1")
        experiment_2 = ExperimentModel(experiment_id=2, experiment_name="test-study-2")

        session.add(TrialModel(experiment_id=experiment_1.experiment_id, state=TrialState.COMPLETE))
        session.add(TrialModel(experiment_id=experiment_1.experiment_id, state=TrialState.RUNNING))
        session.add(TrialModel(experiment_id=experiment_2.experiment_id, state=TrialState.RUNNING))
        session.commit()

        assert 3 == TrialModel.count(session)
        assert 2 == TrialModel.count(session, experiment=experiment_1)
        assert 1 == TrialModel.count(session, state=TrialState.COMPLETE)

    @staticmethod
    def test_count_past_trials(session: Session) -> None:

        experiment_1 = ExperimentModel(experiment_id=1, experiment_name="test-experiment-1")
        experiment_2 = ExperimentModel(experiment_id=2, experiment_name="test-experiment-2")

        trial_1_1 = TrialModel(experiment_id=experiment_1.experiment_id, state=TrialState.COMPLETE)
        session.add(trial_1_1)
        session.commit()
        assert 0 == trial_1_1.count_past_trials(session)

        trial_1_2 = TrialModel(experiment_id=experiment_1.experiment_id, state=TrialState.RUNNING)
        session.add(trial_1_2)
        session.commit()
        assert 1 == trial_1_2.count_past_trials(session)

        trial_2_1 = TrialModel(experiment_id=experiment_2.experiment_id, state=TrialState.RUNNING)
        session.add(trial_2_1)
        session.commit()
        assert 0 == trial_2_1.count_past_trials(session)

    @staticmethod
    def test_cascade_delete_on_study(session: Session) -> None:

        experiment_id = 1
        experiment = ExperimentModel(
            experiment_id=experiment_id, experiment_name="test-experiment", direction=ExperimentDirection.MINIMIZE
        )
        experiment.trials.append(TrialModel(experiment_id=experiment.experiment_id, state=TrialState.COMPLETE))
        experiment.trials.append(TrialModel(experiment_id=experiment.experiment_id, state=TrialState.RUNNING))
        session.add(experiment)
        session.commit()

        assert 2 == len(TrialModel.where_experiment(experiment, session))

        session.delete(experiment)
        session.commit()

        assert 0 == len(TrialModel.where_experiment(experiment, session))


class TestTrialUserAttributeModel(object):
    @staticmethod
    def test_find_by_trial_and_key(session: Session) -> None:

        experiment = ExperimentModel(experiment_id=1, experiment_name="test-experiment")
        trial = TrialModel(experiment_id=experiment.experiment_id)

        session.add(
            TrialUserAttributeModel(trial_id=trial.trial_id, key="sample-key", value_json="1")
        )
        session.commit()

        attr = TrialUserAttributeModel.find_by_trial_and_key(trial, "sample-key", session)
        assert attr is not None
        assert "1" == attr.value_json
        assert TrialUserAttributeModel.find_by_trial_and_key(trial, "not-found", session) is None

    @staticmethod
    def test_where_experiment(session: Session) -> None:

        experiment = ExperimentModel(experiment_id=1, experiment_name="test-experiment", direction=ExperimentDirection.MINIMIZE)
        trial = TrialModel(trial_id=1, experiment_id=experiment.experiment_id, state=TrialState.COMPLETE)

        session.add(experiment)
        session.add(trial)
        session.add(
            TrialUserAttributeModel(trial_id=trial.trial_id, key="sample-key", value_json="1")
        )
        session.commit()

        user_attributes = TrialUserAttributeModel.where_experiment(experiment, session)
        assert 1 == len(user_attributes)
        assert "sample-key" == user_attributes[0].key
        assert "1" == user_attributes[0].value_json

    @staticmethod
    def test_where_trial(session: Session) -> None:

        experiment = ExperimentModel(experiment_id=1, experiment_name="test-experiment", direction=ExperimentDirection.MINIMIZE)
        trial = TrialModel(trial_id=1, experiment_id=experiment.experiment_id, state=TrialState.COMPLETE)

        session.add(
            TrialUserAttributeModel(trial_id=trial.trial_id, key="sample-key", value_json="1")
        )
        session.commit()

        user_attributes = TrialUserAttributeModel.where_trial(trial, session)
        assert 1 == len(user_attributes)
        assert "sample-key" == user_attributes[0].key
        assert "1" == user_attributes[0].value_json

    @staticmethod
    def test_all(session: Session) -> None:

        experiment = ExperimentModel(experiment_id=1, experiment_name="test-study", direction=ExperimentDirection.MINIMIZE)
        trial = TrialModel(trial_id=1, experiment_id=experiment.experiment_id, state=TrialState.COMPLETE)

        session.add(
            TrialUserAttributeModel(trial_id=trial.trial_id, key="sample-key", value_json="1")
        )
        session.commit()

        user_attributes = TrialUserAttributeModel.all(session)
        assert 1 == len(user_attributes)
        assert "sample-key" == user_attributes[0].key
        assert "1" == user_attributes[0].value_json

    @staticmethod
    def test_cascade_delete_on_trial(session: Session) -> None:

        trial_id = 1
        experiment = ExperimentModel(experiment_id=1, experiment_name="test-experiment", direction=ExperimentDirection.MINIMIZE)
        trial = TrialModel(trial_id=trial_id, experiment_id=experiment.experiment_id, state=TrialState.COMPLETE)
        trial.user_attributes.append(
            TrialUserAttributeModel(trial_id=trial_id, key="sample-key1", value_json="1")
        )
        trial.user_attributes.append(
            TrialUserAttributeModel(trial_id=trial_id, key="sample-key2", value_json="2")
        )
        experiment.trials.append(trial)
        session.add(experiment)
        session.commit()

        assert 2 == len(TrialUserAttributeModel.where_trial_id(trial_id, session))

        session.delete(trial)
        session.commit()

        assert 0 == len(TrialUserAttributeModel.where_trial_id(trial_id, session))


class TestTrialSystemAttributeModel(object):
    @staticmethod
    def test_find_by_trial_and_key(session: Session) -> None:

        experiment = ExperimentModel(experiment_id=1, experiment_name="test-experiment")
        trial = TrialModel(experiment_id=experiment.experiment_id)

        session.add(
            TrialSystemAttributeModel(trial_id=trial.trial_id, key="sample-key", value_json="1")
        )
        session.commit()

        attr = TrialSystemAttributeModel.find_by_trial_and_key(trial, "sample-key", session)
        assert attr is not None
        assert "1" == attr.value_json
        assert TrialSystemAttributeModel.find_by_trial_and_key(trial, "not-found", session) is None

    @staticmethod
    def test_where_experiment(session: Session) -> None:

        experiment = ExperimentModel(experiment_id=1, experiment_name="test-experiment", direction=ExperimentDirection.MINIMIZE)
        trial = TrialModel(trial_id=1, experiment_id=experiment.experiment_id, state=TrialState.COMPLETE)

        session.add(experiment)
        session.add(trial)
        session.add(
            TrialSystemAttributeModel(trial_id=trial.trial_id, key="sample-key", value_json="1")
        )
        session.commit()

        system_attributes = TrialSystemAttributeModel.where_experiment(experiment, session)
        assert 1 == len(system_attributes)
        assert "sample-key" == system_attributes[0].key
        assert "1" == system_attributes[0].value_json

    @staticmethod
    def test_where_trial(session: Session) -> None:

        experiment = ExperimentModel(experiment_id=1, experiment_name="test-experiment", direction=ExperimentDirection.MINIMIZE)
        trial = TrialModel(trial_id=1, experiment_id=experiment.experiment_id, state=TrialState.COMPLETE)

        session.add(
            TrialSystemAttributeModel(trial_id=trial.trial_id, key="sample-key", value_json="1")
        )
        session.commit()

        system_attributes = TrialSystemAttributeModel.where_trial(trial, session)
        assert 1 == len(system_attributes)
        assert "sample-key" == system_attributes[0].key
        assert "1" == system_attributes[0].value_json

    @staticmethod
    def test_all(session: Session) -> None:

        experiment = ExperimentModel(experiment_id=1, experiment_name="test-experiment", direction=ExperimentDirection.MINIMIZE)
        trial = TrialModel(trial_id=1, experiment_id=experiment.experiment_id, state=TrialState.COMPLETE)

        session.add(
            TrialSystemAttributeModel(trial_id=trial.trial_id, key="sample-key", value_json="1")
        )
        session.commit()

        system_attributes = TrialSystemAttributeModel.all(session)
        assert 1 == len(system_attributes)
        assert "sample-key" == system_attributes[0].key
        assert "1" == system_attributes[0].value_json

    @staticmethod
    def test_cascade_delete_on_trial(session: Session) -> None:

        trial_id = 1
        experiment = ExperimentModel(experiment_id=1, experiment_name="test-experiment", direction=ExperimentDirection.MINIMIZE)
        trial = TrialModel(trial_id=trial_id, experiment_id=experiment.experiment_id, state=TrialState.COMPLETE)
        trial.system_attributes.append(
            TrialSystemAttributeModel(trial_id=trial_id, key="sample-key1", value_json="1")
        )
        trial.system_attributes.append(
            TrialSystemAttributeModel(trial_id=trial_id, key="sample-key2", value_json="2")
        )
        experiment.trials.append(trial)
        session.add(experiment)
        session.commit()

        assert 2 == len(TrialSystemAttributeModel.where_trial_id(trial_id, session))

        session.delete(trial)
        session.commit()

        assert 0 == len(TrialSystemAttributeModel.where_trial_id(trial_id, session))


class TestVersionInfoModel(object):
    @staticmethod
    def test_version_info_id_constraint(session: Session) -> None:

        session.add(VersionInfoModel(schema_version=1, library_version="0.0.1"))
        session.commit()

        # Test check constraint of version_info_id.
        session.add(VersionInfoModel(version_info_id=2, schema_version=2, library_version="0.0.2"))
        pytest.raises(IntegrityError, lambda: session.commit())
