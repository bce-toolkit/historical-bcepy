#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.base.stack as _adt_stack
import bce.parser.common.error as _pe
import bce.parser.mexp.operator as _mexp_operators
import bce.parser.mexp.token as _mexp_tok
import bce.parser.mexp.error as _mexp_errors
import bce.parser.mexp.function as _mexp_fns
import bce.locale.msg_id as _msg_id
import bce.option as _opt


class _RPNProcessor:
    """RPN processor for the MEXP parser."""

    def __init__(self):
        """Initialize the processor with empty operator stack and RPN token list."""

        self.__op_stack = _adt_stack.Stack()
        self.__rpn = []

    def clear(self):
        """Clear the operator stack and RPN token list."""

        self.__op_stack = _adt_stack.Stack()
        self.__rpn = []

    def add_operand(self, operand_token):
        """Process an operand token.

        :type operand_token: _mexp_tok.Token
        :param operand_token: The operand token.
        """

        self.__rpn.append(operand_token)

    def add_operator(self, operator_token):
        """Process an operator token.

        :type operator_token: _mexp_tok.Token
        :param operator_token: The operator token.
        """

        #  Get the operator of the token.
        op1 = _mexp_operators.OPERATORS[operator_token.get_subtype()]

        while True:
            if len(self.__op_stack) == 0:
                break

            #  Stop popping if the top item of the stack isn't an operator.
            top_op = self.__op_stack.top()
            if not top_op.is_operator():
                break

            #  Get the operator on the top of the stack.
            op2 = _mexp_operators.OPERATORS[top_op.get_subtype()]

            if (op1.is_left_associative() and op1.get_precedence() <= op2.get_precedence()) or \
                    (op1.is_right_associative() and op1.get_precedence() < op2.get_precedence()):
                self.__rpn.append(top_op)
                self.__op_stack.pop()
            else:
                break

        #  Push current token to the operator stack.
        self.__op_stack.push(operator_token)

    def add_function(self, function_token):
        """Process a function token.

        :type function_token: _mexp_tok.Token
        :param function_token: The function token.
        """

        self.__op_stack.push(function_token)

    def add_separator(self):
        """Process a separator token."""

        while True:
            top_op = self.__op_stack.top()
            if top_op.is_left_parenthesis():
                break
            self.__rpn.append(top_op)
            self.__op_stack.pop()

    def add_left_parenthesis(self, parenthesis_token):
        """Process a left parenthesis.

        :type parenthesis_token: _mexp_tok.Token
        :param parenthesis_token:
        """

        self.__op_stack.push(parenthesis_token)

    def add_right_parenthesis(self):
        """Process a right parenthesis."""

        while True:
            #  Get the top item of the stack.
            top_op = self.__op_stack.top()

            #  Stop popping if the top item of the stack is not a left parenthesis.
            if top_op.is_left_parenthesis():
                break

            #  Pop the token off from the stack and push it onto the RPN token list.
            self.__rpn.append(top_op)
            self.__op_stack.pop()

        #  Pop the left parenthesis off from the stack.
        self.__op_stack.pop()

        if len(self.__op_stack) != 0 and self.__op_stack.top().is_function():
            self.__rpn.append(self.__op_stack.pop())

    def finalize(self):
        """Pop all items off from the stack and push them to the RPN token list."""

        while len(self.__op_stack) != 0:
            self.__rpn.append(self.__op_stack.pop())

    def direct_add_token_to_rpn(self, token):
        """Add a token to the RPN token list directly.

        :type token: _mexp_tok.Token
        :param token: The token.
        """

        self.__rpn.append(token)

    def direct_push_item_onto_stack(self, item):
        """Push an item onto the stack directly.

        :type item: _mexp_tok.Token
        :param item: The item.
        """

        self.__op_stack.push(item)

    def direct_pop_item_from_stack(self):
        """Pop an item off from the stack and return it directly.

        :rtype : _mexp_tok.Token
        :return: The item.
        """

        return self.__op_stack.pop()

    def get_stack_item_count(self):
        """Get the item count of the stack.

        :rtype : int
        :return: The item count.
        """

        return len(self.__op_stack)

    def get_stack_top_item(self):
        """Get the top item of the stack.

        :rtype : _mexp_tok.Token
        :return: The item.
        """

        return self.__op_stack.top()

    def get_rpn(self):
        """Get the RPN token list.

        :rtype : list
        :return: The list.
        """

        return self.__rpn


class _ParenthesisStackItem:
    """Parenthesis state class for MEXP parser."""

    def __init__(self, symbol, token_id, is_in_fn, cur_argc, req_argc, prev_sep_pos):
        """Initialize the item.

        :type symbol: str
        :type token_id: int
        :type is_in_fn: bool
        :type cur_argc: int
        :type req_argc: int
        :type prev_sep_pos: int
        :param symbol: The symbol of the left parenthesis.
        :param token_id: The token ID.
        :param is_in_fn: Whether it's in function state now.
        :param cur_argc: Current argument count.
        :param req_argc: Required argument count.
        :param prev_sep_pos: Previous separator position.
        """

        self.__sym = symbol
        self.__token_id = token_id
        self.__is_in_fn = is_in_fn
        self.__cur_argc = cur_argc
        self.__req_argc = req_argc
        self.__prev_sep_pos = prev_sep_pos

    def get_symbol(self):
        """Get the symbol of the left parenthesis.

        :rtype : str
        :return: The symbol.
        """

        return self.__sym

    def is_in_function(self):
        """Get whether it's in function state.

        :rtype : bool
        :return: Whether it's in function state.
        """

        return self.__is_in_fn

    def get_current_argument_count(self):
        """Get current argument count.

        :rtype : int
        :return: The count.
        """

        return self.__cur_argc

    def get_required_argument_count(self):
        """Get required argument count.

        :rtype : int
        :return: The count.
        """

        return self.__req_argc

    def get_previous_separator_position(self):
        """Get the position of previous separator.

        :rtype : int
        :return: The position.
        """

        return self.__prev_sep_pos

    def get_token_id(self):
        """Get the token ID.

        :rtype : int
        :return: The token ID.
        """

        return self.__token_id


def _check_left_operand(expression, token_list, token_id, options):
    """Check the left operand.

    :type expression: str
    :type token_list: list
    :type token_id: int
    :type options: _opt.Option
    :param expression: (The same as the variable in parse_to_rpn() routine.)
    :param token_list: (The same as the variable in parse_to_rpn() routine.)
    :param token_id: (The same as the variable in parse_to_rpn() routine.)
    :param options: (The same as the variable in parse_to_rpn() routine.)
    :raise _pe.Error: When there's no left operand.
    """

    raise_err = False

    if token_id == 0:
        raise_err = True
    else:
        prev_tok = token_list[token_id - 1]
        if (not prev_tok.is_right_parenthesis()) and not prev_tok.is_operand():
            raise_err = True

    if raise_err:
        err_pos = token_list[token_id].get_position()
        err = _pe.Error(_mexp_errors.PE_MEXP_MISSING_OPERAND,
                        _msg_id.MSG_PE_MEXP_MISSING_OPERAND_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              err_pos,
                              err_pos,
                              _msg_id.MSG_PE_MEXP_MISSING_OPERAND_LEFT)

        raise err


def _check_right_operand(expression, token_list, token_id, options):
    """Check the right operand.

    :type expression: str
    :type token_list: list
    :type token_id: int
    :type options: _opt.Option
    :param expression: (The same as the variable in parse_to_rpn() routine.)
    :param token_list: (The same as the variable in parse_to_rpn() routine.)
    :param token_id: (The same as the variable in parse_to_rpn() routine.)
    :param options: (The same as the variable in parse_to_rpn() routine.)
    :raise _pe.Error: When there's no right operand.
    """

    raise_err = False

    if token_id + 1 == len(token_list):
        raise_err = True
    else:
        next_tok = token_list[token_id + 1]
        if (not next_tok.is_left_parenthesis()) and not next_tok.is_operand():
            raise_err = True

    if raise_err:
        err_pos = token_list[token_id].get_position()

        err = _pe.Error(_mexp_errors.PE_MEXP_MISSING_OPERAND,
                        _msg_id.MSG_PE_MEXP_MISSING_OPERAND_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              err_pos,
                              err_pos,
                              _msg_id.MSG_PE_MEXP_MISSING_OPERAND_RIGHT)

        raise err


def parse_to_rpn(expression, token_list, options):
    """Parse an infix math expression to RPN.

    :type expression: str
    :type token_list: list
    :type options: _opt.Option
    :param expression: The infix math expression.
    :param token_list: The tokenized infix math expression.
    :param options: BCE options.
    :rtype : list
    :return: The RPN token list.
    :raise _pe.Error: When a parser error occurred.
    """

    #  Initialize
    token_id = 0
    token_cnt = len(token_list)
    rpn = _RPNProcessor()
    cur_argc = 0
    req_argc = 0
    prev_sep_pos = -1
    p_match_map = {")": "(", "]": "[", "}": "{"}
    p_stack = _adt_stack.Stack()
    p_fn = False

    while token_id < token_cnt:
        #  Get current token.
        token = token_list[token_id]

        #  Get previous token.
        if token_id != 0:
            prev_tok = token_list[token_id - 1]
        else:
            prev_tok = None

        if token.is_operand():
            if not (prev_tok is None):
                if prev_tok.is_right_parenthesis():
                    if token.is_symbol_operand():
                        #  Do completion:
                        #    ([expr])[unknown] => ([expr])*[unknown]
                        #
                        #  For example:
                        #    (3-y)x => (3-y)*x
                        rpn.add_operator(_mexp_tok.create_multiply_operator_token())
                    else:
                        #  Numeric parenthesis suffix was not supported.
                        #
                        #  For example:
                        #    (x-y)3
                        #         ^
                        #         Requires a '*' before this token.
                        err = _pe.Error(_mexp_errors.PE_MEXP_MISSING_OPERATOR,
                                        _msg_id.MSG_PE_MEXP_MISSING_OPERATOR_DESCRIPTION,
                                        options)

                        err.push_traceback_ex(expression,
                                              token.get_position(),
                                              token.get_position() + len(token.get_symbol()) - 1,
                                              _msg_id.MSG_PE_MEXP_MISSING_OPERATOR_MUL_BEFORE)

                        raise err

                if prev_tok.is_operand():
                    #  Do completion:
                    #    [number][symbol] => [number]*[symbol]
                    #
                    #  For example:
                    #    4x => 4*x
                    rpn.add_operator(_mexp_tok.create_multiply_operator_token())

            #  Process the token.
            rpn.add_operand(token)

            #  Go to next token.
            token_id += 1

            continue
        elif token.is_function():
            #  Raise an error if the function is unsupported.
            if not token.get_symbol() in _mexp_fns.SUPPORTED:
                err = _pe.Error(_mexp_errors.PE_MEXP_FN_UNSUPPORTED,
                                _msg_id.MSG_PE_MEXP_FN_UNSUPPORTED_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position() + len(token.get_symbol()) - 1,
                                      _msg_id.MSG_PE_MEXP_FN_UNSUPPORTED_TB_MESSAGE,
                                      {"$1": token.get_symbol()})

                raise err

            if (not (prev_tok is None)) and (prev_tok.is_operand() or prev_tok.is_right_parenthesis()):
                #  Do completion:
                #    [num][fn] => [num]*[fn]
                #
                #  For example:
                #    4pow(2,3) => 4*pow(2,3)
                rpn.add_operator(_mexp_tok.create_multiply_operator_token())

            #  Process the token.
            rpn.add_function(token)

            #  Go to next token.
            token_id += 1

            continue
        elif token.is_operator():
            #  Get the operator.
            op = _mexp_operators.OPERATORS[token.get_subtype()]

            #  Check operands.
            if op.is_required_left_operand():
                _check_left_operand(expression, token_list, token_id, options)

            if op.is_required_right_operand():
                _check_right_operand(expression, token_list, token_id, options)

            #  Process the token.
            rpn.add_operator(token)

            #  Go to next token.
            token_id += 1

            continue
        elif token.is_left_parenthesis():
            #  Save state.
            p_stack.push(_ParenthesisStackItem(token.get_symbol(),
                                               token_id,
                                               p_fn,
                                               cur_argc,
                                               req_argc,
                                               prev_sep_pos))

            cur_argc = 0
            prev_sep_pos = token_id

            #  Set function state and get required argument count.
            if (not (prev_tok is None)) and prev_tok.is_function():
                p_fn = True
                req_argc = _mexp_fns.ARGUMENT_COUNT[prev_tok.get_symbol()]
            else:
                p_fn = False
                req_argc = 0

            if (not (prev_tok is None)) and (prev_tok.is_right_parenthesis() or prev_tok.is_operand()):
                #  Do completion
                #    [lp][expr][rp][lp][expr][rp] => [lp][expr][rp]*[lp][expr][rp]
                #
                #  For example:
                #    (2+3)(4+2) => (2+3)*(4+2)
                rpn.add_operator(_mexp_tok.create_multiply_operator_token())

            #  Process the token.
            rpn.add_left_parenthesis(token)

            #  Go to next token.
            token_id += 1

            continue
        elif token.is_right_parenthesis():
            #  Raise an error if there's no content between two separators.
            if prev_sep_pos + 1 == token_id:
                err = _pe.Error(_mexp_errors.PE_MEXP_NO_CONTENT,
                                _msg_id.MSG_PE_MEXP_NO_CONTENT_DESCRIPTION,
                                options)

                if prev_tok.is_left_parenthesis():
                    err.push_traceback_ex(expression,
                                          prev_tok.get_position(),
                                          token.get_position(),
                                          _msg_id.MSG_PE_MEXP_NO_CONTENT_PARENTHESIS)
                else:
                    err.push_traceback_ex(expression,
                                          prev_tok.get_position(),
                                          token.get_position(),
                                          _msg_id.MSG_PE_MEXP_NO_CONTENT_ARGUMENT)

                raise err

            #  Raise an error if there's no left parenthesis to be matched with.
            if len(p_stack) == 0:
                err = _pe.Error(_mexp_errors.PE_MEXP_PARENTHESIS_MISMATCH,
                                _msg_id.MSG_PE_MEXP_PARENTHESIS_MISMATCH_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position(),
                                      _msg_id.MSG_PE_MEXP_PARENTHESIS_MISMATCH_MISSING_LEFT)

                raise err

            #  Get the top item of the stack.
            p_item = p_stack.pop()

            #  Get the symbol of the parenthesis matches with current token.
            p_matched_sym = p_match_map[token.get_symbol()]

            #  Raise an error if the parenthesis was mismatched.
            if p_matched_sym != p_item.get_symbol():
                err = _pe.Error(_mexp_errors.PE_MEXP_PARENTHESIS_MISMATCH,
                                _msg_id.MSG_PE_MEXP_PARENTHESIS_MISMATCH_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position(),
                                      _msg_id.MSG_PE_MEXP_PARENTHESIS_MISMATCH_INCORRECT,
                                      {"$1": p_matched_sym})

                raise err

            if p_fn:
                cur_argc += 1

                #  Raise an error if the argument count was not matched.
                if cur_argc != req_argc:
                    fn_token = token_list[p_item.get_token_id() - 1]

                    err = _pe.Error(_mexp_errors.PE_MEXP_FN_ARGC_MISMATCH,
                                    _msg_id.MSG_PE_MEXP_FN_ARGC_MISMATCH_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(expression,
                                          fn_token.get_position(),
                                          fn_token.get_position() + len(fn_token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_MEXP_FN_ARGC_MISMATCH_TB_MESSAGE,
                                          {"$1": str(req_argc), "$2": str(cur_argc)})

                    raise err

            #  Restore state.
            p_fn = p_item.is_in_function()
            cur_argc = p_item.get_current_argument_count()
            req_argc = p_item.get_required_argument_count()
            prev_sep_pos = p_item.get_previous_separator_position()

            #  Process the token.
            rpn.add_right_parenthesis()

            #  Go to next token.
            token_id += 1

            continue
        elif token.is_separator():
            #  Raise an error if we're not in function now.
            if not p_fn:
                err = _pe.Error(_mexp_errors.PE_MEXP_ILLEGAL_ARG_SEPARATOR,
                                _msg_id.MSG_PE_MEXP_ILLEGAL_ARG_SEPARATOR_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position(),
                                      _msg_id.MSG_PE_MEXP_ILLEGAL_ARG_SEPARATOR_TB_MESSAGE)

                raise err

            #  Raise an error if there's no content between two separators.
            if prev_sep_pos + 1 == token_id:
                err = _pe.Error(_mexp_errors.PE_MEXP_NO_CONTENT,
                                _msg_id.MSG_PE_MEXP_NO_CONTENT_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      prev_tok.get_position(),
                                      token.get_position(),
                                      _msg_id.MSG_PE_MEXP_NO_CONTENT_ARGUMENT)

                raise err

            #  Save separator position.
            prev_sep_pos = token_id

            #  Increase argument counter.
            cur_argc += 1

            #  Process the token.
            rpn.add_separator()

            #  Go to next token.
            token_id += 1

            continue
        else:
            raise RuntimeError("Never reach this condition.")

    #  Raise an error if there are still some left parentheses in the stack.
    if len(p_stack) != 0:
        err = _pe.Error(_mexp_errors.PE_MEXP_PARENTHESIS_MISMATCH,
                        _msg_id.MSG_PE_MEXP_PARENTHESIS_MISMATCH_DESCRIPTION,
                        options)

        while len(p_stack) != 0:
            p_item = p_stack.pop()
            p_token = token_list[p_item.get_token_id()]
            err.push_traceback_ex(expression,
                                  p_token.get_position(),
                                  p_token.get_position(),
                                  _msg_id.MSG_PE_MEXP_PARENTHESIS_MISMATCH_MISSING_RIGHT)

        raise err

    #  Pop all items off from the stack and push them onto the RPN token list.
    rpn.finalize()

    #  Return the RPN token list.
    return rpn.get_rpn()