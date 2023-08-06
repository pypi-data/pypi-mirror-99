"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/8 2:42 下午
@Software: PyCharm
@File    : progress_bar.py
@E-mail  : victor.xsyang@gmail.com
"""
import logging
from typing import Any
from typing import Optional

from tqdm.auto import tqdm

from opts import logger as opts_logger
from opts._experimental import experimental


class _TqdmLoggingHandler(logging.StreamHandler):
    def emit(self, record: Any) -> None:
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)

_tqdm_handler: Optional[_TqdmLoggingHandler]

class _ProgressBar(object):
    """Progress Bar implementation for `Experiment.optimize` on the top of `tqdm`.

    """
    def __init__(
            self, is_valid: bool, n_trials: Optional[int] = None,
            timeout: Optional[float] = None
    ) -> None:
        self._is_valid = is_valid
        self._n_trials = n_trials
        self._timeout = timeout
        if self._is_valid:
            self._init_valid()

    @experimental("1.2.0", name="Progress bar")
    def _init_valid(self) -> None:
        self._progress_bar = tqdm(range(self._n_trials) if self._n_trials is not None else None)
        global _tqdm_handler

        _tqdm_handler = _TqdmLoggingHandler()
        _tqdm_handler.setLevel(logging.INFO)
        _tqdm_handler.setFormatter(opts_logger.create_default_formatter())
        opts_logger.disable_default_handle()
        opts_logger._get_library_root_logger().addHandler(_tqdm_handler)

    def update(self, elapsed_seconds: Optional[float]) -> None:
        """Update the progress bars id ``is_valid`` is ``True``.

        :param elapsed_seconds:
        :return:
        """
        if self._is_valid:
            self._progress_bar.update(1)
            if self._timeout is not None and elapsed_seconds is not None:
                self._progress_bar.set_postfix_str(
                    "{:.02f}/{} seconds".format(elapsed_seconds, self._timeout)
                )

    def close(self) -> None:
        """Close progress bars."""
        if self._is_valid:
            self._progress_bar.close()
            assert _tqdm_handler is not None
            opts_logger._get_library_root_logger().removeHandler(_tqdm_handler)
            opts_logger.enable_default_handler()