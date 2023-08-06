# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import Optional, Any, Union
from io import IOBase
from collections import ChainMap

from .err import *
from .abc import *

_REGISTERED_SERIALIZERS = {}

def register_format(*keys):
    '''
    register a serializer class for load and dump into global module.
    '''
    def decorator(cls):
        for k in keys:
            _REGISTERED_SERIALIZERS[k] = cls
        return cls
    return decorator

class ComplexSerializer:
    def __init__(self) -> None:
        self._serializers = ChainMap(_REGISTERED_SERIALIZERS).new_child()

    def register_format(self, *keys):
        '''
        register a serializer class for load and dump into this ComplexSerializer.
        '''
        def decorator(cls):
            for k in keys:
                self._serializers[k] = cls
            return cls
        return decorator

    def get_available_formats(self) -> list:
        '''
        get all available formats.
        '''
        return list(self._serializers)

    def _find_serializer(self, format: str) -> Optional[ISerializer]:
        if not isinstance(format, str):
            raise TypeError

        cls = self._serializers.get(format)
        if cls is not None:
            return cls()

    def _get_required_serializer(self, format: str) -> ISerializer:
        serializer = self._find_serializer(format)
        if not serializer:
            raise FormatNotFoundError(format)
        return serializer

    def load(self, s: Union[str, bytes, IOBase], format: str, **options) -> Any:
        'load a obj from source.'
        if not isinstance(s, (str, bytes, IOBase)):
            raise TypeError
        serializer = self._get_required_serializer(format)
        return serializer.load(s, options)

    def loads(self, s: str, format: str, **options) -> Any:
        'load a obj from str.'
        if not isinstance(s, str):
            raise TypeError
        serializer = self._get_required_serializer(format)
        return serializer.loads(s, options)

    def loadb(self, b: bytes, format: str, **options) -> Any:
        'load a obj from bytes.'
        if not isinstance(b, bytes):
            raise TypeError
        serializer = self._get_required_serializer(format)
        return serializer.loadb(b, options)

    def loadf(self, fp: IOBase, format: str, **options) -> Any:
        'load a obj from a file-like object.'
        if not isinstance(fp, IOBase):
            raise TypeError
        serializer = self._get_required_serializer(format)
        return serializer.loadf(fp, options)

    def dumps(self, obj, format: str, **options) -> str:
        '''
        dump a obj to str.

        options:

        - `ensure_ascii` - `bool`, default `True`.
        - `indent` - `int?`, default `None`.
        - `origin_kwargs` - `dict`, pass to serializer
        '''
        serializer = self._get_required_serializer(format)
        return serializer.dumps(obj, options)

    def dumpb(self, obj, format: str, **options) -> bytes:
        '''
        dump a obj to bytes.

        options:

        - `encoding` - `str`, default `utf-8`.
        - `ensure_ascii` - `bool`, default `True`.
        - `indent` - `int?`, default `None`.
        - `origin_kwargs` - `dict`, pass to serializer
        '''
        serializer = self._get_required_serializer(format)
        return serializer.dumpb(obj, options)

    def dumpf(self, obj, fp: IOBase, format: str, **options):
        '''
        dump a obj into the file-like object.

        options:

        - `encoding` - `str`, default `utf-8`.
        - `ensure_ascii` - `bool`, default `True`.
        - `indent` - `int?`, default `None`.
        - `origin_kwargs` - `dict`, pass to serializer
        '''
        if not isinstance(fp, IOBase):
            raise TypeError
        serializer = self._get_required_serializer(format)
        return serializer.dumpf(obj, fp, options)
