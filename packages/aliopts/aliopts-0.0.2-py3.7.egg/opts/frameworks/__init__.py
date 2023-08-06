"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/17 3:05 下午
@Software: PyCharm
@File    : __init__.py.py
@E-mail  : victor.xsyang@gmail.com
"""
import os
import sys
from types import ModuleType
from typing import Any
from typing import TYPE_CHECKING


_import_structure = {
    "cma": ["CmaEsSampler", "PyCmaSampler"],
    "pytorch_ignite": ["PytorchIgniteStoppinghandler"],
    "pytorch_lightning": ["PytorchLightningStoppingCallback"],
    "skopt": ["SkoptSampler"],
}

__all__ = list(_import_structure.keys()) + sum(_import_structure.values(), [])

if TYPE_CHECKING:

    from opts.frameworks.cma import CmaEsSampler  # NOQA
    from opts.frameworks.cma import PyCmaSampler  # NOQA
    from opts.frameworks.pytorch_ignite import PytorchIgniteStoppinghandler  # NOQA
    from opts.frameworks.pytorch_lightning import PytorchLightningStoppingCallback  # NOQA
    from opts.frameworks.skopt import SkoptSampler  # NOQA
else:

    class _IntegrationModule(ModuleType):
        """Module class that implements `opts.framework` package.

        """

        __file__ = globals()["__file__"]
        __path__ = [os.path.dirname(__file__)]

        _modules = set(_import_structure.keys())
        _class_to_module = {}
        for key, values in _import_structure.items():
            for value in values:
                _class_to_module[value] = key

        def __getattr__(self, name: str) -> Any:

            if name in self._modules:
                value = self._get_module(name)
            elif name in self._class_to_module.keys():
                module = self._get_module(self._class_to_module[name])
                value = getattr(module, name)
            else:
                raise AttributeError("module {} has no attribute {}".format(self.__name__, name))

            setattr(self, name, value)
            return value

        def _get_module(self, module_name: str) -> ModuleType:

            import importlib

            return importlib.import_module("." + module_name, self.__name__)

    sys.modules[__name__] = _IntegrationModule(__name__)
