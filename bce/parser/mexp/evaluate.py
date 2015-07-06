#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.mexp.token as _mexp_token
import bce.parser.mexp.parser as _mexp_parser
import bce.parser.mexp.rpn as _mexp_rpn
import bce.option as _opt


def evaluate_math_expression(expr, options):
    """Parse and evaluate a math expression.

    :type expr: str
    :type options: _opt.Option
    :param expr: The expression.
    :param options: The BCE options.
    :return: The evaluation result.
    """

    #  Tokenize
    token_list = _mexp_token.tokenize(expr, options)

    #  Convert the token list to RPN token list.
    rpn_token_list = _mexp_parser.parse_to_rpn(expr, token_list, options)

    #  Evaluate the RPN token list and return the calculated value.
    return _mexp_rpn.calculate_rpn(token_list, rpn_token_list, options)