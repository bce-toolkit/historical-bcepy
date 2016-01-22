#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import sympy as _sympy

SUPPORTED = ["pow", "sqrt"]
ARGUMENT_COUNT = {"pow": 2, "sqrt": 1}


def do_sqrt(x):
    """Get the value of sqrt(x).

    :param x: The |x|.
    :return: The value of sqrt(x).
    """

    #  Call sqrt routine in SymPy package to do this operation.
    return _sympy.sqrt(x)