#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.math.constant as _math_const
import bce.parser.common.error as _pe
import bce.parser.electronic.error as _el_errors
import bce.parser.mexp.utils as _mexp_utils
import bce.locale.msg_id as _msg_id

#  Import this for PyCharm auto type-hinting.
import bce.option as _opt


def parse(expression, token_list, options):
    """Parse electronic descriptor.

    :type expression: str
    :type token_list: list
    :type options: _opt.Option
    :param expression: The expression.
    :param token_list: The token list.
    :param options: The BCE options.
    :return: The electronic charge number.
    :raise _pe.Error: Raise this if we meet a syntax error.
    """

    #  Currently, BCE only supports following two forms:
    #    1) [e+/e-]
    #    2) [coefficient(MEXP/integer)][e+/e-]
    #
    #  Raise an error if the token count isn't one or two.
    if len(token_list) != 2 and len(token_list) != 1:
        err = _pe.Error(_el_errors.PE_EP_UNRECOGNIZED_FORM,
                        _msg_id.MSG_PE_EL_UNRECOGNIZED_FORM_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              0, len(expression) - 1,
                              _msg_id.MSG_PE_EL_UNRECOGNIZED_FORM_TB_MESSAGE)

        raise err

    if len(token_list) == 1:
        e_token = token_list[0]

        #  Raise an error if the first token isn't an electronic property(EP).
        if not e_token.is_electronic_property():
            err = _pe.Error(_el_errors.PE_EP_ILLEGAL_TOKEN,
                            _msg_id.MSG_PE_EL_ILLEGAL_TOKEN_DESCRIPTION,
                            options)

            err.push_traceback_ex(expression,
                                  e_token.get_position(),
                                  e_token.get_position() + len(e_token.get_symbol()) - 1,
                                  _msg_id.MSG_PE_EL_ILLEGAL_TOKEN_REQ_EL_PROPERTY)

            raise err

        if e_token.is_positive_electronic():
            return _math_const.ONE
        else:
            return -_math_const.ONE
    else:
        e_token = token_list[1]
        co_token = token_list[0]

        #  Raise an error if the first token isn't a math value.
        if not co_token.is_operand():
            err = _pe.Error(_el_errors.PE_EP_ILLEGAL_TOKEN,
                            _msg_id.MSG_PE_EL_ILLEGAL_TOKEN_DESCRIPTION,
                            options)

            err.push_traceback_ex(expression,
                                  co_token.get_position(),
                                  co_token.get_position() + len(co_token.get_symbol()) - 1,
                                  _msg_id.MSG_PE_EL_ILLEGAL_TOKEN_REQ_MATH_VALUE)

            raise err

        #  Raise an error if the second token isn't an EP.
        if not e_token.is_electronic_property():
            err = _pe.Error(_el_errors.PE_EP_ILLEGAL_TOKEN,
                            _msg_id.MSG_PE_EL_ILLEGAL_TOKEN_DESCRIPTION,
                            options)

            err.push_traceback_ex(expression,
                                  e_token.get_position(),
                                  e_token.get_position() + len(e_token.get_symbol()) - 1,
                                  _msg_id.MSG_PE_EL_ILLEGAL_TOKEN_REQ_EL_PROPERTY)

            raise err
        if co_token.is_integer_operand():
            coeff = _mexp_utils.convert_int_string_to_rational(co_token.get_symbol())
        else:
            coeff = co_token.get_evaluated_mexp()

        #  Raise an error if the coefficient equals to one.
        #
        #  For example:
        #    {1}e+
        #    ^^^
        #    This token is useless.
        #
        #  Corrected edition:
        #    e+
        if coeff == _math_const.ONE:
            err = _pe.Error(_el_errors.PE_EP_ILLEGAL_COEFFICIENT,
                            _msg_id.MSG_PE_EL_ILLEGAL_COEFFICIENT_DESCRIPTION,
                            options)

            err.push_traceback_ex(expression,
                                  co_token.get_position(),
                                  co_token.get_position() + len(co_token.get_symbol()) - 1,
                                  _msg_id.MSG_PE_EL_ILLEGAL_COEFFICIENT_EQ_ONE)

            raise err

        #  Raise an error if the coefficient is zero or negative.
        if coeff.is_zero or coeff.is_negative:
            err = _pe.Error(_el_errors.PE_EP_ILLEGAL_COEFFICIENT,
                            _msg_id.MSG_PE_EL_ILLEGAL_COEFFICIENT_DESCRIPTION,
                            options)

            err.push_traceback_ex(expression,
                                  co_token.get_position(),
                                  co_token.get_position() + len(co_token.get_symbol()) - 1,
                                  _msg_id.MSG_PE_EL_ILLEGAL_COEFFICIENT_NEG_OR_ZERO)

            raise err

        if e_token.is_positive_electronic():
            return coeff
        else:
            return -coeff