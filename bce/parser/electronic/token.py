#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.base.stack as _adt_stack
import bce.parser.common.token as _base_token
import bce.parser.common.error as _pe
import bce.parser.electronic.error as _ep_errors
import bce.parser.mexp.evaluate as _mexp_ev
import bce.locale.msg_id as _msg_id

#  Import this for PyCharm auto type-hinting.
import bce.option as _opt

#  Token types.
TOKEN_TYPE_OPERAND = 1
TOKEN_TYPE_ELECTRONIC_PROPERTY = 2

#  Token sub-types.
TOKEN_SUBTYPE_INTEGER = 1
TOKEN_SUBTYPE_MEXP = 2
TOKEN_SUBTYPE_POSITIVE_ELECTRONIC = 1
TOKEN_SUBTYPE_NEGATIVE_ELECTRONIC = 2


class Token(_base_token.BaseToken):
    """Token class for electronic."""

    def __init__(self, symbol, token_type, token_subtype=None, idx=-1, pos=-1):
        """Initialize the class.

        :type symbol: str
        :type token_type: int
        :type token_subtype: int
        :type idx: int
        :type pos: int
        :param symbol: The symbol.
        :param token_type: The token type (one of TOKEN_TYPE_*).
        :param token_subtype: The token sub-type (one of TOKEN_SUBTYPE_*).
        :param idx: The index.
        :param pos: The starting position of the token.
        """

        self.__extra_pos = pos
        self.__ev_mexp = None
        _base_token.BaseToken.__init__(self, symbol, token_type, token_subtype, idx)

    def get_position(self):
        """Get the starting position of the token.

        :rtype : int
        :return: The position.
        """

        return self.__extra_pos

    def is_operand(self):
        """Get whether the token is a math value token.

        :rtype : bool
        :return: Return True if the token is a math value token.
        """

        return self.get_type() == TOKEN_TYPE_OPERAND

    def is_integer_operand(self):
        """Get whether the token is an integer token.

        :rtype : bool
        :return: Return True if the token is an integer value token.
        """

        if not self.is_operand():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_INTEGER

    def is_mexp_operand(self):
        """Get whether the token is a MEXP token.

        :rtype : bool
        :return: Return True if the token is a MEXP token.
        """

        if not self.is_operand():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_MEXP

    def is_electronic_property(self):
        """Get whether the token is an electronic property token.

        :rtype : bool
        :return: Return True if the token is an electronic property token.
        """

        return self.get_type() == TOKEN_TYPE_ELECTRONIC_PROPERTY

    def is_positive_electronic(self):
        """Get whether the token is a positive electronic token.

        :rtype : bool
        :return: Return True if the token is a positive electronic token.
        """

        if not self.is_electronic_property():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_POSITIVE_ELECTRONIC

    def is_negative_electronic(self):
        """Get whether the token is a negative electronic token.

        :rtype : bool
        :return: Return True if the token is a negative electronic token.
        """

        if not self.is_electronic_property():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_NEGATIVE_ELECTRONIC

    def get_evaluated_mexp(self):
        """Get the evaluated value of the MEXP (only available when the token is a MEXP token).

        :return: The evaluated value.
        """

        return self.__ev_mexp

    def set_evaluated_mexp(self, value):
        """Set the evaluated value of the MEXP (only available when the token is a MEXP token).

        :param value: The evaluated value.
        """

        self.__ev_mexp = value


def create_integer_operand_token(symbol, idx=-1, pos=-1):
    """Create an integer operand token.

    :type symbol: str
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token(symbol, TOKEN_TYPE_OPERAND, TOKEN_SUBTYPE_INTEGER, idx, pos)


def create_mexp_operand_token(symbol, value, idx=-1, pos=-1):
    """Create a MEXP operand token.

    :type symbol: str
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param value: The evaluated value of the MEXP.
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    new_tok = Token(symbol, TOKEN_TYPE_OPERAND, TOKEN_SUBTYPE_MEXP, idx, pos)
    new_tok.set_evaluated_mexp(value)

    return new_tok


def create_positive_electronic_token(idx=-1, pos=-1):
    """Create a positive electronic token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("e+", TOKEN_TYPE_ELECTRONIC_PROPERTY, TOKEN_SUBTYPE_POSITIVE_ELECTRONIC, idx, pos)


def create_negative_electronic_token(idx=-1, pos=-1):
    """Create a negative electronic token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("e-", TOKEN_TYPE_ELECTRONIC_PROPERTY, TOKEN_SUBTYPE_NEGATIVE_ELECTRONIC, idx, pos)


def tokenize(expression, options):
    """Tokenize a electronic expression.

    :type expression: str
    :type options: _opt.Option
    :param expression: The expression.
    :param options: The BCE options.
    :rtype : list
    :return: The tokenized electronic expression.
    :raise _pe.Error: Raise this if we meet a syntax error.
    """

    #  Initialize.
    end_pos = len(expression)
    cur_pos = 0
    r = []
    p_pos_stack = _adt_stack.Stack()

    while cur_pos < end_pos:
        cur_ch = expression[cur_pos]

        if cur_ch == "e":
            next_pos = cur_pos + 1
            if next_pos < end_pos:
                next_ch = expression[next_pos]

                if next_ch == "+":
                    #  Create a positive electronic token.
                    r.append(create_positive_electronic_token(len(r), cur_pos))

                    #  Go to next position.
                    cur_pos += 2

                    continue

                if next_ch == "-":
                    #  Create a negative electronic token.
                    r.append(create_negative_electronic_token(len(r), cur_pos))

                    #  Go to next position.
                    cur_pos += 2

                    continue

        if cur_ch.isdigit():
            #  Initialize.
            search_pos = cur_pos + 1
            search_end = end_pos

            #  Search next non-digit character.
            while search_pos < end_pos:
                if not expression[search_pos].isdigit():
                    search_end = search_pos
                    break

                #  Go to next searching position.
                search_pos += 1

            #  Create an integer token.
            r.append(create_integer_operand_token(expression[cur_pos:search_end], len(r), cur_pos))

            #  Go to next position.
            cur_pos = search_end

            continue

        if cur_ch == "{":
            #  Initialize.
            search_pos = cur_pos
            search_end = -1

            #  Search the end '}'.
            while search_pos < end_pos:
                search_ch = expression[search_pos]

                if search_ch == "(" or search_ch == "[" or search_ch == "{":
                    #  Push the left parenthesis onto the stack.
                    p_pos_stack.push(search_pos)
                elif search_ch == ")" or search_ch == "]" or search_ch == "}":
                    #  Pop a left-parenthesis off from the stack.
                    p_pos_stack.pop()

                    if len(p_pos_stack) == 0:
                        #  Raise an error if the end parenthesis isn't '}'.
                        if search_ch != "}":
                            err = _pe.Error(_ep_errors.PE_EP_PARENTHESIS_MISMATCH,
                                            _msg_id.MSG_PE_EL_SUB_MEXP_PARENTHESIS_MISMATCH_DESCRIPTION,
                                            options)
                            err.push_traceback_ex(expression,
                                                  search_pos,
                                                  search_pos,
                                                  _msg_id.MSG_PE_EL_SUB_MEXP_PARENTHESIS_MISMATCH_INCORRECT,
                                                  {"$1": "}"})

                            raise err

                        #  Set end position.
                        search_end = search_pos + 1

                        break
                else:
                    pass

                #  Go to next searching position.
                search_pos += 1

            #  Raise an error if we can't find the end '}'.
            if search_end == -1:
                err = _pe.Error(_ep_errors.PE_EP_PARENTHESIS_MISMATCH,
                                _msg_id.MSG_PE_EL_SUB_MEXP_PARENTHESIS_MISMATCH_DESCRIPTION,
                                options)

                while len(p_pos_stack) != 0:
                    prev_p_pos = p_pos_stack.pop()
                    err.push_traceback_ex(expression,
                                          prev_p_pos,
                                          prev_p_pos,
                                          _msg_id.MSG_PE_EL_SUB_MEXP_PARENTHESIS_MISMATCH_MISSING_RIGHT)

                raise err

            #  Raise an error if there's no content between two parentheses.
            if cur_pos + 2 == search_end:
                err = _pe.Error(_ep_errors.PE_EP_NO_CONTENT,
                                _msg_id.MSG_PE_EL_SUB_MEXP_NO_CONTENT_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      cur_pos,
                                      cur_pos + 1,
                                      _msg_id.MSG_PE_EL_SUB_MEXP_NO_CONTENT_TB_MESSAGE)

                raise err

            #  Get the math expression.
            mexp_expr = expression[cur_pos:search_end]

            #  Evaluate the math expression.
            try:
                ev_value = _mexp_ev.evaluate_math_expression(mexp_expr, options)
            except _pe.Error as err:
                err.push_traceback_ex(expression,
                                      cur_pos + 1,
                                      search_end - 2,
                                      _msg_id.MSG_PE_EL_SUB_MEXP_ERROR_TRACE_MESSAGE)

                raise err

            #  Create a MEXP token.
            r.append(create_mexp_operand_token(mexp_expr, ev_value, len(r), cur_pos))

            #  Go to next position.
            cur_pos = search_end

            continue

        #  Raise an error if we meet an unknown token.
        err = _pe.Error(_ep_errors.PE_EP_UNRECOGNIZED_TOKEN,
                        _msg_id.MSG_PE_EL_UNRECOGNIZED_TOKEN_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              cur_pos,
                              cur_pos,
                              _msg_id.MSG_PE_EL_UNRECOGNIZED_TOKEN_TB_MESSAGE)

        raise err

    return r