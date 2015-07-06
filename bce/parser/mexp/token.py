#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.common.token as _base_token
import bce.parser.common.error as _pe
import bce.parser.mexp.operator as _mexp_operators
import bce.parser.mexp.error as _mexp_errors
import bce.locale.msg_id as _msg_id
import bce.option as _opt

#  Token types.
TOKEN_TYPE_OPERAND = 1
TOKEN_TYPE_OPERATOR = 2
TOKEN_TYPE_PARENTHESIS = 3
TOKEN_TYPE_FUNCTION = 4
TOKEN_TYPE_SEPARATOR = 5

#  Token sub-types.
TOKEN_SUBTYPE_OPERAND_FLOAT = 1
TOKEN_SUBTYPE_OPERAND_INTEGER = 2
TOKEN_SUBTYPE_OPERAND_SYMBOL = 3
TOKEN_SUBTYPE_PARENTHESIS_LEFT = 1
TOKEN_SUBTYPE_PARENTHESIS_RIGHT = 2


class Token(_base_token.BaseToken):
    """Token class for math expression."""

    def __init__(self, symbol, token_type, token_subtype=None, idx=-1, pos=-1):
        """Initialize the class.

        :type symbol: str
        :type token_type: int
        :type idx: int
        :type pos: int
        :param symbol: The symbol.
        :param token_type: The token type (one of TOKEN_TYPE_*).
        :param token_subtype: The token sub-type (one of TOKEN_SUBTYPE_*).
        :param idx: The index.
        :param pos: The starting position of the token.
        """

        self.__extra_pos = pos
        _base_token.BaseToken.__init__(self, symbol, token_type, token_subtype, idx)

    def get_position(self):
        """Get the starting position of the token.

        :rtype : int
        :return: The position.
        """

        return self.__extra_pos

    def is_operand(self):
        """Get whether the token is an operand token.

        :rtype : bool
        :return: Return True if the token is an operand token.
        """

        return self.get_type() == TOKEN_TYPE_OPERAND

    def is_float_operand(self):
        """Get whether the token is a float operand token.

        :rtype : bool
        :return: Return True if the token is a float operand token.
        """

        if not self.is_operand():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_OPERAND_FLOAT

    def is_integer_operand(self):
        """Get whether the token is an integer operand token.

        :rtype : bool
        :return: Return True if the token is an integer operand token.
        """

        if not self.is_operand():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_OPERAND_INTEGER

    def is_symbol_operand(self):
        """Get whether the token is a symbol operand token.

        :rtype : bool
        :return: Return True if the token is a symbol operand token.
        """

        if not self.is_operand():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_OPERAND_SYMBOL

    def is_operator(self):
        """Get whether the token is an operator token.

        :rtype : bool
        :return: Return True if the token is an operator token.
        """

        return self.get_type() == TOKEN_TYPE_OPERATOR

    def is_plus_operator(self):
        """Get whether the token is a plus operator token.

        :rtype : bool
        :return: Return True if the token is a plus operator token.
        """

        if not self.is_operator():
            return False

        return self.get_subtype() == _mexp_operators.OPERATOR_PLUS_ID

    def is_minus_operator(self):
        """Get whether the token is a minus operator token.

        :rtype : bool
        :return: Return True if the token is a minus operator token.
        """

        if not self.is_operator():
            return False

        return self.get_subtype() == _mexp_operators.OPERATOR_MINUS_ID

    def is_multiply_operator(self):
        """Get whether the token is a multiply operator token.

        :rtype : bool
        :return: Return True if the token is a multiply operator token.
        """

        if not self.is_operator():
            return False

        return self.get_subtype() == _mexp_operators.OPERATOR_MULTIPLY_ID

    def is_divide_operator(self):
        """Get whether the token is a divide operator token.

        :rtype : bool
        :return: Return True if the token is a divide operator token.
        """

        if not self.is_operator():
            return False

        return self.get_subtype() == _mexp_operators.OPERATOR_DIVIDE_ID

    def is_pow_operator(self):
        """Get whether the token is a pow operator token.

        :rtype : bool
        :return: Return True if the token is a pow operator token.
        """

        if not self.is_operator():
            return False

        return self.get_subtype() == _mexp_operators.OPERATOR_POW_ID

    def is_negative_operator(self):
        """Get whether the token is a negative operator token.

        :rtype : bool
        :return: Return True if the token is a negative operator token.
        """

        if not self.is_operator():
            return False

        return self.get_subtype() == _mexp_operators.OPERATOR_NEGATIVE_ID

    def is_parenthesis(self):
        """Get whether the token is a parenthesis token.

        :rtype : bool
        :return: Return True if the token is a parenthesis token.
        """

        return self.get_type() == TOKEN_TYPE_PARENTHESIS

    def is_left_parenthesis(self):
        """Get whether the token is a left parenthesis token.

        :rtype : bool
        :return: Return True if the token is a left parenthesis token.
        """

        if not self.is_parenthesis():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_PARENTHESIS_LEFT

    def is_right_parenthesis(self):
        """Get whether the token is a right parenthesis token.

        :rtype : bool
        :return: Return True if the token is a right parenthesis token.
        """

        if not self.is_parenthesis():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_PARENTHESIS_RIGHT

    def is_function(self):
        """Get whether the token is a function token.

        :rtype : bool
        :return: Return True if the token is a function token.
        """

        return self.get_type() == TOKEN_TYPE_FUNCTION

    def is_separator(self):
        """Get whether the token is a separator token.

        :rtype : bool
        :return: Return True if the token is a separator token.
        """

        return self.get_type() == TOKEN_TYPE_SEPARATOR


def create_float_operand_token(symbol, idx=-1, pos=-1):
    """Create a float operand token.

    :type symbol: str
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token(symbol, TOKEN_TYPE_OPERAND, TOKEN_SUBTYPE_OPERAND_FLOAT, idx, pos)


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

    return Token(symbol, TOKEN_TYPE_OPERAND, TOKEN_SUBTYPE_OPERAND_INTEGER, idx, pos)


def create_symbol_operand_token(symbol, idx=-1, pos=-1):
    """Create a symbol operand token.

    :type symbol: str
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token(symbol, TOKEN_TYPE_OPERAND, TOKEN_SUBTYPE_OPERAND_SYMBOL, idx, pos)


def create_plus_operator_token(idx=-1, pos=-1):
    """Create a plus operator token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("+", TOKEN_TYPE_OPERATOR, _mexp_operators.OPERATOR_PLUS_ID, idx, pos)


def create_minus_operator_token(idx=-1, pos=-1):
    """Create a minus operator token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("-", TOKEN_TYPE_OPERATOR, _mexp_operators.OPERATOR_MINUS_ID, idx, pos)


def create_multiply_operator_token(idx=-1, pos=-1):
    """Create a multiply operator token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("*", TOKEN_TYPE_OPERATOR, _mexp_operators.OPERATOR_MULTIPLY_ID, idx, pos)


def create_divide_operator_token(idx=-1, pos=-1):
    """Create a divide operator token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("/", TOKEN_TYPE_OPERATOR, _mexp_operators.OPERATOR_DIVIDE_ID, idx, pos)


def create_pow_operator_token(idx=-1, pos=-1):
    """Create a pow operator token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("^", TOKEN_TYPE_OPERATOR, _mexp_operators.OPERATOR_POW_ID, idx, pos)


def create_negative_operator_token(idx=-1, pos=-1):
    """Create a negative operator token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("-", TOKEN_TYPE_OPERATOR, _mexp_operators.OPERATOR_NEGATIVE_ID, idx, pos)


def create_left_parenthesis_token(symbol, idx=-1, pos=-1):
    """Create a left parenthesis token.

    :type symbol: str
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token(symbol, TOKEN_TYPE_PARENTHESIS, TOKEN_SUBTYPE_PARENTHESIS_LEFT, idx, pos)


def create_right_parenthesis_token(symbol, idx=-1, pos=-1):
    """Create a right parenthesis token.

    :type symbol: str
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token(symbol, TOKEN_TYPE_PARENTHESIS, TOKEN_SUBTYPE_PARENTHESIS_RIGHT, idx, pos)


def create_function_token(symbol, idx=-1, pos=-1):
    """Create a function token.

    :type symbol: str
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token(symbol, TOKEN_TYPE_FUNCTION, None, idx, pos)


def create_separator_token(idx=-1, pos=-1):
    """Create a separator token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token(",", TOKEN_TYPE_SEPARATOR, None, idx, pos)


def tokenize(expression, options):
    """Tokenize a math expression.

    :type expression: str
    :type options: _opt.Option
    :param expression: The math expression.
    :param options: The BCE options.
    :rtype : list
    :return: The tokenized math expression.
    :raise _pe.Error: If we meet a syntax error.
    """

    #  Initialize.
    r = []
    cur_pos = 0
    end_pos = len(expression)
    prev_tok = None

    while cur_pos < end_pos:
        cur_ch = expression[cur_pos]

        #  Get previous token if possible.
        if len(r) != 0:
            prev_tok = r[-1]

        #  Read a number token if current character is a digit.
        if cur_ch.isdigit():
            #  Search for next non-digit and non-dot character.
            met_dot = False
            prev_dot_pos = -1
            search_pos = cur_pos + 1
            search_end = end_pos

            while search_pos < end_pos:
                search_ch = expression[search_pos]
                if search_ch == ".":
                    #  If we met decimal dot more than once, raise an duplicated-dot error.
                    if met_dot:
                        err = _pe.Error(_mexp_errors.PE_MEXP_DUPLICATED_DECIMAL_DOT,
                                        _msg_id.MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_DESCRIPTION,
                                        options)

                        err.push_traceback_ex(expression,
                                              search_pos,
                                              search_pos,
                                              _msg_id.MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_DUPLICATED)

                        err.push_traceback_ex(expression,
                                              prev_dot_pos,
                                              prev_dot_pos,
                                              _msg_id.MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_PREVIOUS)

                        raise err
                    else:
                        met_dot = True
                        prev_dot_pos = search_pos
                else:
                    if not search_ch.isdigit():
                        search_end = search_pos
                        break

                #  Go to next searching position.
                search_pos += 1

            if met_dot:
                #  Create a float token if there's a decimal dot in the sequence.
                r.append(create_float_operand_token(expression[cur_pos:search_end], len(r), cur_pos))
            else:
                #  Create a integer token if there's no decimal dot in the sequence.
                r.append(create_integer_operand_token(expression[cur_pos:search_end], len(r), cur_pos))

            #  Go to next position.
            cur_pos = search_end

            continue

        if cur_ch.isalpha():
            #  Search for next non-alphabet character.
            search_pos = cur_pos + 1
            search_end = end_pos

            while search_pos < end_pos:
                if not expression[search_pos].isalpha():
                    search_end = search_pos
                    break

                #  Go to next searching position.
                search_pos += 1

            if search_end == end_pos:
                symbol_hdr = options.get_protected_math_symbol_header()

                #  Raise an error if the symbol starts with the protected symbol header.
                if expression.startswith(symbol_hdr, cur_pos, search_end):
                    err = _pe.Error(_mexp_errors.PE_MEXP_USE_PROTECTED_SYMBOL_HEADER,
                                    _msg_id.MSG_PE_MEXP_USE_PROTECTED_SYMBOL_HEADER_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(expression,
                                          cur_pos,
                                          search_end - 1,
                                          _msg_id.MSG_PE_MEXP_USE_PROTECTED_SYMBOL_HEADER_TB_MESSAGE,
                                          {"$1": symbol_hdr})

                    raise err

                #  Create a symbol token if there's nothing behind the string we got.
                r.append(create_symbol_operand_token(expression[cur_pos:search_end], len(r), cur_pos))
            else:
                next_ch = expression[search_end]
                if next_ch.isdigit() or next_ch == "(" or next_ch == "[" or next_ch == "{":
                    #  Create a function token if there's a number or a parenthesis behind the string we got.
                    r.append(create_function_token(expression[cur_pos:search_end], len(r), cur_pos))
                else:
                    symbol_hdr = options.get_protected_math_symbol_header()

                    #  Raise an error if the symbol starts with the protected symbol header.
                    if expression.startswith(symbol_hdr, cur_pos, search_end):
                        err = _pe.Error(_mexp_errors.PE_MEXP_USE_PROTECTED_SYMBOL_HEADER,
                                        _msg_id.MSG_PE_MEXP_USE_PROTECTED_SYMBOL_HEADER_DESCRIPTION,
                                        options)

                        err.push_traceback_ex(expression,
                                              cur_pos,
                                              search_end - 1,
                                              _msg_id.MSG_PE_MEXP_USE_PROTECTED_SYMBOL_HEADER_TB_MESSAGE,
                                              {"$1": symbol_hdr})

                        raise err

                    #  Create a symbol token.
                    r.append(create_symbol_operand_token(expression[cur_pos:search_end], len(r), cur_pos))

            #  Go to next position.
            cur_pos = search_end

            continue

        if cur_ch == "+":
            #  Create a token.
            r.append(create_plus_operator_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 1

            continue

        if cur_ch == "-":
            #  If the left operand exists, create a minus operator token. Otherwise, create a negative sign token.
            if (not (prev_tok is None)) and \
                    (prev_tok.is_operand() or prev_tok.is_right_parenthesis()):
                r.append(create_minus_operator_token(len(r), cur_pos))
            else:
                r.append(create_negative_operator_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 1

            continue

        if cur_ch == "*":
            #  Create a token.
            r.append(create_multiply_operator_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 1

            continue

        if cur_ch == "/":
            #  Create a token.
            r.append(create_divide_operator_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 1

            continue

        if cur_ch == "^":
            #  Create a token.
            r.append(create_pow_operator_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 1

            continue

        if cur_ch == "(" or cur_ch == "[" or cur_ch == "{":
            r.append(create_left_parenthesis_token(cur_ch, len(r), cur_pos))
            cur_pos += 1
            continue

        if cur_ch == ")" or cur_ch == "]" or cur_ch == "}":
            #  Create a  token.
            r.append(create_right_parenthesis_token(cur_ch, len(r), cur_pos))

            #  Go to next position.
            cur_pos += 1

            continue

        if cur_ch == ",":
            #  Create a token.
            r.append(create_separator_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 1

            continue

        #  Raise an untokenizable error.
        err = _pe.Error(_mexp_errors.PE_MEXP_UNRECOGNIZED_TOKEN,
                        _msg_id.MSG_PE_MEXP_UNRECOGNIZED_TOKEN_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              cur_pos,
                              cur_pos,
                              _msg_id.MSG_PE_MEXP_UNRECOGNIZED_TOKEN_TB_MESSAGE)

        raise err

    return r