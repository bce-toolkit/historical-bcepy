#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.base.stack as _adt_stack
import bce.parser.common.token as _base_token
import bce.parser.common.error as _pe
import bce.parser.ce.error as _ce_errors
import bce.locale.msg_id as _msg_id

#  Add this for PyCharm auto-hinting.
import bce.option as _opt

#  Token types.
TOKEN_TYPE_OPERATOR = 1
TOKEN_TYPE_EQUAL = 2
TOKEN_TYPE_MOLECULE = 3

#  Token sub-types.
TOKEN_SUBTYPE_OPERATOR_PLUS = 1
TOKEN_SUBTYPE_OPERATOR_MINUS = 2
TOKEN_SUBTYPE_OPERATOR_SEPARATOR = 3

#  Expression forms.
TOKENIZED_CE_FORM_NORMAL = 1
TOKENIZED_CE_FORM_AUTO_SIDING = 2


class Token(_base_token.BaseToken):
    """Token class for chemical equation."""

    def __init__(self, symbol, token_type, token_subtype=None, idx=-1, pos=-1):
        """Initialize the token.

        :type symbol: str
        :type token_type: int
        :type idx: int
        :type pos: int
        :param symbol: The symbol.
        :param token_type: The token type (one of TOKEN_TYPE_*).
        :param token_subtype: The token sub-type (one of TOKEN_SUBTYPE_*).
        :param idx: The index.
        :param pos: The starting position.
        """

        self.__extra_pos = pos
        _base_token.BaseToken.__init__(self, symbol, token_type, token_subtype, idx)

    def get_position(self):
        """Get the starting position of the token.

        :rtype : int
        :return: The starting position.
        """

        return self.__extra_pos

    def is_operator(self):
        """Get whether the token is an operator token.

        :rtype : bool
        :return: Return True if the token is an operator token.
        """

        return self.get_type() == TOKEN_TYPE_OPERATOR

    def is_operator_plus(self):
        """Get whether the token is a plus operator token.

        :rtype : bool
        :return: Return True if the token is a plus operator token.
        """

        if not self.is_operator():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_OPERATOR_PLUS

    def is_operator_minus(self):
        """Get whether the token is a minus operator token.

        :rtype : bool
        :return: Return True if the token is a minus operator token.
        """

        if not self.is_operator():
            return False

        return self.get_subtype() == TOKEN_SUBTYPE_OPERATOR_MINUS

    def is_operator_separator(self):
        """Get whether the token is a separator operator token.

        :rtype : bool
        :return: Return True if the token is a separator operator token.
        """

        if not self.is_operator():
            return False
        return self.get_subtype() == TOKEN_SUBTYPE_OPERATOR_SEPARATOR

    def is_equal(self):
        """Get whether the token is an equal('=') token.

        :rtype : bool
        :return: Return True if the token is an equal token.
        """

        return self.get_type() == TOKEN_TYPE_EQUAL

    def is_molecule(self):
        """Get whether the token is a molecule token.

        :rtype : bool
        :return: Return True if the token is a molecule token.
        """

        return self.get_type() == TOKEN_TYPE_MOLECULE


class TokenizedCE:
    """Class for containing tokenized chemical equation / expression."""

    def __init__(self, token_list, form):
        """Initialize the class with specified token list and form indicator.

        :type token_list: list
        :type form: int
        :param token_list: The token list.
        :param form: The form indicator.
        """

        self.__t = token_list
        self.__f = form

    def get_token_list(self):
        """Get the token list.

        :rtype : list of Token
        :return: The token list.
        """

        return self.__t

    def get_form(self):
        """Get the form of the chemical equation / expression.

        :rtype : int
        :return: The form indicator (oen of TOKENIZED_CE_FORM_*).
        """

        return self.__f


def create_operator_plus_token(idx=-1, pos=-1):
    """Create a plus operator token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :return: The created token.
    """

    return Token("+", TOKEN_TYPE_OPERATOR, TOKEN_SUBTYPE_OPERATOR_PLUS, idx, pos)


def create_operator_minus_token(idx=-1, pos=-1):
    """Create a minus operator token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :return: The created token.
    """

    return Token("-", TOKEN_TYPE_OPERATOR, TOKEN_SUBTYPE_OPERATOR_MINUS, idx, pos)


def create_operator_separator_token(idx=-1, pos=-1):
    """Create a separator operator token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :return: The created token.
    """

    return Token(";", TOKEN_TYPE_OPERATOR, TOKEN_SUBTYPE_OPERATOR_SEPARATOR, idx, pos)


def create_equal_token(idx=-1, pos=-1):
    """Create an equal operator token.

    :type idx: int
    :type pos: int
    :param idx: The index.
    :param pos: The starting position.
    :return: The created token.
    """

    return Token("=", TOKEN_TYPE_EQUAL, None, idx, pos)


def create_molecule_token(symbol, idx=-1, pos=-1):
    """Create a molecule token.

    :type symbol: str
    :type idx: int
    :type pos: int
    :param symbol: The symbol.
    :param idx: The index.
    :param pos: The starting position.
    :return: The created token.
    """

    return Token(symbol, TOKEN_TYPE_MOLECULE, None, idx, pos)


def _raise_no_content_between_operators_exception(expression, last_op_pos, cur_pos, options):
    """Raise a 'No content between operators' exception.

    :type expression: str
    :type last_op_pos: int
    :type cur_pos: int
    :type options: _opt.Option
    :param expression: The expression.
    :param last_op_pos: The last operator position.
    :param cur_pos: Current operator position.
    :param options: The BCE options.
    :raise _pe.Error: Raise the created exception.
    """

    err = _pe.Error(_ce_errors.PE_CE_NO_CONTENT,
                    _msg_id.MSG_PE_CE_NO_CONTENT_DESCRIPTION,
                    options)

    if last_op_pos == -1:
        err.push_traceback_ex(expression,
                              cur_pos,
                              cur_pos,
                              _msg_id.MSG_PE_CE_NO_CONTENT_OPERATOR_BEFORE)
    else:
        err.push_traceback_ex(expression,
                              last_op_pos,
                              cur_pos,
                              _msg_id.MSG_PE_CE_NO_CONTENT_OPERATOR_BETWEEN)

    raise err


def _raise_parenthesis_mismatch_exception(expression, pos, options, is_left):
    """Raise a 'Parenthesis mismatch' exception.

    :type expression: str
    :type pos: int
    :type options: _opt.Option
    :type is_left: bool
    :param expression: The expression.
    :param pos: The position of the parenthesis.
    :param options: The BCE options.
    :param is_left: Whether the mismatched parenthesis is a left parenthesis.
    :raise _pe.Error: Raise the created exception.
    """

    err = _pe.Error(_ce_errors.PE_CE_PARENTHESIS_MISMATCH,
                    _msg_id.MSG_PE_CE_PARENTHESIS_MISMATCH_DESCRIPTION,
                    options)

    if is_left:
        err.push_traceback_ex(expression,
                              pos,
                              pos,
                              _msg_id.MSG_PE_CE_PARENTHESIS_MISMATCH_LEFT)
    else:
        err.push_traceback_ex(expression,
                              pos,
                              pos,
                              _msg_id.MSG_PE_CE_PARENTHESIS_MISMATCH_RIGHT)

    raise err


def _raise_mixed_form_exception(expression, options):
    """Raise a 'Mixed form' exception.

    :type expression: str
    :type options: _opt.Option
    :param expression: The expression.
    :param options: The BCE options.
    :raise _pe.Error: Raise the created exception.
    """
    err = _pe.Error(_ce_errors.PE_CE_MIXED_FORM,
                    _msg_id.MSG_PE_CE_MIXED_FORM_DESCRIPTION,
                    options)

    err.push_traceback_ex(expression,
                          0,
                          len(expression) - 1,
                          _msg_id.MSG_PE_CE_MIXED_FORM_TB_MESSAGE)

    raise err


def tokenize(expression, options):
    """Tokenize a chemical equation / expression.

    :type expression: str
    :type options: _opt.Option
    :param expression: Origin chemical equation / expression.
    :param options: The BCE options.
    :rtype : TokenizedCE
    :return: The tokenized chemical equation /expression.
    :raise _pe.Error: When there are any syntax errors in the expression.
    """

    #  Initialize.
    r = []
    form = -1
    cur_pos = 0
    end_pos = len(expression)
    prev_equal_pos = -1
    p_ml_pos_stack = _adt_stack.Stack()
    last_op_pos = -1

    while cur_pos < end_pos:
        cur_ch = expression[cur_pos]
        if cur_ch == "(":
            #  Push the parenthesis onto the stack.
            p_ml_pos_stack.push(cur_pos)

            #  Go to next position.
            cur_pos += 1

            continue

        if cur_ch == ")":
            #  Raise an error if there's no left parenthesis in the stack.
            if len(p_ml_pos_stack) == 0:
                _raise_parenthesis_mismatch_exception(expression, cur_pos, options, True)

            #  Pop off the last left parenthesis from the stack.
            p_ml_pos_stack.pop()

            #  Go to next position.
            cur_pos += 1

            continue

        if cur_ch == "[":
            #  Search the end ']'.
            search_pos = cur_pos + 1
            search_end = -1

            while search_pos < end_pos:
                if expression[search_pos] == "]":
                    search_end = search_pos + 1
                    break

                #  Go to next searching position.
                search_pos += 1

            #  Raise an error if we can't find the end ']'.
            if search_end == -1:
                _raise_parenthesis_mismatch_exception(expression, cur_pos, cur_pos, False)

            #  Go to next position.
            cur_pos = search_end

            continue

        #  Raise an error if we meet a ']' in the main loop, because we should have
        #  processed it when processing '['.
        if cur_ch == "]":
            _raise_parenthesis_mismatch_exception(expression, cur_pos, options, True)

        if cur_ch == "<":
            #  Search the end '>'.
            search_pos = cur_pos + 1
            search_end = -1

            while search_pos < end_pos:
                if expression[search_pos] == ">":
                    search_end = search_pos + 1
                    break

                #  Go to next searching position.
                search_pos += 1

            #  Raise an error if we can't find the end '>'.
            if search_end == -1:
                _raise_parenthesis_mismatch_exception(expression, cur_pos, options, False)

            #  Go to next position.
            cur_pos = search_end

            continue

        #  Raise an error if we meet a '>' in the main loop, because we should have
        #  processed it when processing '<'.
        if cur_ch == ">":
            _raise_parenthesis_mismatch_exception(expression, cur_pos, options, True)

        if cur_ch == "{":
            #  Simulate a parenthesis stack to find the end '}'.
            p_mexp = 0

            #  Search the end '}'.
            search_pos = cur_pos + 1
            search_end = -1

            while search_pos < end_pos:
                search_ch = expression[search_pos]

                if search_ch == "(" or search_ch == "[" or search_ch == "{":
                    #  If current character is a left parenthesis, push it onto the stack.
                    p_mexp += 1
                elif search_ch == ")" or search_ch == "]" or search_ch == "}":
                    #  When we meet a right parenthesis and there's no left parenthesis in the stack.
                    #  The parenthesis we met should be the end parenthesis matches with current
                    #  parenthesis.
                    #
                    #  NOTE: We don't have to check whether it's '}' or not, we will check it when
                    #        tokenizing the molecule.
                    if p_mexp == 0:
                        search_end = search_pos + 1
                        break

                    #  Raise an error if the parenthesis isn't '}'.
                    p_mexp -= 1
                else:
                    pass

                #  Go to next searching position.
                search_pos += 1

            #  Raise an error if we can't find the end '}'.
            if search_end == -1:
                _raise_parenthesis_mismatch_exception(expression, cur_pos, options, False)

            #  Go to next position.
            cur_pos = search_end

            continue

        #  Raise an error if we meet a '}' in the main loop, because we should have
        #  processed it when processing '{'.
        if cur_ch == "}":
            _raise_parenthesis_mismatch_exception(expression, cur_pos, options, True)

        #  Process '+', '-', '=', ';' outside the molecules.
        if len(p_ml_pos_stack) == 0:
            if cur_ch == "+":
                #  Raise an error if there's no content between this and the previous operator.
                if last_op_pos + 1 == cur_pos:
                    _raise_no_content_between_operators_exception(expression, last_op_pos, cur_pos, options)

                new_form = TOKENIZED_CE_FORM_NORMAL
                if form == -1:
                    #  Register the form of the chemical equation expression.
                    form = new_form
                elif form == new_form:
                    pass
                else:
                    #  Raise an error because the form is different from what we registered before.
                    _raise_mixed_form_exception(expression, options)

                #  Create a molecule token.
                r.append(create_molecule_token(expression[last_op_pos + 1:cur_pos], len(r), last_op_pos + 1))

                #  Create a plus operator token.
                r.append(create_operator_plus_token(len(r), cur_pos))

                #  Set current position as the position of the last operator.
                last_op_pos = cur_pos

                #  Go to next position.
                cur_pos += 1

                continue

            if cur_ch == "-":
                no_molecule_before = False
                if cur_pos == 0:
                    no_molecule_before = True
                else:
                    #  Raise an error if there's no content between this and the previous operator.
                    if last_op_pos + 1 == cur_pos:
                        if expression[last_op_pos] == "=":
                            no_molecule_before = True
                        else:
                            _raise_no_content_between_operators_exception(expression, last_op_pos, cur_pos, options)

                new_form = TOKENIZED_CE_FORM_NORMAL
                if form == -1:
                    #  Register the form of the chemical equation expression.
                    form = new_form
                elif form == new_form:
                    pass
                else:
                    #  Raise an error because the form is different from what we registered before.
                    _raise_mixed_form_exception(expression, options)

                if not no_molecule_before:
                    #  Create a molecule token.
                    r.append(create_molecule_token(expression[last_op_pos + 1:cur_pos], len(r), last_op_pos + 1))

                #  Create a minus operator token.
                r.append(create_operator_minus_token(len(r), cur_pos))

                #  Set current position as the position of the last operator.
                last_op_pos = cur_pos

                #  Go to next position.
                cur_pos += 1

                continue

            if cur_ch == "=":
                #  Raise an error if there's no content between this and the previous operator.
                if last_op_pos + 1 == cur_pos:
                    _raise_no_content_between_operators_exception(expression, last_op_pos, cur_pos, options)

                #  Raise an error if the operator is duplicated.
                if prev_equal_pos != -1:
                    err = _pe.Error(_ce_errors.PE_CE_DUPLICATED_EQUAL_SIGN,
                                    _msg_id.MSG_PE_CE_DUPLICATED_EQUAL_SIGN_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(expression,
                                          cur_pos,
                                          cur_pos,
                                          _msg_id.MSG_PE_CE_DUPLICATED_EQUAL_SIGN_DUPLICATED)

                    err.push_traceback_ex(expression,
                                          prev_equal_pos,
                                          prev_equal_pos,
                                          _msg_id.MSG_PE_CE_DUPLICATED_EQUAL_SIGN_PREVIOUS)

                    raise err
                else:
                    #  Mark current equal operator as the equal operator we have met.
                    prev_equal_pos = cur_pos

                new_form = TOKENIZED_CE_FORM_NORMAL
                if form == -1:
                    #  Register the form of the chemical equation expression.
                    form = new_form
                elif form == new_form:
                    pass
                else:
                    #  Raise an error because the form is different from what we registered before.
                    _raise_mixed_form_exception(expression, options)

                #  Create a molecule token.
                r.append(create_molecule_token(expression[last_op_pos + 1:cur_pos], len(r), last_op_pos + 1))

                #  Create a equal operator token.
                r.append(create_equal_token(len(r), cur_pos))

                #  Set current position as the position of the last operator.
                last_op_pos = cur_pos

                #  Go to next position.
                cur_pos += 1

                continue

            if cur_ch == ";":
                #  Raise an error if there's no content between this and the previous operator.
                if last_op_pos + 1 == cur_pos:
                    _raise_no_content_between_operators_exception(expression, last_op_pos, cur_pos, options)

                new_form = TOKENIZED_CE_FORM_AUTO_SIDING
                if form == -1:
                    #  Register the form of the chemical equation expression.
                    form = new_form
                elif form == new_form:
                    pass
                else:
                    #  Raise an error because the form is different from what we registered before.
                    _raise_mixed_form_exception(expression, options)

                #  Create a molecule token.
                r.append(create_molecule_token(expression[last_op_pos + 1:cur_pos], len(r), last_op_pos + 1))

                #  Create a separator operator token.
                r.append(create_operator_separator_token(len(r), cur_pos))

                #  Set current position as the position of the last operator.
                last_op_pos = cur_pos

                #  Go to next position.
                cur_pos += 1

                continue

        cur_pos += 1

    #  Raise an error if there are still some left parentheses in the stack.
    if len(p_ml_pos_stack) != 0:
        err = _pe.Error(_ce_errors.PE_CE_PARENTHESIS_MISMATCH,
                        _msg_id.MSG_PE_CE_PARENTHESIS_MISMATCH_DESCRIPTION,
                        options)

        while len(p_ml_pos_stack) != 0:
            prev_p_pos = p_ml_pos_stack.pop()
            err.push_traceback_ex(expression,
                                  prev_p_pos,
                                  prev_p_pos,
                                  _msg_id.MSG_PE_CE_PARENTHESIS_MISMATCH_RIGHT)

        raise err

    if form == -1:
        #  Raise an error because there's only one molecule in this chemical expression.
        err = _pe.Error(_ce_errors.PE_CE_ONLY_ONE_MOLECULE,
                        _msg_id.MSG_PE_CE_ONLY_ONE_MOLECULE_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              0,
                              end_pos - 1,
                              _msg_id.MSG_PE_CE_ONLY_ONE_MOLECULE_TB_MESSAGE)

        raise err
    elif form == TOKENIZED_CE_FORM_NORMAL:
        #  Raise an error if there's no equal operator in a normal-form chemical expression(equation).
        if prev_equal_pos == -1:
            err = _pe.Error(_ce_errors.PE_CE_NO_EQUAL_SIGN,
                            _msg_id.MSG_PE_CE_NO_EQUAL_SIGN_DESCRIPTION,
                            options)

            err.push_traceback_ex(expression,
                                  0,
                                  end_pos - 1,
                                  _msg_id.MSG_PE_CE_NO_EQUAL_SIGN_TB_MESSAGE)

            raise err
    else:
        pass

    #  Raise an error if there's no content between this and the previous operator.
    if last_op_pos + 1 == end_pos:
        _raise_no_content_between_operators_exception(expression, last_op_pos, cur_pos, options)

    r.append(create_molecule_token(expression[last_op_pos + 1:], len(r), last_op_pos + 1))

    return TokenizedCE(r, form)