#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.math.equation as _math_equ
import bce.parser.ce.base as _ce_base


def merge_solving_result_into_ce(ce, solve_result):
    """Merge the solving result into chemical equation.

    :type ce: _ce_base.ChemicalEquation
    :type solve_result: _math_equ.SolvedEquation
    :param ce: The chemical equation (represented by ChemicalEquation class).
    :param solve_result: The solving result.
    """

    #  Get the answer list.
    answer_list = solve_result.get_answer_list()
    assert len(answer_list) == len(ce)

    #  Process left items.
    for idx in range(0, ce.get_left_item_count()):
        item = ce.get_left_item(idx)
        item.set_coefficient(answer_list[idx])
        ce.set_left_item(idx, item)

    #  Process right items.
    for idx in range(0, ce.get_right_item_count()):
        item = ce.get_right_item(idx)
        item.set_coefficient(answer_list[ce.get_left_item_count() + idx])
        ce.set_right_item(idx, item)

    #  Remove items with coefficient 0.
    ce.remove_items_with_coefficient_zero()

    #  Move items that have negative coefficient to another side.
    ce.move_items_with_negative_coefficient_to_another_side()

    #  Integerize the coefficients.
    ce.coefficients_integerize()