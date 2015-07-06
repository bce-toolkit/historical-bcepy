#!/usr/bin/env python
#
#  Copyright 2014-2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

#
#  This file was copied and modified from SymPy's source code.
#  Original source location: [SymPy source dir]/sympy/printing/mathematica.py
#
#  Coding-style notes:
#    1)  Keep origin coding-style (SymPy's coding style) except the
#        routine wrote by ourselves.
#    2)  Remove all warnings.
#

import sympy.printing.codeprinter as _sympy_cp
import sympy.printing.str as _sympy_print_str
import sympy.printing.precedence as _sympy_prec

_known_functions = {
}


class _MEXPPrinter(_sympy_cp.CodePrinter):
    """A printer to convert python expressions to strings of the BCE's MEXP form."""

    _default_settings = {
        'order': None,
        'full_prec': 'auto',
        'precision': 15,
        'user_functions': {},
        'human': True,
    }

    _number_symbols = set()
    _not_supported = set()

    def __init__(self):
        """Register function mappings supplied by user"""
        _sympy_cp.CodePrinter.__init__(self, {})
        self.known_functions = dict(_known_functions)

    doprint = _sympy_print_str.StrPrinter.doprint

    def _print_Pow(self, expr, rational=False):
        prec = _sympy_prec.precedence(expr)
        return '%s^%s' % (self.parenthesize(expr.base, prec),
                          self.parenthesize(expr.exp, prec))

    def _print_Mul(self, expr):
        prec = _sympy_prec.precedence(expr)
        c, nc = expr.args_cnc()
        res = super(_MEXPPrinter, self)._print_Mul(expr.func(*c))
        if nc:
            res += '*'
            res += '^'.join(self.parenthesize(a, prec) for a in nc)
        return res

    def _print_Function(self, expr):
        if expr.func.__name__ in self.known_functions:
            cond_mfunc = self.known_functions[expr.func.__name__]
            for cond, mfunc in cond_mfunc:
                if cond(*expr.args):
                    return "%s(%s)" % (mfunc, self.stringify(expr.args, ","))
        return expr.func.__name__ + "(%s)" % self.stringify(expr.args, ",")


def decompile_mexp(expr):
    """Represent the expression in BCE's MEXP form.

    :param expr: The expression.
    :rtype : str
    :return: The BCE-MEXP form string.
    """

    return _MEXPPrinter().doprint(expr).replace(" ", "")