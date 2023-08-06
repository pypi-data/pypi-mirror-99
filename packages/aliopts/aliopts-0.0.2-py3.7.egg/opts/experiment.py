"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/25 9:56 下午
@Software: PyCharm
@File    : experiment.py
@E-mail  : victor.xsyang@gmail.com
"""
import copy
import threading
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from opts import errors
from opts import logger
from opts import stoppers
from opts import samplers
from opts import storages
from opts import trial as trial_module
from opts._dataframe import _trials_dataframe
from opts._dataframe import pd
from opts._experimental import experimental
from opts._optimize import _optimize
from opts._experiment_direction import ExperimentDirection
from opts._experiment_summary import ExperimentSummary
from opts.trial import create_trial
from opts.trial import FrozenTrial
from opts.trial import TrialState

ObjectiveFuncType = Callable[[trial_module.Trial], float]


_logger = logger.get_logger(__name__)


class BaseExperiment(object):
    def __init__(self, experiment_id: int, storage: storages.BaseStorage) -> None:

        self._experiment_id = experiment_id
        self._storage = storage

    @property
    def best_params(self) -> Dict[str, Any]:
        """Return parameters of the best trial in the study.

        Returns:
            A dictionary containing parameters of the best trial.
        """

        return self.best_trial.params

    @property
    def best_value(self) -> float:
        """Return the best objective value in the study.

        Returns:
            A float representing the best objective value.
        """

        best_value = self.best_trial.value
        assert best_value is not None

        return best_value

    @property
    def best_trial(self) -> FrozenTrial:
        """Return the best trial in the experiment.

        Returns:
            A :class:`~opts.FrozenTrial` object of the best trial.
        """

        return copy.deepcopy(self._storage.get_best_trial(self._experiment_id))

    @property
    def direction(self) -> ExperimentDirection:
        """Return the direction of the study.

        Returns:
            A :class:`~optuna.study.StudyDirection` object.
        """

        return self._storage.get_experiment_direction(self._experiment_id)

    @property
    def trials(self) -> List[FrozenTrial]:
        """Return all trials in the study.

        The returned trials are ordered by trial number.

        This is a short form of ``self.get_trials(deepcopy=True)``.

        Returns:
            A list of :class:`~optuna.FrozenTrial` objects.
        """

        return self.get_trials()

    def get_trials(self, deepcopy: bool = True) -> List[FrozenTrial]:
        """Return all trials in the study.

        The returned trials are ordered by trial number.

        For library users, it's recommended to use more handy
        :attr:`~optuna.study.Study.trials` property to get the trials instead.

        Example:
            .. testcode::

                import optuna


                def objective(trial):
                    x = trial.suggest_uniform("x", -1, 1)
                    return x ** 2


                study = optuna.create_study()
                study.optimize(objective, n_trials=3)

                trials = study.get_trials()
                assert len(trials) == 3
        Args:
            deepcopy:
                Flag to control whether to apply ``copy.deepcopy()`` to the trials.
                Note that if you set the flag to :obj:`False`, you shouldn't mutate
                any fields of the returned trial. Otherwise the internal state of
                the study may corrupt and unexpected behavior may happen.

        Returns:
            A list of :class:`~optuna.FrozenTrial` objects.
        """

        self._storage.read_trials_from_remote_storage(self._experiment_id)
        return self._storage.get_all_trials(self._experiment_id, deepcopy=deepcopy)


class Experiment(BaseExperiment):
    """A experiment corresponds to an optimization task, i.e., a set of trials.


    """

    def __init__(
        self,
        experiment_name: str,
        storage: Union[str, storages.BaseStorage],
        sampler: Optional["samplers.BaseSampler"] = None,
        stopper: Optional[stoppers.BaseStopper] = None,
    ) -> None:

        self.experiment_name = experiment_name
        storage = storages.get_storage(storage)
        experiment_id = storage.get_experiment_id_from_name(experiment_name)
        super(Experiment, self).__init__(experiment_id, storage)

        self.sampler = sampler or samplers.TPESampler()
        self.stopper = stopper or stoppers.MedianStopper()

        self._optimize_lock = threading.Lock()
        self._stop_flag = False

    def __getstate__(self) -> Dict[Any, Any]:

        state = self.__dict__.copy()
        del state["_optimize_lock"]
        return state

    def __setstate__(self, state: Dict[Any, Any]) -> None:

        self.__dict__.update(state)
        self._optimize_lock = threading.Lock()

    @property
    def user_attrs(self) -> Dict[str, Any]:
        """Return user attributes.

        """

        return copy.deepcopy(self._storage.get_experiment_user_attrs(self._experiment_id))

    @property
    def system_attrs(self) -> Dict[str, Any]:
        """Return system attributes.

        Returns:
            A dictionary containing all system attributes.
        """

        return copy.deepcopy(self._storage.get_experiment_system_attrs(self._experiment_id))

    def optimize(
        self,
        func: ObjectiveFuncType,
        n_trials: Optional[int] = None,
        timeout: Optional[float] = None,
        n_jobs: int = 1,
        catch: Tuple[Type[Exception], ...] = (),
        callbacks: Optional[List[Callable[["Experiment", FrozenTrial], None]]] = None,
        gc_after_trial: bool = False,
        show_progress_bar: bool = False,
    ) -> None:
        """Optimize an objective function.

        """
        _optimize(
            experiment=self,
            func=func,
            n_trials=n_trials,
            timeout=timeout,
            n_jobs=n_jobs,
            catch=catch,
            callbacks=callbacks,
            gc_after_trial=gc_after_trial,
            show_progress_bar=show_progress_bar,
        )

    def set_user_attr(self, key: str, value: Any) -> None:
        """Set a user attribute to the study.

        .. seealso::

            See :attr:`~optuna.study.Study.user_attrs` for related attribute.

        Example:

            .. testcode::

                import optuna


                def objective(trial):
                    x = trial.suggest_float("x", 0, 1)
                    y = trial.suggest_float("y", 0, 1)
                    return x ** 2 + y ** 2


                study = optuna.create_study()

                study.set_user_attr("objective function", "quadratic function")
                study.set_user_attr("dimensions", 2)
                study.set_user_attr("contributors", ["Akiba", "Sano"])

                assert study.user_attrs == {
                    "objective function": "quadratic function",
                    "dimensions": 2,
                    "contributors": ["Akiba", "Sano"],
                }

        Args:
            key: A key string of the attribute.
            value: A value of the attribute. The value should be JSON serializable.

        """

        self._storage.set_experiment_user_attr(self._experiment_id, key, value)

    def set_system_attr(self, key: str, value: Any) -> None:
        """Set a system attribute to the study.

        Note that Optuna internally uses this method to save system messages. Please use
        :func:`~optuna.study.Study.set_user_attr` to set users' attributes.

        Args:
            key: A key string of the attribute.
            value: A value of the attribute. The value should be JSON serializable.

        """

        self._storage.set_experiment_system_attr(self._experiment_id, key, value)

    def trials_dataframe(
        self,
        attrs: Tuple[str, ...] = (
            "number",
            "value",
            "datetime_start",
            "datetime_complete",
            "duration",
            "params",
            "user_attrs",
            "system_attrs",
            "state",
        ),
        multi_index: bool = False,
    ) -> "pd.DataFrame":
        """Export trials as a pandas DataFrame_.

        The DataFrame_ provides various features to analyze studies. It is also useful to draw a
        histogram of objective values and to export trials as a CSV file.
        If there are no trials, an empty DataFrame_ is returned.

        Example:

            .. testcode::

                import optuna
                import pandas


                def objective(trial):
                    x = trial.suggest_uniform("x", -1, 1)
                    return x ** 2


                study = optuna.create_study()
                study.optimize(objective, n_trials=3)

                # Create a dataframe from the study.
                df = study.trials_dataframe()
                assert isinstance(df, pandas.DataFrame)
                assert df.shape[0] == 3  # n_trials.

        Args:
            attrs:
                Specifies field names of :class:`~optuna.FrozenTrial` to include them to a
                DataFrame of trials.
            multi_index:
                Specifies whether the returned DataFrame_ employs MultiIndex_ or not. Columns that
                are hierarchical by nature such as ``(params, x)`` will be flattened to
                ``params_x`` when set to :obj:`False`.

        Returns:
            A pandas DataFrame_ of trials in the :class:`~optuna.study.Study`.

        .. _DataFrame: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
        .. _MultiIndex: https://pandas.pydata.org/pandas-docs/stable/advanced.html
        """
        return _trials_dataframe(self, attrs, multi_index)

    def stop(self) -> None:

        """Exit from the current optimization loop after the running trials finish.

        This method lets the running :meth:`~optuna.study.Study.optimize` method return
        immediately after all trials which the :meth:`~optuna.study.Study.optimize` method
        spawned finishes.
        This method does not affect any behaviors of parallel or successive study processes.

        Example:

            .. testcode::

                import optuna


                def objective(trial):
                    if trial.number == 4:
                        trial.study.stop()
                    x = trial.suggest_uniform("x", 0, 10)
                    return x ** 2


                study = optuna.create_study()
                study.optimize(objective, n_trials=10)
                assert len(study.trials) == 5

        Raises:
            RuntimeError:
                If this method is called outside an objective function or callback.
        """

        if self._optimize_lock.acquire(False):
            self._optimize_lock.release()
            raise RuntimeError(
                "`Study.stop` is supposed to be invoked inside an objective function or a "
                "callback."
            )

        self._stop_flag = True

    @experimental("1.2.0")
    def enqueue_trial(self, params: Dict[str, Any]) -> None:
        """Enqueue a trial with given parameter values.

        You can fix the next sampling parameters which will be evaluated in your
        objective function.

        Example:

            .. testcode::

                import optuna


                def objective(trial):
                    x = trial.suggest_uniform("x", 0, 10)
                    return x ** 2


                study = optuna.create_study()
                study.enqueue_trial({"x": 5})
                study.enqueue_trial({"x": 0})
                study.optimize(objective, n_trials=2)

                assert study.trials[0].params == {"x": 5}
                assert study.trials[1].params == {"x": 0}

        Args:
            params:
                Parameter values to pass your objective function.
        """

        self.add_trial(
            create_trial(state=TrialState.WAITING, system_attrs={"fixed_params": params})
        )

    @experimental("2.0.0")
    def add_trial(self, trial: FrozenTrial) -> None:
        """Add trial to study.

        The trial is validated before being added.

        Example:

            .. testcode::

                import optuna
                from optuna.distributions import UniformDistribution


                def objective(trial):
                    x = trial.suggest_uniform("x", 0, 10)
                    return x ** 2


                study = optuna.create_study()
                assert len(study.trials) == 0

                trial = optuna.trial.create_trial(
                    params={"x": 2.0},
                    distributions={"x": UniformDistribution(0, 10)},
                    value=4.0,
                )

                study.add_trial(trial)
                assert len(study.trials) == 1

                study.optimize(objective, n_trials=3)
                assert len(study.trials) == 4

                other_study = optuna.create_study()

                for trial in study.trials:
                    other_study.add_trial(trial)
                assert len(other_study.trials) == len(study.trials)

                other_study.optimize(objective, n_trials=2)
                assert len(other_study.trials) == len(study.trials) + 2

        .. seealso::

            This method should in general be used to add already evaluated trials
            (``trial.state.is_finished() == True``). To queue trials for evaluation,
            please refer to :func:`~optuna.study.Study.enqueue_trial`.

        .. seealso::

            See :func:`~optuna.trial.create_trial` for how to create trials.

        Args:
            trial: Trial to add.

        Raises:
            :exc:`ValueError`:
                If trial is an invalid state.

        """

        trial._validate()

        self._storage.create_new_trial(self._experiment_id, template_trial=trial)

    def _pop_waiting_trial_id(self) -> Optional[int]:

        # TODO(c-bata): Reduce database query counts for extracting waiting trials.
        for trial in self._storage.get_all_trials(self._experiment_id, deepcopy=False):
            if trial.state != TrialState.WAITING:
                continue

            if not self._storage.set_trial_state(trial._trial_id, TrialState.RUNNING):
                continue

            _logger.debug("Trial {} popped from the trial queue.".format(trial.number))
            return trial._trial_id

        return None

    def _ask(self) -> trial_module.Trial:
        # Sync storage once at the beginning of the objective evaluation.
        self._storage.read_trials_from_remote_storage(self._experiment_id)

        trial_id = self._pop_waiting_trial_id()
        if trial_id is None:
            trial_id = self._storage.create_new_trial(self._experiment_id)
        return trial_module.Trial(self, trial_id)

    def _tell(self, trial: trial_module.Trial, state: TrialState, value: Optional[float]) -> None:
        if state == TrialState.COMPLETE:
            assert value is not None
        if value is not None:
            self._storage.set_trial_value(trial._trial_id, value)
        self._storage.set_trial_state(trial._trial_id, state)

    def _log_completed_trial(self, trial: trial_module.Trial, value: float) -> None:
        # This method is overwritten by `MultiObjectiveStudy` using `types.MethodType` so one must
        # be careful modifying this method, e.g. making this a free function.

        if not _logger.isEnabledFor(logger.INFO):
            return

        _logger.info(
            "Trial {} finished with value: {} and parameters: {}. "
            "Best is trial {} with value: {}.".format(
                trial.number, value, trial.params, self.best_trial.number, self.best_value
            )
        )


def create_experiment(
    storage: Optional[Union[str, storages.BaseStorage]] = None,
    sampler: Optional["samplers.BaseSampler"] = None,
    stopper: Optional[stoppers.BaseStopper] = None,
    experiment_name: Optional[str] = None,
    direction: str = "minimize",
    load_if_exists: bool = False,
) -> Experiment:
    """Create a new :class:`~opts.experiment.Experiment`.


    """

    storage = storages.get_storage(storage)
    try:
        experiment_id = storage.create_new_experiment(experiment_name)
    except errors.DuplicatedExperimentError:
        if load_if_exists:
            assert experiment_name is not None

            _logger.info(
                "Using an existing study with name '{}' instead of "
                "creating a new one.".format(experiment_name)
            )
            experiment_id = storage.get_experiment_id_from_name(experiment_name)
        else:
            raise

    experiment_name = storage.get_experiment_name_from_id(experiment_id)
    experiment = Experiment(experiment_name=experiment_name, storage=storage, sampler=sampler, stopper=stopper)

    if direction == "minimize":
        _direction = ExperimentDirection.MINIMIZE
    elif direction == "maximize":
        _direction = ExperimentDirection.MAXIMIZE
    else:
        raise ValueError("Please set either 'minimize' or 'maximize' to direction.")

    experiment._storage.set_experiment_direction(experiment_id, _direction)

    return experiment


def load_experiment(
    experiment_name: str,
    storage: Union[str, storages.BaseStorage],
    sampler: Optional["samplers.BaseSampler"] = None,
    stopper: Optional[stoppers.BaseStopper] = None,
) -> Experiment:
    """

    """

    return Experiment(experiment_name=experiment_name, storage=storage, sampler=sampler, stopper=stopper)


def delete_experiment(
    experiment_name: str,
    storage: Union[str, storages.BaseStorage],
) -> None:
    """Delete a :class:`~optuna.study.Study` object.

    Example:

        .. testsetup::

            import os

            if os.path.exists("example.db"):
                raise RuntimeError("'example.db' already exists. Please remove it.")

        .. testcode::

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", -10, 10)
                return (x - 2) ** 2


            study = optuna.create_study(study_name="example-study", storage="sqlite:///example.db")
            study.optimize(objective, n_trials=3)

            optuna.delete_study(study_name="example-study", storage="sqlite:///example.db")

        .. testcleanup::

            os.remove("example.db")

    Args:
        study_name:
            Study's name.
        storage:
            Database URL such as ``sqlite:///example.db``. Please see also the documentation of
            :func:`~optuna.study.create_study` for further details.

    See also:
        :func:`optuna.delete_study` is an alias of :func:`optuna.study.delete_study`.

    """

    storage = storages.get_storage(storage)
    experiment_id = storage.get_experiment_id_from_name(experiment_name)
    storage.delete_experiment(experiment_id)


def get_all_experiment_summaries(storage: Union[str, storages.BaseStorage]) -> List[ExperimentSummary]:
    """Get all history of studies stored in a specified storage.

    Example:

        .. testsetup::

            import os

            if os.path.exists("example.db"):
                raise RuntimeError("'example.db' already exists. Please remove it.")

        .. testcode::

            import optuna


            def objective(trial):
                x = trial.suggest_float("x", -10, 10)
                return (x - 2) ** 2


            study = optuna.create_study(study_name="example-study", storage="sqlite:///example.db")
            study.optimize(objective, n_trials=3)

            study_summaries = optuna.study.get_all_study_summaries(storage="sqlite:///example.db")
            assert len(study_summaries) == 1

            study_summary = study_summaries[0]
            assert study_summary.study_name == "example-study"

        .. testcleanup::

            os.remove("example.db")

    Args:
        storage:
            Database URL such as ``sqlite:///example.db``. Please see also the documentation of
            :func:`~optuna.study.create_study` for further details.

    Returns:
        List of study history summarized as :class:`~optuna.study.StudySummary` objects.

    See also:
        :func:`optuna.get_all_study_summaries` is an alias of
        :func:`optuna.study.get_all_study_summaries`.

    """

    storage = storages.get_storage(storage)
    return storage.get_all_experiment_summaries()
