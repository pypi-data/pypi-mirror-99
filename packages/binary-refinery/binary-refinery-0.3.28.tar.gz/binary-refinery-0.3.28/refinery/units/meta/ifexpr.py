#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ...lib.argformats import PythonExpression
from . import arg, ConditionalUnit


class ifexpr(ConditionalUnit):
    """
    Filter incoming chunks depending on whether a given Python expression evaluates
    to true.
    """
    def __init__(
        self,
        *expression: arg(metavar='token', type=str, help=(
            'All "token" arguments to this unit are joined with spaces to produce the expression to be '
            'evaluated. This is done so that unnecessary shell quoting is avoided.')),
        negate=False
    ):
        super().__init__(negate=negate, expression=' '.join(expression))

    def match(self, chunk):
        return bool(PythonExpression.evaluate(self.args.expression, **getattr(chunk, 'meta', {})))
