# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import yaml
import yaml.scanner

from ..err import SerializeError
from ..abc import *
from ..core import register_format

@register_format('yaml', '.yaml', '.yml')
class YamlSerializer(ISerializer):
    format_name = 'yaml'

    def loads(self, s: str, options: dict):
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        try:
            return yaml.safe_load(s, **kwargs)
        except yaml.scanner.ScannerError as e:
            raise SerializeError(e)

    def dumps(self, obj, options: dict) -> str:
        kwargs = {
            'allow_unicode': not Options.pop_ensure_ascii(options),
            'indent': Options.pop_indent(options),
        }
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        return yaml.dump(obj, **kwargs)
