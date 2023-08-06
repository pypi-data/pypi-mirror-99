"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/9 9:21 上午
@Software: PyCharm
@File    : _grid.py
@E-mail  : victor.xsyang@gmail.com
"""
import collections
import itertools
import random
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Sequence
from typing import Union

from opts.samples import BaseDistribution
from opts.logger import get_logger
from opts.samplers import BaseSampler
from opts.experiment import Experiment
from opts.trial import FrozenTrial

GridValueType = Union[str, float, int, bool, None]

_logger = get_logger(__name__)

class GridSampler(BaseSampler):
    """Sampler using grid search.
    With :class:`~opts.samplers.GridSampler`,
    the trials suggest all combinations of
    parameters in the given search space during the experiment.
    """
    def __init__(self, search_space: Mapping[str, Sequence[GridValueType]]) -> None:
        for param_name, param_values in search_space.items():
            for value in param_values:
                self._check_value(param_name, value)

        self._search_space = collections.OrderedDict()
        for param_name, param_values in sorted(search_space.items(), key=lambda x: x[0]):
            self._search_space[param_name] = sorted(param_values)

        self._all_grids = list(itertools.product(*self._search_space.values()))
        self._param_names = sorted(search_space.keys())
        self._n_min_trials = len(self._all_grids)

    def infer_relative_search_space(
            self, experiment: Experiment,
            trial: FrozenTrial) -> Dict[str, BaseDistribution]:
        return {}

    def sample_relative(
            self, experiment: Experiment, trial: FrozenTrial,
            search_space: Dict[str, BaseDistribution]
    ) -> Dict[str, Any]:
        target_grids = self._get_unvisited_grid_ids(experiment)
        if len(target_grids) == 0:
            _logger.warning(
                "`GridSampler` is re-evaluating a configuration because the grid has been "
                "exhausted. This may happen due to a timing issue during distributed optimization "
                "or when re-running optimizations on already finished studies."
            )
            target_grids = list(range(len(self._all_grids)))
            experiment.stop()
        elif len(target_grids) == 1:
            experiment.stop()

        grid_id = random.choice(target_grids)
        experiment._storage.set_trial_system_attr(trial._trial_id, "search_space", self._search_space)
        experiment._storage.set_trial_system_attr(trial._trial_id,"grid_id", grid_id)
        return {}

    def sample_independent(
            self,
            experiment: Experiment,
            trial: FrozenTrial,
            param_name: str,
            param_distribution: BaseDistribution
                           ) -> Any:
        if param_name not in self._search_space:
            message = "The parameter name, {}, is not found in the given grid.".format(param_name)
            raise ValueError(message)

        grid_id = trial.system_attrs["grid_id"]
        param_value = self._all_grids[grid_id][self._param_names.index(param_name)]
        contains = param_distribution._contains(param_distribution.to_internal_repr(param_value))
        if not contains:
            raise ValueError(
                "The value `{}` is out of range of the parameter `{}`. Please make "
                "sure the search space of the `GridSampler` only contains values "
                "consistent with the distribution specified in the objective "
                "function. The distribution is: `{}`.".format(
                    param_value, param_name, param_distribution
                )
            )
        return param_value

    def _get_unvisited_grid_ids(self, experiment: Experiment) -> List[int]:
        visited_grids = []
        for t in experiment.trials:
            if (
                t.state.is_finished()
                and "grid_id" in t.system_attrs
                and self._same_search_space(t.system_attrs["search_space"])
            ):
                visited_grids.append(t.system_attrs["grid_id"])
        unvisited_grids = set(range(self._n_min_trials)) - set(visited_grids)
        return list(unvisited_grids)

    def _same_search_space(self, search_space: Mapping[str, Sequence[GridValueType]]) -> bool:
        if set(search_space.keys()) != set(self._search_space.keys()):
            return False

        for param_name in search_space.keys():
            if len(search_space[param_name]) != len(self._search_space[param_name]):
                return False

            for i, param_value in enumerate(sorted(search_space[param_name])):
                if param_value != self._search_space[param_name][i]:
                    return False
        return True

    @staticmethod
    def _check_value(param_name: str, param_value: Any) -> None:
        if param_value is None or isinstance(param_value, (str, int, float, bool)):
            return

        raise ValueError(
            "{} contains a value with the type of {}, which is not supported by "
            "`GridSampler`. Please make sure a value is `str`, `int`, `float`, `bool`"
            " or `None`.".format(param_name, type(param_value))
        )