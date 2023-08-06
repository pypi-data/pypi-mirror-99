'''
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/24 3:50 下午
@Software: PyCharm
@File    : errors.py
@E-mail  : victor.xsyang@gmail.com
'''
class OptsError(Exception):
    """Base class for Opts specific errors."""

    pass

class TrialStop(OptsError):

    pass

class CLIUsageError(OptsError):
    """Exception for CLI.

    CLI raises this exception when it receives invalid configuration.
    """

    pass

class StorageInternalError(OptsError):
    """Exception for storage operation.

    This error is raised when an operation failed in backend DB of storage.
    """

    pass

class DuplicatedExperimentError(OptsError):
    """Exception for a duplicated experiment name.

    This error is raised when a specified experiment name already exists in the storage.
    """
    pass

class ExperimentalWarning(Warning):
    """Experimental Warning class.

    This implementation exists here because the policy of `FutureWarning` has been changed
    since Python 3.7 was released. See the details in
    https://docs.python.org/3/library/warnings.html#warning-categories.
    """

    pass