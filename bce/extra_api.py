#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#


import bce.decompiler.mexp.to_bce as _decompiler_mexp_to_bce
import bce.decompiler.mexp.to_mathml as _decompiler_mexp_to_mathml
import bce.api as _api
import bce.option as _opt


def decompile_mexp(value, decompilers, options):
    """Decompile a math expression.

    :type decompilers: list[int]
    :type options: _opt.Option
    :param value: The math expression.
    :param decompilers:  A list that contains the decompiler IDs.
    :param options: The BCE options.
    :rtype : list[str]
    :return: A list that contains the decompiling result.
    """

    #  Initialize.
    ret = []

    #  Decompile.
    for dec_id in decompilers:
        if dec_id == _api.DECOMPILER_TEXT:
            ret.append(_decompiler_mexp_to_bce.decompile_mexp(value))
        elif dec_id == _api.DECOMPILER_MATHML:
            ret.append(_decompiler_mexp_to_mathml.decompile_mexp(value, options.get_protected_math_symbol_header()))
        else:
            raise ValueError("Unsupported decompiler ID.")

    return ret