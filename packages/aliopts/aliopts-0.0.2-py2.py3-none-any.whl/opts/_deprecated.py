"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/27 6:46 下午
@Software: PyCharm
@File    : _deprecated.py
@E-mail  : victor.xsyang@gmail.com
"""
import functools
import inspect
import textwrap
from typing import Any
from typing import Callable
from typing import Optional
import warnings

from packaging import version

from opts._experimental import _get_docstring_indent
from opts._experimental import _validate_version

_DEPRECATION_NOTE_TEMPLATE = """
.. warning::
    Deprecated in v{d_ver}. This feature will be removed in the future. The removal of this
    feature is currently scheduled for v{r_ver}, but this schedule is subject to change.
"""

def _validate_two_version(old_version: str, new_version: str) -> None:
    if version.parse(old_version) > version.parse(new_version):
        raise ValueError(
            "Invalid version relationship. The deprecated version must be smaller than "
            "the removed version, but (deprecated version, removed version) = ({}, {}) are "
            "specified.".format(old_version, new_version)
        )

def _format_text(text: str) -> str:
    return "\n\n" + textwrap.indent(text.strip(), "    ") + "\n"

def _get_removed_version_from_deprecated_version(deprecated_version: str) -> str:
    parsed_deprecated_version = version.parse(deprecated_version)
    assert isinstance(parsed_deprecated_version, version.Version)  # Required for mypy.
    return "{}.0.0".format(parsed_deprecated_version.major + 2)

def deprecated(
    deprecated_version: str,
    removed_version: Optional[str] = None,
    name: Optional[str] = None,
    text: Optional[str] = None,
) -> Any:
    """Decorate class or function as deprecated.
    """

    _validate_version(deprecated_version)
    if removed_version is None:
        removed_version = _get_removed_version_from_deprecated_version(deprecated_version)
    _validate_version(removed_version)
    _validate_two_version(deprecated_version, removed_version)

    def _deprecated_wrapper(f: Any) -> Any:
        # f is either func or class.

        def _deprecated_func(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            """Decorates a function as deprecated.

            This decorator is supposed to be applied to the deprecated function.
            """
            if func.__doc__ is None:
                func.__doc__ = ""

            note = _DEPRECATION_NOTE_TEMPLATE.format(
                d_ver=deprecated_version, r_ver=removed_version
            )
            if text is not None:
                note += _format_text(text)
            indent = _get_docstring_indent(func.__doc__)
            func.__doc__ = func.__doc__.strip() + textwrap.indent(note, indent) + indent

            @functools.wraps(func)
            def new_func(*args: Any, **kwargs: Any) -> Any:
                warnings.warn(
                    "{} has been deprecated in v{}. "
                    "This feature will be removed in v{}.".format(
                        name if name is not None else func.__name__,
                        deprecated_version,
                        removed_version,
                    ),
                    FutureWarning,
                    stacklevel=2,
                )

                return func(*args, **kwargs)  # type: ignore

            return new_func

        def _deprecated_class(cls: Any) -> Any:
            """Decorates a class as deprecated.

            This decorator is supposed to be applied to the deprecated class.
            """
            _original_init = cls.__init__

            @functools.wraps(_original_init)
            def wrapped_init(self, *args, **kwargs) -> None:  # type: ignore
                warnings.warn(
                    "{} has been deprecated in v{}. "
                    "This feature will be removed in v{}.".format(
                        name if name is not None else cls.__name__,
                        deprecated_version,
                        removed_version,
                    ),
                    FutureWarning,
                    stacklevel=2,
                )

                _original_init(self, *args, **kwargs)

            cls.__init__ = wrapped_init

            if cls.__doc__ is None:
                cls.__doc__ = ""

            note = _DEPRECATION_NOTE_TEMPLATE.format(
                d_ver=deprecated_version, r_ver=removed_version
            )
            if text is not None:
                note += _format_text(text)
            indent = _get_docstring_indent(cls.__doc__)
            cls.__doc__ = cls.__doc__.strip() + textwrap.indent(note, indent) + indent

            return cls

        return _deprecated_class(f) if inspect.isclass(f) else _deprecated_func(f)

    return _deprecated_wrapper


