# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import Optional, Any, Union
from io import IOBase
from collections import ChainMap

from .err import *
from .abc import *
from .core import ComplexSerializer

_DEFAULE = ComplexSerializer()

register_format = _DEFAULE.register_format
get_available_formats = _DEFAULE.get_available_formats
load = _DEFAULE.load
loads = _DEFAULE.loads
loadb = _DEFAULE.loadb
loadf = _DEFAULE.loadf
dumps = _DEFAULE.dumps
dumpb = _DEFAULE.dumpb
dumpf = _DEFAULE.dumpf
dumps = _DEFAULE.dumps
