"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/11/28 2:31 下午
@Software: PyCharm
@File    : __init__.py.py
@E-mail  : victor.xsyang@gmail.com
"""
from typing import Union

from opts.storages._base import BaseStorage
from opts.storages._in_memory import InMemoryStorage
from opts.storages._redis import RedisStorage
from opts.storages._cached_storage import _CachedStorage
from opts.storages._rdb.storage import RDBStorage

__all__ = [
    "BaseStorage",
    "InMemoryStorage",
    "RDBStorage",
    "RedisStorage",
    "_CachedStorage",
]


def get_storage(storage: Union[None, str, BaseStorage]) -> BaseStorage:

    if storage is None:
        return InMemoryStorage()
    if isinstance(storage, str):
        if storage.startswith("redis"):
            return RedisStorage(storage)
        else:
            return _CachedStorage(RDBStorage(storage))
    elif isinstance(storage, RDBStorage):
        return _CachedStorage(storage)
    else:
        return storage
