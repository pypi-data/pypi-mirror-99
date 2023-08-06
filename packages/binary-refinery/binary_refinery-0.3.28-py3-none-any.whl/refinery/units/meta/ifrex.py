#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..pattern import arg, RegexUnit
from . import ConditionalUnit


class ifrex(RegexUnit, ConditionalUnit):
    """
    Filter incoming chunks by discarding those that do not match the given
    regular expression.
    """
    def __init__(
        self, regex, multiline=False, ignorecase=False, negate=False,
        match: arg.switch('-m',
            help='Perform a full match rather than matching anywhere in the chunk.') = False
    ):
        super().__init__(regex=regex, negate=negate, multiline=multiline, ignorecase=ignorecase, match=match)

    def match(self, chunk):
        return bool(self._matcher(chunk))

    def filter(self, inputs):
        self._matcher = self.args.regex.fullmatch if self.args.match else self.args.regex.search
        yield from super().filter(inputs)
