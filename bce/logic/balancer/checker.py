#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.logic.balancer.modeling as _bce_model
import bce.math.equation as _math_equ
import bce.parser.ce.base as _ce_base


def check_whether_balanced(ce):
    """Check whether a chemical equation is balanced.

    :type ce: _ce_base.ChemicalEquation
    :param ce: The chemical equation (presented by ChemicalEquation class).
    :rtype : bool
    :return: Return True if it's balanced.
    """

    #  Build matrix.
    mtx = _bce_model.build_matrix(ce)

    #  Generate the solution of the matrix from the expression.
    pfx_list = []
    for i in range(0, ce.get_left_item_count()):
        pfx_list.append(ce.get_left_item(i).get_coefficient())
    for i in range(0, ce.get_right_item_count()):
        pfx_list.append(ce.get_right_item(i).get_coefficient())

    #  Check whether the solution matches with the matrix.
    return _math_equ.check_solved_answer(mtx, _math_equ.SolvedEquation(pfx_list, 0))
