#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.common.error as _pe
import bce.math.constant as _math_cst
import bce.parser.molecule.token as _ml_token
import bce.parser.molecule.ast.generator as _ml_ast_generator
import bce.parser.molecule.ast.parser as _ml_ast_parser
import bce.parser.ce.token as _ce_token
import bce.parser.ce.base as _ce_base
import bce.parser.ce.operator as _ce_op
import bce.locale.msg_id as _msg_id
import bce.option as _opt
import bce.parser.ce.error as _ce_error

#  States of the state machine.
_STATE_ROUTE_1 = 1
_STATE_READ_MINUS_1 = 2
_STATE_READ_MOLECULE = 3
_STATE_ROUTE_2 = 4
_STATE_READ_PLUS = 5
_STATE_READ_MINUS_2 = 6
_STATE_READ_SEPARATOR = 7
_STATE_READ_EQUAL_SIGN = 8

#  Chemical equation forms.
_FORM_NORMAL = 1
_FORM_AUTO_CORRECTION = 2


def _macro_register_form(expression, origin_form, new_form, options):
    if origin_form is not None and origin_form != new_form:
        err = _pe.Error(_ce_error.PE_CE_MIXED_FORM,
                        _msg_id.MSG_PE_CE_MIXED_FORM_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              0,
                              len(expression) - 1,
                              _msg_id.MSG_PE_CE_MIXED_FORM_TB_MESSAGE)

        raise err

    return new_form


def parse(expression, token_list, options):
    """Parse the tokenized chemical equation.

    :type expression: str
    :type token_list: list[_ce_token.Token]
    :type options: _opt.Option
    :param expression: Origin chemical equation.
    :param token_list: The tokenized chemical equation.
    :param options: The BCE options.
    :rtype : _ce_base.ChemicalEquation
    :return: The parsed chemical equation.
    """

    #  Initialize an empty chemical equation.
    ret = _ce_base.ChemicalEquation()

    #  Initialize the sign.
    operator = _ce_op.OPERATOR_PLUS

    #  Initialize the form container.
    form = None

    #  Initialize the side mark.
    #  (side == False: Left side; side == True: Right side;)
    side = False

    #  Initialize the state.
    state = _STATE_ROUTE_1

    #  Initialize other variables.
    read_molecule_end = None
    equal_sign_position = -1

    #  Initialize the token cursor.
    cursor = 0
    while True:
        token = token_list[cursor]

        if state == _STATE_ROUTE_1:
            #  Reset the operator to '+'.
            operator = _ce_op.OPERATOR_PLUS

            #  Redirect by rules.
            if token.is_operator_minus():
                #  Go to read the '-'.
                state = _STATE_READ_MINUS_1
            else:
                #  Go and try to read a molecule.
                read_molecule_end = _STATE_ROUTE_2
                state = _STATE_READ_MOLECULE
        elif state == _STATE_READ_MINUS_1:
            #  Register the new form.
            form = _macro_register_form(expression, form, _FORM_NORMAL, options)

            #  Set the operator to '-'.
            operator = _ce_op.OPERATOR_MINUS

            #  Next token.
            cursor += 1

            #  Go to read-molecule state.
            read_molecule_end = _STATE_ROUTE_2
            state = _STATE_READ_MOLECULE
        elif state == _STATE_READ_MOLECULE:
            if not token.is_molecule():
                if token.is_end():
                    if cursor == 0:
                        #  In this condition, we got an empty expression. Raise an error.
                        err = _pe.Error(_ce_error.PE_CE_EMPTY_EXPRESSION,
                                        _msg_id.MSG_PE_CE_EMPTY_EXPRESSION_DESCRIPTION,
                                        options)

                        raise err
                    else:
                        #  There is no content between the end token and previous token. Raise an error.
                        err = _pe.Error(_ce_error.PE_CE_NO_CONTENT,
                                        _msg_id.MSG_PE_CE_NO_CONTENT_DESCRIPTION,
                                        options)

                        err.push_traceback_ex(expression,
                                              token.get_position() - 1,
                                              token.get_position() - 1,
                                              _msg_id.MSG_PE_CE_NO_CONTENT_OPERATOR_AFTER)

                        raise err
                else:
                    err = _pe.Error(_ce_error.PE_CE_NO_CONTENT,
                                    _msg_id.MSG_PE_CE_NO_CONTENT_DESCRIPTION,
                                    options)
                    if cursor == 0:
                        #  There is no content before this token. Raise an error.
                        err.push_traceback_ex(expression,
                                              token.get_position(),
                                              token.get_position(),
                                              _msg_id.MSG_PE_CE_NO_CONTENT_OPERATOR_BEFORE)
                    else:
                        #  There is no content between this token and previous token. Raise an error.
                        err.push_traceback_ex(expression,
                                              token.get_position() - 1,
                                              token.get_position(),
                                              _msg_id.MSG_PE_CE_NO_CONTENT_OPERATOR_BETWEEN)

                    raise err

            try:
                #  Tokenize the molecule.
                ml_token_list = _ml_token.tokenize(token.get_symbol(), options)
                #  Generate the AST.
                ml_ast_root = _ml_ast_generator.generate_ast(token.get_symbol(), ml_token_list, options)

                #  Separate the coefficient from the AST.
                ml_coeff = ml_ast_root.get_prefix_number()
                ml_ast_root.set_prefix_number(_math_cst.ONE)
                ml_atoms_dict = _ml_ast_parser.parse_ast(token.get_symbol(), ml_ast_root, options)

                #  Add the molecule to the chemical equation.
                if side:
                    ret.append_right_item(operator, ml_coeff, ml_ast_root, ml_atoms_dict)
                else:
                    ret.append_left_item(operator, ml_coeff, ml_ast_root, ml_atoms_dict)
            except _pe.Error as err:
                #  Add error description.
                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position() + len(token.get_symbol()) - 1,
                                      _msg_id.MSG_PE_CE_SUB_ML_ERROR_TRACE_MESSAGE)

                raise err

            #  Next token.
            cursor += 1

            #  Redirect by pre-saved state.
            state = read_molecule_end
        elif state == _STATE_ROUTE_2:
            #  Redirect by rules.
            if token.is_operator_plus():
                state = _STATE_READ_PLUS
            elif token.is_operator_minus():
                state = _STATE_READ_MINUS_2
            elif token.is_operator_separator():
                state = _STATE_READ_SEPARATOR
            elif token.is_equal():
                state = _STATE_READ_EQUAL_SIGN
            elif token.is_end():
                break
            else:
                raise RuntimeError("BUG: Unexpected token (should never happen).")
        elif state == _STATE_READ_PLUS:
            #  Register the new form.
            form = _macro_register_form(expression, form, _FORM_NORMAL, options)

            #  Set the operator to '+'.
            operator = _ce_op.OPERATOR_PLUS

            #  Next token.
            cursor += 1

            #  Go to read-molecule state.
            read_molecule_end = _STATE_ROUTE_2
            state = _STATE_READ_MOLECULE
        elif state == _STATE_READ_MINUS_2:
            #  Register the new form.
            form = _macro_register_form(expression, form, _FORM_NORMAL, options)

            #  Set the operator to '-'.
            operator = _ce_op.OPERATOR_MINUS

            #  Next token.
            cursor += 1

            #  Go to read-molecule state.
            read_molecule_end = _STATE_ROUTE_2
            state = _STATE_READ_MOLECULE
        elif state == _STATE_READ_SEPARATOR:
            #  Register the new form.
            form = _macro_register_form(expression, form, _FORM_AUTO_CORRECTION, options)

            #  Set the operator to '+'.
            operator = _ce_op.OPERATOR_PLUS

            #  Next token.
            cursor += 1

            #  Go to read-molecule state.
            read_molecule_end = _STATE_ROUTE_2
            state = _STATE_READ_MOLECULE
        elif state == _STATE_READ_EQUAL_SIGN:
            #  Register the new form.
            form = _macro_register_form(expression, form, _FORM_NORMAL, options)

            #  Next token.
            cursor += 1

            #  Raise an error if the equal sign is duplicated.
            if side:
                err = _pe.Error(_ce_error.PE_CE_DUPLICATED_EQUAL_SIGN,
                                _msg_id.MSG_PE_CE_DUPLICATED_EQUAL_SIGN_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position(),
                                      _msg_id.MSG_PE_CE_DUPLICATED_EQUAL_SIGN_DUPLICATED)

                err.push_traceback_ex(expression,
                                      equal_sign_position,
                                      equal_sign_position,
                                      _msg_id.MSG_PE_CE_DUPLICATED_EQUAL_SIGN_PREVIOUS)

                raise err

            #  Save the position of the equal sign.
            equal_sign_position = token.get_position()

            #  Mark the side flag.
            side = True

            #  Go to route 1.
            state = _STATE_ROUTE_1
        else:
            raise RuntimeError("BUG: Unexpected state.")

    #  Raise an error if there is only 1 molecule.
    if len(ret) == 1:
        err = _pe.Error(_ce_error.PE_CE_ONLY_ONE_MOLECULE,
                        _msg_id.MSG_PE_CE_ONLY_ONE_MOLECULE_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              0,
                              len(expression) - 1,
                              _msg_id.MSG_PE_CE_ONLY_ONE_MOLECULE_TB_MESSAGE)

        raise err

    #  Check form.
    if form is None:
        raise RuntimeError("BUG: Form was not set.")

    #  Raise an error if there is no equal sign (for normal form only).
    if form == _FORM_NORMAL and not side:
        err = _pe.Error(_ce_error.PE_CE_NO_EQUAL_SIGN,
                        _msg_id.MSG_PE_CE_NO_EQUAL_SIGN_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              0,
                              len(expression) - 1,
                              _msg_id.MSG_PE_CE_NO_EQUAL_SIGN_TB_MESSAGE)

        raise err

    return ret
