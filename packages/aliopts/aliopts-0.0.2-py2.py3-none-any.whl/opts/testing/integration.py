"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/26 4:20 下午
@Software: PyCharm
@File    : integration.py
@E-mail  : victor.xsyang@gmail.com
"""
import opts


class DeterministicStopper(opts.stoppers.BaseStopper):
    def __init__(self, is_stopping: bool) -> None:

        self.is_stopping = is_stopping

    def stop(self, experiment: "opts.experiment.Experiment", trial: "opts.trail.FrozenTrial") -> bool:

        return self.is_stopping


def create_running_trial(experiment: "opts.experiment.Experiment", value: float) -> opts.trial.Trial:

    trial_id = experiment._storage.create_new_trial(experiment._experiment_id)
    experiment._storage.set_trial_value(trial_id, value)
    return opts.trial.Trial(experiment, trial_id)
