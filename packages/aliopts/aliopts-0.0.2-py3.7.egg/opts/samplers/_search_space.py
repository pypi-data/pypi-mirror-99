"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/10 10:33 上午
@Software: PyCharm
@File    : _search_space.py
@E-mail  : victor.xsyang@gmail.com
"""
from collections import OrderedDict
import copy
from typing import Dict
from typing import Optional

import opts
from opts.samples import BaseDistribution
from opts.experiment import BaseExperiment


class IntersectionSearchSpace(object):
    """A class to calculate the intersection search space of a :class:`~opts.experiment.BaseExperiment`.

    """

    def __init__(self) -> None:
        self._cursor: int = -1
        self._search_space: Optional[Dict[str, BaseDistribution]] = None
        self._experiment_id: Optional[int] = None

    def calculate(
            self, experiment: BaseExperiment,
            ordered_dict: bool = False
    ) -> Dict[str, BaseDistribution]:
        """:Returns the intersection search space of the :class:`~opts.experiment.BaseExperiment`


        :param experiment:
        :param ordered_dict:
        :return:
        """
        if self._experiment_id is None:
            self._experiment_id = experiment._experiment_id
        else:
            if self._experiment_id != experiment._experiment_id:
                raise ValueError("`IntersectionSearchSpace` cannot handle multiple studies.")

        next_cursor = self._cursor
        for trial in reversed(experiment._storage.get_all_trials(experiment._experiment_id, deepcopy=False)):
            if self._cursor > trial.number:
                break

            if not trial.state.is_finished():
                next_cursor = trial.number

            if trial.state != opts.trial.TrialState.COMPLETE:
                continue

            if self._search_space is None:
                self._search_space = copy.copy(trial.distributions)
                continue

            delete_list = []
            for param_name, param_distribution in self._search_space.items():
                if param_name not in trial.distributions:
                    delete_list.append(param_name)
                elif trial.distributions[param_name] != param_distribution:
                    delete_list.append(param_name)

            for param_name in delete_list:
                del self._search_space[param_name]

        self._cursor = next_cursor
        search_space = self._search_space or {}

        if ordered_dict:
            search_space = OrderedDict(sorted(search_space.items(), key=lambda x: x[0]))

        return copy.deepcopy(search_space)


def intersection_search_space(
        experiment: BaseExperiment, ordered_dict: bool = False
) -> Dict[str, BaseDistribution]:
    """Return the intersection search space of the :class:`~opts.experiment.BaseExperiment`.
    :param experiment:
    :param ordered_dict:
    :return:
    """
    return IntersectionSearchSpace().calculate(experiment, ordered_dict=ordered_dict)
