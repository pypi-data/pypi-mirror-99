"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/25 4:55 下午
@Software: PyCharm
@File    : _base.py
@E-mail  : victor.xsyang@gmail.com
"""
import abc
import opts


class BaseStopper(object, metaclass=abc.ABCMeta):
    """Base class for stoppers."""

    @abc.abstractmethod
    def stop(self, experiment: "opts.experiment.Experiment", trial: "opts.trail.FrozenTrial") -> bool:
        """Judge whether the trial should be pruned based on the reported values.

        :param experiment:
        :param trial:
        :return:
        """
        raise NotImplementedError
