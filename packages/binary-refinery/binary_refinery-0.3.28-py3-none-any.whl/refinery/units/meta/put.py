#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools

from .. import arg, Unit
from ...lib.argformats import numseq
from ...lib.tools import isbuffer
from . import check_variable_name


class put(Unit):
    """
    Can be used to add a meta variable to the processed chunk. Note that meta variables
    cease to exist outside a frame.
    """
    def __init__(
        self,
        name : arg(help='The name of the variable to be used.', type=str),
        value: arg(help='The value for the variable.', type=numseq)
    ):
        super().__init__(name=check_variable_name(name), value=value)

    def process(self, data):
        value = self.args.value
        if not isinstance(value, int) and not isbuffer(value):
            try:
                len(value)
            except TypeError:
                if isinstance(value, itertools.repeat):
                    value = next(value)
                if not isinstance(value, int):
                    raise NotImplementedError(F'Unsupported value {value!r}; expected integer.')
            else:
                if not isinstance(value, list):
                    value = list(value)
        self.log_debug(F'storing {type(value).__name__}:', value)
        return self.labelled(data, **{self.args.name: value})
