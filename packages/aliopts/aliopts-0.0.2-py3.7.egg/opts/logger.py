"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/24 4:01 下午
@Software: PyCharm
@File    : logger.py
@E-mail  : victor.xsyang@gmail.com
"""
import logging
from logging import CRITICAL
from logging import DEBUG
from logging import ERROR
from logging import FATAL
from logging import INFO
from logging import WARN
from logging import WARNING

import threading
from typing import Optional
import colorlog  # pip install

_lock: threading.Lock = threading.Lock()
_default_handler: Optional[logging.Handler] = None


def create_default_formatter() -> colorlog.ColoredFormatter:
    """Create a default formatter of log messages.
    This function is used by developers
    :return:colorlog.ColoredFormatter
    """
    return colorlog.ColoredFormatter(
        "%(log_color)s[%(levelname)1.1s %(asctime)s]%(reset)s %(message)s"
    )


def _get_library_name() -> str:
    """

    :return:
    """
    return __name__.split(".")[0]


def _get_library_root_logger() -> logging.Logger:
    """

    :return:
    """
    return logging.getLogger(_get_library_name())


def _confighure_library_root_logger() -> None:
    global _default_handler

    with _lock:
        if _default_handler:
            # This library has already configured the library root logger.
            return
        _default_handler = logging.StreamHandler()  # Set sys.stderr as stream.
        _default_handler.setFormatter(create_default_formatter())

        # Apply our default configuration to the library root logger.
        library_root_logger: logging.Logger = _get_library_root_logger()
        library_root_logger.addHandler(_default_handler)
        library_root_logger.setLevel(logging.INFO)
        library_root_logger.propagate = False


def _reset_library_root_logger() -> None:
    global _default_handler
    with _lock:
        if not _default_handler:
            return

        library_root_logger: logging.Logger = _get_library_root_logger()
        library_root_logger.removeHandler(_default_handler)
        library_root_logger.setLevel(logging.NOTSET)
        _default_handler = None


def get_logger(name: str) -> logging.Logger:
    """Return a logger with the specified name.
    This function is used by developers
    :param name: specified name
    :return:
    """

    _confighure_library_root_logger()
    return logging.getLogger(name)


def get_verbosity() -> int:
    """Return the current level for the opts's logger.

    :return: Logging level, e.g., ``opts.logger.DEBUG``
    and ``opts.logging.INFO``.

    note :
        opts has following logging levels:
        - ``opts.logging.CRITICAL``, ``opts.logging.FATAL``
        - ``opts.logging.ERROR``
        - ``opts.logging.WARNING``, ``opts.logging.WARN``
        - ``opts.logging.INFO``
        - ``opts.logging.DEBUG``
    """
    _confighure_library_root_logger()
    return _get_library_root_logger().getEffectiveLevel()


def set_verbosity(verbosity: int) -> None:
    """

    :param verbosity:
    :return:
    """
    _confighure_library_root_logger()
    _get_library_root_logger().setLevel(verbosity)


def disable_default_handler() -> None:
    """Disable the default handler of Opts's root logger.

    :return:
    """
    _confighure_library_root_logger()

    assert _default_handler is not None
    _get_library_root_logger().removeHandler(_default_handler)


def enable_default_handler() -> None:
    """Enable the default handler of the Opts's root logger

    :return:
    """
    _confighure_library_root_logger()
    assert _default_handler is not None
    _get_library_root_logger().addHandler(_default_handler)


def disable_propagation() -> None:
    """Disable propagation of the library log outputs.
    Note that log propagation is disabled by default
    :return:
    """
    _confighure_library_root_logger()
    _get_library_root_logger().propagate = False


def enable_propagation() -> None:
    """

    :return:
    """
    _confighure_library_root_logger()
    _get_library_root_logger().propagate = True