# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import bencodepy

from ..err import SerializeError
from ..abc import *
from ..core import register_format

@register_format('bencode', '.torrent')
class BencodeSerializer(ISerializer):
    format_name = 'bencode'

    def loadb(self, b: bytes, options: dict) -> Any:
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        try:
            return bencodepy.decode(b, **kwargs)
        except bencodepy.BencodeDecodeError as e:
            raise SerializeError(e)

    def loads(self, s: str, options):
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        bc = bencodepy.Bencode(encoding='utf-8')
        try:
            return bc.decode(s, **kwargs)
        except bencodepy.BencodeDecodeError as e:
            raise SerializeError(e)

    def dumpb(self, obj, options: dict) -> bytes:
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        try:
            return bencodepy.encode(obj, **kwargs)
        except TypeError as e:
            raise SerializeError(e)
