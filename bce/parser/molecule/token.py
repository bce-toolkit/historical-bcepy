#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.common.token as _base_token
import bce.parser.common.error as _pe
import bce.parser.electronic.token as _el_token
import bce.parser.electronic.parser as _el_parser
import bce.parser.mexp.evaluate as _mexp_ev
import bce.parser.molecule.error as _ml_errors
import bce.locale.msg_id as _msg_id

#  Add this for PyCharm auto-hinting.
import bce.option as _opt

#  Token types.
TOKEN_TYPE_SYMBOL = 1
TOKEN_TYPE_OPERAND = 2
TOKEN_TYPE_HYDRATE_DOT = 3
TOKEN_TYPE_PARENTHESIS = 4
TOKEN_TYPE_ABBREVIATION = 5
TOKEN_TYPE_ELECTRONIC = 6
TOKEN_TYPE_STATUS = 7

#  Token sub-types.
TOKEN_SUBTYPE_INTEGER = 1
TOKEN_SUBTYPE_MEXP = 2
TOKEN_SUBTYPE_PARENTHESIS_LEFT = 1
TOKEN_SUBTYPE_PARENTHESIS_RIGHT = 2
TOKEN_SUBTYPE_AQUEOUS = 1
TOKEN_SUBTYPE_GAS = 2
TOKEN_SUBTYPE_LIQUID = 3
TOKEN_SUBTYPE_SOLID = 4


class ElectronicDataContainer:
    """Container for the electronic data."""

    def __init__(self, token_list, count):
        """Initialize the container.

        :type token_list: list
        :param token_list: The token list.
        :param count: The count of electronics.
        """

        self.__token_list = token_list
        self.__cnt = count

    def get_token_list(self):
        """Get the token list.

        :rtype : list
        :return: The token list.
        """

        return self.__token_list

    def get_count(self):
        """Get the electronic count.

        :return: The electronic count.
        """

        return self.__cnt


class Token(_base_token.BaseToken):
    """Token class for molecule."""

    def __init__(self, symbol, token_type, token_subtype=None, idx=-1, pos=-1):
        """Initialize the class.

        :type symbol: str
        :type token_type: int
        :type idx: int
        :type pos: int
        :param symbol: The symbol.
        :param token_type: The token type.
        :param token_subtype: The token sub-type.
        :param idx: The index.
        :param pos: The starting position.
        """

        self.__extra_pos = pos
        self.__extra_ev_mexp = None
        self.__extra_el = None
        _base_token.BaseToken.__init__(self, symbol, token_type, token_subtype, idx)

    def get_position(self):
        """Get the starting position of the token in origin expression.

        :rtype : int
        :return: The position.
        """

        return self.__extra_pos

    def is_symbol(self):
        """Get whether the token is a symbol token.

        :rtype : bool
        :return: Return True if the token is a symbol token.
        """

        return self.get_type() == TOKEN_TYPE_SYMBOL

    def is_operand(self):
        """Get whether the token is an operand token.

        :rtype : bool
        :return: Return True if the token is an operand token.
        """

        return self.get_type() == TOKEN_TYPE_OPERAND

    def is_integer_operand(self):
        """Get whether the token is an integer operand token.

        :rtype : bool
        :return: Return True if the token is an integer operand token.
        """

        if not self.is_operand():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_INTEGER

    def is_mexp_operand(self):
        """Get whether the token is a MEXP operand token.

        :rtype : bool
        :return: Return True if the token is a MEXP operand token.
        """

        if not self.is_operand():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_MEXP

    def is_hydrate_dot(self):
        """Get whether the token is a dot token.

        :rtype : bool
        :return: Return True if the token is a dot token.
        """

        return self.get_type() == TOKEN_TYPE_HYDRATE_DOT

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

    def is_abbreviation(self):
        """Get whether the token is an abbreviation token.

        :rtype : bool
        :return: Return True if the token is an abbreviation token.
        """

        return self.get_type() == TOKEN_TYPE_ABBREVIATION

    def is_electronic(self):
        """Get whether the token is an electronic token.

        :rtype : bool
        :return: Return True if the token is an electronic token.
        """

        return self.get_type() == TOKEN_TYPE_ELECTRONIC

    def set_evaluated_mexp(self, ev_value):
        """Set the evaluated MEXP value of this token.

        :param ev_value: The value.
        """

        self.__extra_ev_mexp = ev_value

    def get_evaluated_mexp(self):
        """Get the evaluated MEXP value of the token.

        :return: The value.
        """

        return self.__extra_ev_mexp

    def set_electronic_data(self, el_data):
        """Set electronic data (only available in electronic token).

        :type el_data: ElectronicDataContainer
        :param el_data: The data.
        """

        self.__extra_el = el_data

    def get_electronic_data(self):
        """Get electronic data (only available in electronic token).

        :rtype : ElectronicDataContainer
        :return: The data.
        """

        return self.__extra_el

    def is_status(self):
        """Get whether the token is a status descriptor.

        :rtype : bool
        :return: Whether the token is a status descriptor.
        """

        return self.get_type() == TOKEN_TYPE_STATUS

    def is_aqueous_status(self):
        """Get whether the token is an aqueous status descriptor.

        :rtype : bool
        :return: Whether the token is an aqueous status descriptor.
        """

        if not self.is_status():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_AQUEOUS

    def is_gas_status(self):
        """Get whether the token is a gas status descriptor.

        :rtype : bool
        :return: Whether the token is a gas status descriptor.
        """

        if not self.is_status():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_GAS

    def is_liquid_status(self):
        """Get whether the token is a liquid status descriptor.

        :rtype : bool
        :return: Whether the token is a liquid status descriptor.
        """

        if not self.is_status():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_LIQUID

    def is_solid_status(self):
        """Get whether the token is a solid status descriptor.

        :rtype : bool
        :return: Whether the token is a solid status descriptor.
        """

        if not self.is_status():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_SOLID

    def set_position(self, new_position):
        """Set the position.

        :param new_position: The new position.
        """

        self.__extra_pos = new_position


def create_symbol_token(symbol, idx=-1, pos=-1):
    """Create an atom symbol token.

    :type symbol: str
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token(symbol, TOKEN_TYPE_SYMBOL, None, idx, pos)


def create_integer_operand_token(symbol, idx=-1, pos=-1):
    """Create an integer token.

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
    """Create a math expression token.

    :type symbol: str
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param value: The evaluated value of the expression.
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    r = Token(symbol, TOKEN_TYPE_OPERAND, TOKEN_SUBTYPE_MEXP, idx, pos)
    r.set_evaluated_mexp(value)

    return r


def create_hydrate_dot_token(idx=-1, pos=-1):
    """Create a dot token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token(".", TOKEN_TYPE_HYDRATE_DOT, None, idx, pos)


def create_left_parenthesis_token(idx=-1, pos=-1):
    """Create a left parenthesis token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("(", TOKEN_TYPE_PARENTHESIS, TOKEN_SUBTYPE_PARENTHESIS_LEFT, idx, pos)


def create_right_parenthesis_token(idx=-1, pos=-1):
    """Create a right parenthesis token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token(")", TOKEN_TYPE_PARENTHESIS, TOKEN_SUBTYPE_PARENTHESIS_RIGHT, idx, pos)


def create_abbreviation_token(symbol, idx=-1, pos=-1):
    """Create an abbreviation token.

    :type symbol: str
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token(symbol, TOKEN_TYPE_ABBREVIATION, None, idx, pos)


def create_electronic_token(symbol, data, idx=-1, pos=-1):
    """Create an electronic token.

    :type symbol: str
    :type data: ElectronicDataContainer
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param data: The parsed data.
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    new_token = Token(symbol, TOKEN_TYPE_ELECTRONIC, None, idx, pos)
    new_token.set_electronic_data(data)

    return new_token


def create_aqueous_status_token(idx=-1, pos=-1):
    """Create an aqueous status descriptor token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("(aq)", TOKEN_TYPE_STATUS, TOKEN_SUBTYPE_AQUEOUS, idx, pos)


def create_gas_status_token(idx=-1, pos=-1):
    """Create a gas status descriptor.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("(g)", TOKEN_TYPE_STATUS, TOKEN_SUBTYPE_GAS, idx, pos)


def create_liquid_status_token(idx=-1, pos=-1):
    """Create a liquid status descriptor token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("(l)", TOKEN_TYPE_STATUS, TOKEN_SUBTYPE_LIQUID, idx, pos)


def create_solid_status_token(idx=-1, pos=-1):
    """Create a solid status descriptor token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :rtype : Token
    :return: The created token.
    """

    return Token("(s)", TOKEN_TYPE_STATUS, TOKEN_SUBTYPE_SOLID, idx, pos)


def tokenize(expression, options):
    """Tokenize a molecule expression.

    :type expression: str
    :type options: _opt.Option
    :param expression: The expression.
    :param options: The BCE options.
    :rtype : list of Token
    :return: The tokenized molecule.
    :raise _pe.Error: When we meet a parser error.
    """

    #  Initialize.
    r = []
    cur_pos = 0
    end_pos = len(expression)

    while cur_pos < end_pos:
        cur_ch = expression[cur_pos]

        #  Read a integer token if current character is a digit.
        if cur_ch.isdigit():
            #  Search for the next non-digit character.
            search_pos = cur_pos + 1
            search_end = end_pos
            lz_last_pos = -1

            if cur_ch == "0":
                chk_ld_zero = True
            else:
                chk_ld_zero = False

            while search_pos < end_pos:
                search_ch = expression[search_pos]

                if not search_ch.isdigit():
                    search_end = search_pos
                    break

                #  Check leading zero.
                if chk_ld_zero:
                    if search_ch != "0":
                        chk_ld_zero = False
                    else:
                        lz_last_pos = search_pos

                #  Go to next searching position.
                search_pos += 1

            #  If the whole number is filled with zero, the last zero isn't leading zero.
            if lz_last_pos + 1 == search_end:
                lz_last_pos -= 1

            #  Raise an error if the number has leading zero.
            if lz_last_pos != -1:
                err = _pe.Error(_ml_errors.PE_ML_EXCESSIVE_LEADING_ZERO,
                                _msg_id.MSG_PE_ML_EXCESSIVE_LEADING_ZERO_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      cur_pos,
                                      lz_last_pos,
                                      _msg_id.MSG_PE_ML_EXCESSIVE_LEADING_ZERO_TB_MESSAGE)

                raise err

            #  Create an integer token.
            r.append(create_integer_operand_token(expression[cur_pos:search_end], len(r), cur_pos))

            #  Go to next position.
            cur_pos = search_end

            continue

        #  Read an atom symbol if current character is a upper-case alphabet.
        if cur_ch.isupper():
            #  Search for next non-lower-case character.
            search_pos = cur_pos + 1
            search_end = end_pos

            while search_pos < end_pos:
                if not expression[search_pos].islower():
                    search_end = search_pos
                    break

                #  Go to next searching position.
                search_pos += 1

            #  Create a symbol token.
            r.append(create_symbol_token(expression[cur_pos:search_end], len(r), cur_pos))

            #  Go to next position.
            cur_pos = search_end

            continue

        #  Read a hydrate-dot token if current character is a dot.
        if cur_ch == ".":
            #  Create a dot token.
            r.append(create_hydrate_dot_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 1

            continue

        if expression.startswith("(g)", cur_pos):
            #  Create a status descriptor token.
            r.append(create_gas_status_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 3

            continue

        if expression.startswith("(l)", cur_pos):
            #  Create a status descriptor token.
            r.append(create_liquid_status_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 3

            continue

        if expression.startswith("(s)", cur_pos):
            #  Create a status descriptor token.
            r.append(create_solid_status_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 3

            continue

        if expression.startswith("(aq)", cur_pos):
            #  Create a status descriptor token.
            r.append(create_aqueous_status_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 4

            continue

        #  Read a normal left parenthesis if current character is '('.
        if cur_ch == "(":
            #  Create a left parenthesis token.
            r.append(create_left_parenthesis_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 1

            continue

        #  Read a normal right parenthesis if current character is ')'.
        if cur_ch == ")":
            #  Create a right parenthesis token.
            r.append(create_right_parenthesis_token(len(r), cur_pos))

            #  Go to next position.
            cur_pos += 1

            continue

        #  Read a abbreviation if current character is '['.
        if cur_ch == "[":
            #  Find the ']'.
            search_end = -1
            search_pos = cur_pos + 1

            while search_pos < end_pos:
                if expression[search_pos] == "]":
                    search_end = search_pos + 1
                    break

                #  Go to next searching position.
                search_pos += 1

            #  Raise an error if we can't find the ']'.
            if search_end == -1:
                err = _pe.Error(_ml_errors.PE_ML_PARENTHESIS_MISMATCH,
                                _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      cur_pos,
                                      cur_pos,
                                      _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_ABBR_RIGHT)

                raise err

            #  Raise an error if there's no content between these two parentheses.
            if cur_pos + 2 == search_end:
                err = _pe.Error(_ml_errors.PE_ML_NO_CONTENT,
                                _msg_id.MSG_PE_ML_NO_CONTENT_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      cur_pos,
                                      cur_pos + 1,
                                      _msg_id.MSG_PE_ML_NO_CONTENT_PARENTHESIS)

                raise err

            #  Create an abbreviation token.
            r.append(create_abbreviation_token(expression[cur_pos:search_end], len(r), cur_pos))

            #  Go to next position.
            cur_pos = search_end

            continue

        #  Read a math expression if current character is '{'.
        if cur_ch == "{":
            #  Simulate a parenthesis stack to find the end '}'.
            p_mexp = 0

            #  Searching the end '}'.
            search_end = -1
            search_pos = cur_pos + 1

            while search_pos < end_pos:
                search_ch = expression[search_pos]

                if search_ch == "(" or search_ch == "[" or search_ch == "{":
                    #  If current character is a left parenthesis, push it onto the stack.
                    p_mexp += 1
                elif search_ch == ")" or search_ch == "]" or search_ch == "}":
                    #  When we meet a right parenthesis and there's no left parenthesis in the stack.
                    #  The parenthesis we met should be the end '}'.
                    if p_mexp == 0:
                        #  Raise an error if the parenthesis isn't '}'.
                        if search_ch != "}":
                            err = _pe.Error(_ml_errors.PE_ML_PARENTHESIS_MISMATCH,
                                            _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                                            options)

                            err.push_traceback_ex(expression,
                                                  search_pos,
                                                  search_pos,
                                                  _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_INCORRECT,
                                                  {"$1": "}"})

                            raise err

                        #  Set the end position.
                        search_end = search_pos + 1

                        break

                    #  Pop the parenthesis off from the stack.
                    p_mexp -= 1
                else:
                    pass

                #  Go to next searching position.
                search_pos += 1

            #  Raise an error if we can't find the end '}'.
            if search_end == -1:
                err = _pe.Error(_ml_errors.PE_ML_PARENTHESIS_MISMATCH,
                                _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      cur_pos,
                                      cur_pos,
                                      _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_MEXP_RIGHT)

                raise err

            #  Raise an error if the math expression has no content.
            if cur_pos + 2 == search_end:
                err = _pe.Error(_ml_errors.PE_ML_NO_CONTENT,
                                _msg_id.MSG_PE_ML_NO_CONTENT_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      cur_pos,
                                      cur_pos + 1,
                                      _msg_id.MSG_PE_ML_NO_CONTENT_MEXP)

                raise err

            #  Get the expression.
            mexp_expr = expression[cur_pos:search_end]

            #  Evaluate the expression.
            try:
                ev_value = _mexp_ev.evaluate_math_expression(mexp_expr, options)
            except _pe.Error as err:
                err.push_traceback_ex(expression,
                                      cur_pos + 1,
                                      search_end - 2,
                                      _msg_id.MSG_PE_ML_SUB_MEXP_ERROR_TRACE_MESSAGE)

                raise err

            #  Create a math expression token.
            r.append(create_mexp_operand_token(mexp_expr, ev_value, len(r), cur_pos))

            #  Go to next position.
            cur_pos = search_end

            continue

        if cur_ch == "<":
            #  Initialize.
            search_pos = cur_pos + 1
            search_end = -1

            #  Searching for the '>'.
            while search_pos < end_pos:
                if expression[search_pos] == ">":
                    search_end = search_pos
                    break

                #  Go to next searching position.
                search_pos += 1

            #  Raise an error if not found.
            if search_end == -1:
                err = _pe.Error(_ml_errors.PE_ML_PARENTHESIS_MISMATCH,
                                _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      cur_pos,
                                      cur_pos,
                                      _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_EL_RIGHT)

                raise err

            #  Raise an error if there's no content between two parentheses.
            if cur_pos + 1 == search_end:
                err = _pe.Error(_ml_errors.PE_ML_NO_CONTENT,
                                _msg_id.MSG_PE_ML_NO_CONTENT_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      cur_pos,
                                      search_end,
                                      _msg_id.MSG_PE_ML_NO_CONTENT_EL)

                raise err

            #  Get the inner electronic expression.
            el_expr = expression[cur_pos + 1:search_end]

            #  Parse the expression.
            try:
                el_tok_list = _el_token.tokenize(el_expr, options)
                el_count = _el_parser.parse(el_expr, el_tok_list, options)
            except _pe.Error as err:
                err.push_traceback_ex(expression,
                                      cur_pos,
                                      search_end,
                                      _msg_id.MSG_PE_ML_SUB_EL_ERROR_TRACE_MESSAGE)

                raise err

            #  Create an electronic token.
            r.append(create_electronic_token(expression[cur_pos:search_end + 1],
                                             ElectronicDataContainer(el_tok_list, el_count),
                                             len(r),
                                             cur_pos))

            #  Go to next position.
            cur_pos = search_end + 1

            continue

        #  Raise an error if current character can't be tokenized.
        err = _pe.Error(_ml_errors.PE_ML_UNRECOGNIZED_TOKEN,
                        _msg_id.MSG_PE_ML_UNRECOGNIZED_TOKEN_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              cur_pos,
                              cur_pos,
                              _msg_id.MSG_PE_ML_UNRECOGNIZED_TOKEN_TB_MESSAGE)

        raise err

    return r