"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/2 3:04 下午
@Software: PyCharm
@File    : _imports.py
@E-mail  : victor.xsyang@gmail.com
"""
from types import TracebackType
from typing import Optional
from typing import Tuple
from typing import Type


class _DeferredImportExceptionContextManager(object):
    """Context manager to defer exceptions from imports.

    """

    def __init__(self) -> None:
        self._deferred: Optional[Tuple[Exception, str]] = None

    def __enter__(self) -> "_DeferredImportExceptionContextManager":
        return self

    def __exit__(self,
                 exc_type: Optional[Type[Exception]],
                 exc_val: Optional[Exception],
                 exc_tb: Optional[TracebackType]
                 ) -> Optional[bool]:
        """Exit the context manager.

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        if isinstance(exc_val, (ImportError, SyntaxError)):
            if isinstance(exc_val, ImportError):
                message = (
                    "Tried to import '{}' but failed. Please make sure that the package is "
                    "installed correctly to use this feature. Actual error: {}."
                ).format(exc_val.name, exc_val)
            elif isinstance(exc_val, SyntaxError):
                message = (
                    "Tried to import a package but failed due to a syntax error in {}. Please "
                    "make sure that the Python version is correct to use this feature. Actual "
                    "error: {}."
                ).format(exc_val.filename, exc_val)
            else:
                assert False

            self._deferred = (exc_val, message)
            return True
        return None

    def is_successful(self) -> bool:
        """Return whether the context manager has caught any exceptions.

        :return:
        """
        return self._deferred is None

    def check(self) -> None:
        """Check whether the context manager has caught any exceptions.

        :return:
        """
        if self._deferred is not None:
            exc_val, message = self._deferred
            raise ImportError(message) from exc_val

def try_import() -> _DeferredImportExceptionContextManager:
    """Create a context manager that can wrap imports of optional packages to defer exceptions.

    :return:
    """
    return _DeferredImportExceptionContextManager()