#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 1999-2020 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod
from typing import Union, Dict

from enum import Enum


class StorageLevel(Enum):
    GPU = 1 << 0
    MEMORY = 1 << 1
    DISK = 1 << 2
    REMOTE = 1 << 3

    def __or__(self, other: "StorageLevel"):
        return self.value | other.value


class ObjectInfo:
    def __init__(self, size=None, device=None, object_id=None):
        self._size = size
        self._device = device
        self._object_id = object_id

    @property
    def size(self):
        return self._size

    @property
    def device(self):
        return self._device

    @property
    def object_id(self):
        return self._object_id


class StorageInfo:
    def __init__(self, total_size=None, used_size=None):
        self._total_size = total_size
        self._used_size = used_size

    @property
    def total_size(self):
        return self._total_size

    @property
    def used_size(self):
        return self._used_size


class FileObject:
    def __init__(self, file_obj, object_id=None):
        self._file_obj = file_obj
        self._object_id = object_id

    @property
    def object_id(self):
        return self._object_id or self._file_obj.name

    def __getattr__(self, item):
        return getattr(self._file_obj, item)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self._file_obj.__exit__(exc_type, exc_val, exc_tb)


class StorageBackend(ABC):
    @classmethod
    async def setup(cls, **kwargs) -> Union[Dict, None]:
        """
        Setup environments, for example, start plasma store for plasma backend.

        Parameters
        ----------
        kwargs : kwargs
            Kwargs for setup.

        Returns
        -------
        Dict
            Parameters for initialization.
        """
        return dict()

    @classmethod
    async def teardown(cls, **kwargs) -> None:
        """
        Clean up the environments.

        Parameters
        ----------
        kwargs : kwargs
             Parameters for clean up.

        Returns
        -------
        None

        """
        pass

    @property
    def level(self):
        raise NotImplementedError

    @abstractmethod
    async def get(self, object_id, **kwargs) -> object:
        """
        Get object by key. For some backends, `columns` or `slice` can pass to get part of data.

        Parameters
        ----------
        object_id : object id
            Object id to get.

        kwargs:
            Additional keyword arguments

        Returns
        -------
        Python object

        """
        pass

    @abstractmethod
    async def put(self, obj, importance=0) -> ObjectInfo:
        """
        Put object into storage with object_id.

        Parameters
        ----------
        obj : python object
            Object to put.

        importance: int
             The priority to spill when storage is full

        Returns
        -------
        ObjectInfo
            object information including size, raw_size, device

        """
        pass

    @abstractmethod
    async def delete(self, object_id):
        """
        Delete object from storage by object_id.

        Parameters
        ----------
        object_id
            object id

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    async def object_info(self, object_id) -> ObjectInfo:
        """
        Get information about stored object.

        Parameters
        ----------
        object_id
            object id

        Returns
        -------
        ObjectInfo
            Object info including size, device and etc.

        """
        pass

    @abstractmethod
    async def create_writer(self, size=None) -> FileObject:
        """
        Return a file-like object for writing.

        Parameters
        ----------
        size: int
            Maximum size in bytes

        Returns
        -------
        file-like object

        """
        pass

    @abstractmethod
    async def open_reader(self, object_id) -> FileObject:
        """
        Return a file-like object for reading.

        Parameters
        ----------
        object_id
            Object id

        Returns
        -------
            file-like object

        """
        pass

    async def migrate(self, object_id, destination, device=None):
        """
        Migrating object from local to other worker.

        Parameters
        ----------
        object_id
            Object id.

        destination : str
            Target worker.

        device : str
            Device for store.

        Returns
        -------
        None

        """
        pass

    async def pin(self, object_id):
        """
        Pin the data.

        Parameters
        ----------
        object_id
            object id

        Returns
        -------
        None

        """
        pass

    async def unpin(self, object_id):
        """
        Unpin the data.

        Parameters
        ----------
        object_id
            object id

        Returns
        -------
        None

        """
        pass
