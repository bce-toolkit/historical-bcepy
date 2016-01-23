#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.base.stack as _adt_stack
import bce.parser.common.token as _base_token
import bce.parser.common.error as _pe
import bce.parser.mexp.error as _mexp_errors
import bce.parser.mexp.function as _mexp_fns
import bce.parser.mexp.token as _mexp_token
import bce.utils.sympy_utils as _mexp_utils
import bce.locale.msg_id as _msg_id
import bce.option as _opt
import sympy as _sympy


def calculate_rpn(origin_token_list, rpn_token_list, options):
    """Calculate the value of a RPN token list.

    :type origin_token_list: list of _mexp_token.Token
    :type rpn_token_list: list of _mexp_token.Token
    :type options: _opt.Option
    :param origin_token_list: The origin token list.
    :param rpn_token_list: The RPN token list.
    :return: The calculated value.
    :raise RuntimeError: When a bug appears.
    """

    #  This routine implements the postfix algorithm.

    #  Initialize the operand stack.
    calc_stack = _adt_stack.Stack()

    for token in rpn_token_list:
        if token.is_integer_operand():
            #  Convert the symbol to integer and push it onto the stack.
            calc_stack.push(_mexp_utils.convert_int_string_to_rational(token.get_symbol()))
        elif token.is_float_operand():
            #  Convert the symbol to float and push it onto the stack.
            calc_stack.push(_mexp_utils.convert_float_string_to_rational(token.get_symbol()))
        elif token.is_symbol_operand():
            #  Create a math symbol and push it onto the stack.
            calc_stack.push(_sympy.Symbol(token.get_symbol()))
        elif token.is_plus_operator():
            #  Get two operands.
            num2 = calc_stack.pop()
            num1 = calc_stack.pop()

            #  Do plus and push the result onto the stack.
            calc_stack.push(num1 + num2)
        elif token.is_minus_operator():
            #  Get two operands.
            num2 = calc_stack.pop()
            num1 = calc_stack.pop()

            #  Do minus and push the result onto the stack.
            calc_stack.push(num1 - num2)
        elif token.is_multiply_operator():
            #  Get two operands.
            num2 = calc_stack.pop()
            num1 = calc_stack.pop()

            #  Do multiplication and push the result onto the stack.
            calc_stack.push(num1 * num2)
        elif token.is_divide_operator():
            #  Get two operands.
            num2 = calc_stack.pop()
            num1 = calc_stack.pop()

            #  Raise an error if the rhs equals to zero.
            if num2.is_zero:
                err = _pe.Error(_mexp_errors.PE_MEXP_RPNEV_DIVIDE_ZERO,
                                _msg_id.MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_DESCRIPTION,
                                options)
                err.push_traceback_ex(_base_token.untokenize(origin_token_list),
                                      token.get_position(),
                                      token.get_position(),
                                      _msg_id.MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_OPERATOR)
                raise err

            #  Do division and push the result onto the stack.
            calc_stack.push(num1 / num2)
        elif token.is_pow_operator():
            #  Get two operands.
            num2 = calc_stack.pop()
            num1 = calc_stack.pop()

            #  For a ^ b, when b < 0, a != 0.
            if num2.is_negative and num1.is_zero:
                err = _pe.Error(_mexp_errors.PE_MEXP_RPNEV_DIVIDE_ZERO,
                                _msg_id.MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_DESCRIPTION,
                                options)

                err.push_traceback_ex(_base_token.untokenize(origin_token_list),
                                      token.get_position(),
                                      token.get_position(),
                                      _msg_id.MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_OPERATOR)

                raise err

            #  Do power and push the result onto the stack.
            calc_stack.push(num1 ** num2)
        elif token.is_negative_operator():
            num1 = calc_stack.pop()
            calc_stack.push(-num1)
        elif token.is_function():
            if token.get_symbol() == "pow":
                #  Get two operands.
                num2 = calc_stack.pop()
                num1 = calc_stack.pop()

                #  For pow(a, b), when b < 0, a != 0.
                if num2.is_negative and num1.is_zero:
                    err = _pe.Error(_mexp_errors.PE_MEXP_RPNEV_DIVIDE_ZERO,
                                    _msg_id.MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(_base_token.untokenize(origin_token_list),
                                          token.get_position(),
                                          token.get_position() + len(token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_POW)

                    raise err

                #  Do power and push the result onto the stack.
                calc_stack.push(num1 ** num2)
            elif token.get_symbol() == "sqrt":
                #  Get one operand.
                num1 = calc_stack.pop()

                #  (For a^b, when b < 0, a != 0.
                if num1.is_negative:
                    err = _pe.Error(_mexp_errors.PE_MEXP_RPNEV_SQRT_NEG_ARG,
                                    _msg_id.MSG_PE_MEXP_RPNEV_SQRT_NEG_ARG_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(_base_token.untokenize(origin_token_list),
                                          token.get_position(),
                                          token.get_position() + len(token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_MEXP_RPNEV_SQRT_NEG_ARG_TB_MESSAGE)

                    raise err

                #  Do sqrt and push the result onto the stack.
                calc_stack.push(_mexp_fns.do_sqrt(num1))
            else:
                raise RuntimeError("Unreachable condition (Invalid function name).")
        else:
            raise RuntimeError("Unreachable condition (Invalid token type).")

    #  If there are more than one operands in the stack, raise a runtime error. But generally,
    #  we shouldn't get this error because we have checked the whole expression when tokenizing.
    if len(calc_stack) > 1:
        raise RuntimeError("Unreachable condition (Too many items in the stack after calculation).")

    return calc_stack.top()
