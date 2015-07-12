#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.locale.msg_id as _msg_id
import bce.logic.balancer.modeling as _bce_model
import bce.logic.balancer.merge as _bce_merge
import bce.logic.common.error as _le
import bce.logic.balancer.error as _bce_error
import bce.math.equation as _math_equ
import bce.parser.ce.base as _ce_base
import bce.option as _opt
import copy as _copy


def balance_chemical_equation(ce, options):
    """Balance a chemical equation.

    :type ce: _ce_base.ChemicalEquation
    :type options: _opt.Option
    :param ce: The chemical equation (represented by ChemicalEquation class).
    :param options: The BCE options.
    """

    #  Get whether the chemical equation is in auto-correction form.
    is_auto_correction_form = (ce.get_right_item_count() == 0)

    #  Build a matrix and backup.
    equations = _bce_model.build_matrix(ce)
    equations_backup = _copy.deepcopy(equations)

    #  Solve the equation and check the answer.
    solved = _math_equ.solve_equation(equations, options.get_protected_math_symbol_header())
    if not _math_equ.check_solved_answer(equations_backup, solved):
        raise _le.LogicError(_bce_error.LE_BCE_CONFLICT_EQUATIONS,
                             _msg_id.MSG_LE_BCE_CONFLICTED_EQUATIONS,
                             options)

    #  Post solving.
    solved = _bce_model.matrix_post_solving(solved, options)

    #  Merge.
    _bce_merge.merge_solving_result_into_ce(ce, solved)

    #  All-eliminated check.
    if len(ce) == 0:
        raise _le.LogicError(_bce_error.LE_BCE_SIDE_ELIMINATED,
                             _msg_id.MSG_LE_BCE_SIDE_ELIMINATED_ALL,
                             options)

    #  'Auto-correction form with multiple answer' check.
    if is_auto_correction_form and (ce.get_left_item_count() == 0 or ce.get_right_item_count() == 0):
        raise _le.LogicError(_bce_error.LE_BCE_AUTO_ARRANGE_WITH_MULTIPLE_ANSWER,
                             _msg_id.MSG_LE_BCE_AUTO_ARRANGE_WITH_MULTI_ANSWER,
                             options)

    #  Left side eliminated check.
    if ce.get_left_item_count() == 0:
        raise _le.LogicError(_bce_error.LE_BCE_SIDE_ELIMINATED,
                             _msg_id.MSG_LE_BCE_SIDE_ELIMINATED_LEFT,
                             options)

    #  Right side eliminated check.
    if ce.get_right_item_count() == 0:
        raise _le.LogicError(_bce_error.LE_BCE_SIDE_ELIMINATED,
                             _msg_id.MSG_LE_BCE_SIDE_ELIMINATED_RIGHT,
                             options)
