"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/17 5:38 下午
@Software: PyCharm
@File    : test_logger.py
@E-mail  : victor.xsyang@gmail.com
"""
import logging

import _pytest.capture
import _pytest.logging

import opts.logger


def test_get_logger(caplog: _pytest.logging.LogCaptureFixture) -> None:
    # Log propagation is necessary for caplog to capture log outputs.
    opts.logger.enable_propagation()

    logger = opts.logger.get_logger("opts.foo")
    with caplog.at_level(logging.INFO, logger="opts.foo"):
        logger.info("hello")
    assert "hello" in caplog.text


def test_default_handler(capsys: _pytest.capture.CaptureFixture) -> None:
    # We need to reconstruct our default handler to properly capture stderr.
    opts.logger._reset_library_root_logger()
    opts.logger.set_verbosity(opts.logger.INFO)

    library_root_logger = opts.logger._get_library_root_logger()

    example_logger = opts.logger.get_logger("opts.bar")

    # Default handler enabled
    opts.logger.enable_default_handler()
    assert library_root_logger.handlers
    example_logger.info("hey")
    _, err = capsys.readouterr()
    assert "hey" in err

    # Default handler disabled
    opts.logger.disable_default_handler()
    assert not library_root_logger.handlers
    example_logger.info("yoyo")
    _, err = capsys.readouterr()
    assert "yoyo" not in err


def test_verbosity(capsys: _pytest.capture.CaptureFixture) -> None:
    # We need to reconstruct our default handler to properly capture stderr.
    opts.logger._reset_library_root_logger()
    library_root_logger = opts.logger._get_library_root_logger()
    example_logger = opts.logger.get_logger("opts.hoge")
    opts.logger.enable_default_handler()

    # level INFO
    opts.logger.set_verbosity(opts.logger.INFO)
    assert library_root_logger.getEffectiveLevel() == logging.INFO
    example_logger.warning("hello-warning")
    example_logger.info("hello-info")
    example_logger.debug("hello-debug")
    _, err = capsys.readouterr()
    assert "hello-warning" in err
    assert "hello-info" in err
    assert "hello-debug" not in err

    # level WARNING
    opts.logger.set_verbosity(opts.logger.WARNING)
    assert library_root_logger.getEffectiveLevel() == logging.WARNING
    example_logger.warning("bye-warning")
    example_logger.info("bye-info")
    example_logger.debug("bye-debug")
    _, err = capsys.readouterr()
    assert "bye-warning" in err
    assert "bye-info" not in err
    assert "bye-debug" not in err


def test_propagation(caplog: _pytest.logging.LogCaptureFixture) -> None:

    opts.logger._reset_library_root_logger()
    logger = opts.logger.get_logger("opts.foo")

    # Propagation is disabled by default.
    with caplog.at_level(logging.INFO, logger="opts"):
        logger.info("no-propagation")
    assert "no-propagation" not in caplog.text

    # Enable propagation.
    opts.logger.enable_propagation()
    with caplog.at_level(logging.INFO, logger="opts"):
        logger.info("enable-propagate")
    assert "enable-propagate" in caplog.text

    # Disable propagation.
    opts.logger.disable_propagation()
    with caplog.at_level(logging.INFO, logger="opts"):
        logger.info("disable-propagation")
    assert "disable-propagation" not in caplog.text