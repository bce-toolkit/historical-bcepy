#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.ce.token as _ce_token
import bce.parser.ce.parser as _ce_parser
import bce.logic.modeling as _model
import bce.math.constant as _math_cst
import bce.math.equation as _math_equ

#  Add this for PyCharm auto-hinting.
import bce.option as _opt


def check_whether_balanced(expression, options):
    """Check whether a chemical equation is balanced.

    :type expression: str
    :type options: _opt.Option
    :param expression: The chemical equation.
    :param options: The BCE options.
    :rtype : bool
    :return: Return True if it's balanced.
    """

    #  Parse.
    parsed_ce = _ce_parser.parse(expression, _ce_token.tokenize(expression, options), False, options)

    #  Build matrix.
    mtx = _model.build_matrix(parsed_ce)

    #  Generate the solution of the matrix from the expression.
    pfx_list = []
    for i in range(0, len(parsed_ce.get_left_items()) + len(parsed_ce.get_right_items())):
        pfx_list.append(_math_cst.ONE)

    #  Check whether the solution matches with the matrix.
    return _math_equ.check_solved_answer(mtx, _math_equ.SolvedEquation(pfx_list, 0))


def check_input_expression_characters(expression):
    """Check whether characters of an expression are all valid.

    :type expression: str
    :rtype : bool
    :param expression: The expression.
    :return: Return True if all characters are valid.
    """

    #  Construct valid characters.
    valid_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz()[]{}+-*/^<>;.,="

    #  Check all characters.
    for ch in expression:
        if valid_char.find(ch) == -1:
            return False

    return True