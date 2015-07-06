#!/usr/bin/env python
#
#  Copyright 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import sympy as _sym

import bce.option as _opt
import bce.parser.common.error as _pe
import bce.parser.ce.token as _tok
import bce.parser.ce.parser as _par
import bce.logic.substitution as _sss
import bce.logic.decompiler.to_bce as _reb
import bce.logic.decompiler.to_mathml as _mll


subst_map = {"x": _sym.Integer(2), "y": _sym.Symbol("z")}
opt = _opt.Option()

expr = "Na2CO3(s)+HCl(aq)=NaCl(aq)+H2O(aq)+CO2(g)"
import bce.logic.error as _le

try:
    tk = _tok.tokenize(expr, opt)
    opt.set_protected_math_symbol_header("_")
    parsed = _par.parse(expr, tk, False, opt)
    rb = _sss.substitute_ce(parsed, subst_map, opt)
    print(_mll.decompile_combined_result(rb, opt).to_string())
except _pe.Error as err:
    print(err.to_string())
except _le.LogicError as err2:
    print(err2.to_string())
