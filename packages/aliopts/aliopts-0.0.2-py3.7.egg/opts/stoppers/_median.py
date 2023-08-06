"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/26 8:26 下午
@Software: PyCharm
@File    : _median.py
@E-mail  : victor.xsyang@gmail.com
"""
from opts.stoppers._percentile import PercentileStopper


class MedianStopper(PercentileStopper):
    """Stopping using the median stopping rule.


    """

    def __init__(
        self, n_startup_trials: int = 5, n_warmup_steps: int = 0, interval_steps: int = 1
    ) -> None:

        super(MedianStopper, self).__init__(50.0, n_startup_trials, n_warmup_steps, interval_steps)