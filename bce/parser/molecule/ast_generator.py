#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.math.constant as _math_cst
import bce.parser.common.error as _pe
import bce.parser.molecule.ast_base as _ast_base
import bce.parser.molecule.ast_utils as _ast_utils
import bce.parser.molecule.error as _ml_error
import bce.parser.molecule.token as _ml_token
import bce.parser.molecule.status as _ml_status
import bce.locale.msg_id as _msg_id

#  Add this for PyCharm auto-hinting.
import bce.option as _opt

#  States.
_ST_RT_ERROR = 0
_ST_ROOT = 1
_ST_ATOM = 2
_ST_PREFIX = 3
_ST_EL_BEGIN = 4
_ST_EL_PREFIX = 5
_ST_EL_POSITIVITY = 6
_ST_EL_END = 7
_ST_SUFFIX_BEGIN = 8
_ST_SUFFIX_EL = 9
_ST_SUFFIX_END = 10
_ST_INNER_EL_BEGIN = 11
_ST_INNER_EL_END = 12
_ST_ABBREVIATION = 13
_ST_LEFT_PARENTHESIS = 14
_ST_RIGHT_PARENTHESIS = 15
_ST_HYDRATE_DOT = 16
_ST_STATUS = 17


def generate_ast_from_token_list(expression, token_list, options):
    """Generate an AST from the token list.

    :type expression: str
    :type token_list: list of _ml_token.Token
    :type options: _opt.Option
    :param expression: The origin expression.
    :param token_list: The token list.
    :param options: The BCE options.
    :rtype : _ast_base._ASTNodeBaseML
    :return: The root node of the created AST tree.
    """

    #  Initialize the token cursor.
    cursor = 0

    #  Create initial AST tree nodes and link them.
    root = _ast_base.ASTNodeHydrateGroup()
    root.register_starting_position_in_source_text(0)
    ptr = _ast_base.ASTNodeMolecule(root)
    ptr.register_starting_position_in_source_text(0)
    root.append_child(ptr)

    #  Initialize the state machine.
    state = _ST_ROOT

    #  Initialize shared variables.
    el_charge = None
    el_fail_state = _ST_RT_ERROR
    el_end_state = _ST_RT_ERROR
    inner_el_starting = -1

    while True:
        #  Read current token.
        token = token_list[cursor]

        if state == _ST_RT_ERROR:
            raise RuntimeError("Never reach this condition.")
        elif state == _ST_ROOT:
            #  Find the first molecule node in current node and parent nodes.
            while not ptr.is_molecule():
                ptr = ptr.get_parent_node()

            #  Jump to specific state by checking current token.
            if token.is_symbol():
                state = _ST_ATOM
            elif token.is_operand() and len(ptr) == 0:
                state = _ST_PREFIX
            elif token.is_electronic_begin():
                state = _ST_INNER_EL_BEGIN
            elif token.is_abbreviation():
                state = _ST_ABBREVIATION
            elif token.is_left_parenthesis():
                state = _ST_LEFT_PARENTHESIS
            elif token.is_right_parenthesis():
                state = _ST_RIGHT_PARENTHESIS
            elif token.is_hydrate_dot():
                state = _ST_HYDRATE_DOT
            elif token.is_status():
                state = _ST_STATUS
            elif token.is_end():
                break
            else:
                #  Raise an error if the token is unexpected.
                err = _pe.Error(_ml_error.PE_ML_UNEXPECTED_TOKEN,
                                _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position() + len(token.get_symbol()) - 1,
                                      _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_DEFAULT)

                raise err
        elif state == _ST_ATOM:
            #  Create a new atom node and link it with the molecule.
            new_node = _ast_base.ASTNodeAtom(token.get_symbol(), ptr)
            new_node.register_starting_position_in_source_text(token.get_position())
            ptr.append_child(new_node)

            #  Set work node pointer to the new created node.
            ptr = new_node

            #  Next token.
            cursor += 1

            #  Jump to read the suffix.
            state = _ST_SUFFIX_BEGIN
        elif state == _ST_PREFIX:
            #  Get the prefix value.
            pfx_val = token.get_operand_value().simplify()

            #  Domain check.
            if pfx_val.is_negative or pfx_val.is_zero:
                err = _pe.Error(_ml_error.PE_ML_DOMAIN_ERROR,
                                _msg_id.MSG_PE_ML_DOMAIN_ERROR_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position() + len(token.get_symbol()) - 1,
                                      _msg_id.MSG_PE_ML_DOMAIN_ERROR_PFX)

                raise err

            #  Raise an error if the prefix is useless.
            if pfx_val == _math_cst.ONE:
                err = _pe.Error(_ml_error.PE_ML_USELESS_OPERAND,
                                _msg_id.MSG_PE_ML_USELESS_OPERAND_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position() + len(token.get_symbol()) - 1,
                                      _msg_id.MSG_PE_ML_USELESS_OPERAND_PFX)

                raise err

            #  Set the prefix number.
            ptr.set_prefix_number(pfx_val * ptr.get_prefix_number())

            #  Next token.
            cursor += 1

            #  Go to root state.
            state = _ST_ROOT
        elif state == _ST_EL_BEGIN:
            #  Try to read a '<'.
            if token.is_electronic_begin():
                #  Next token.
                cursor += 1

                #  Jump to read the prefix number.
                state = _ST_EL_PREFIX
            else:
                #  Jump to fail state.
                state = el_fail_state
        elif state == _ST_EL_PREFIX:
            #  Try to read an operand.
            if token.is_operand():
                #  Get the charge number.
                el_charge = token.get_operand_value().simplify()

                #  Domain check.
                if el_charge.is_negative or el_charge.is_zero:
                    err = _pe.Error(_ml_error.PE_ML_DOMAIN_ERROR,
                                    _msg_id.MSG_PE_ML_DOMAIN_ERROR_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(expression,
                                          token.get_position(),
                                          token.get_position() + len(token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_ML_DOMAIN_ERROR_EL_CHG)

                    raise err

                #  Raise an error if the charge number is useless.
                if el_charge == _math_cst.ONE:
                    err = _pe.Error(_ml_error.PE_ML_USELESS_OPERAND,
                                    _msg_id.MSG_PE_ML_USELESS_OPERAND_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(expression,
                                          token.get_position(),
                                          token.get_position() + len(token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_ML_USELESS_OPERAND_EL)

                    raise err

                #  Next token.
                cursor += 1
            else:
                #  Treat the charge number as 1.
                el_charge = _math_cst.ONE

            #  Jump to read the positivity descriptor.
            state = _ST_EL_POSITIVITY
        elif state == _ST_EL_POSITIVITY:
            if token.is_electronic_positive_flag():
                pass
            elif token.is_electronic_negative_flag():
                el_charge = -el_charge
            else:
                #  Raise an error if there is no positivity descriptor.
                err = _pe.Error(_ml_error.PE_ML_UNEXPECTED_TOKEN,
                                _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION,
                                options)

                if token.is_end():
                    #  Search the '<' token.
                    search_cur = cursor - 1
                    while not token_list[search_cur].is_electronic_begin():
                        search_cur -= 1

                    #  Add the description.
                    err.push_traceback_ex(expression,
                                          token_list[search_cur].get_position(),
                                          token.get_position() - 1,
                                          _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_EL_INCOMPLETE)
                else:
                    err.push_traceback_ex(expression,
                                          token.get_position(),
                                          token.get_position() + len(token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_EL_PN)
                raise err

            #  Next token.
            cursor += 1

            #  Jump to read the '>'.
            state = _ST_EL_END
        elif state == _ST_EL_END:
            if token.is_electronic_end():
                #  Next token.
                cursor += 1
                #  Jump to end state.
                state = el_end_state
            else:
                #  Raise an error if current token is not '>'.
                err = _pe.Error(_ml_error.PE_ML_UNEXPECTED_TOKEN,
                                _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION,
                                options)

                if token.is_end():
                    #  Search the '<' token.
                    search_cur = cursor - 1
                    while not token_list[search_cur].is_electronic_begin():
                        search_cur -= 1

                    #  Add the description.
                    err.push_traceback_ex(expression,
                                          token_list[search_cur].get_position(),
                                          token.get_position() - 1,
                                          _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_EL_INCOMPLETE)
                else:
                    err.push_traceback_ex(expression,
                                          token.get_position(),
                                          token.get_position() + len(token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_EL_ED)

                raise err
        elif state == _ST_SUFFIX_BEGIN:
            #  Set the fail and end state.
            el_fail_state = _ST_SUFFIX_END
            el_end_state = _ST_SUFFIX_EL

            #  Jump to read the electronic descriptor.
            state = _ST_EL_BEGIN
        elif state == _ST_SUFFIX_EL:
            #  Set the electronic charge.
            ptr.set_suffix_electronic(el_charge)
            #  Jump to suffix-end state.
            state = _ST_SUFFIX_END
        elif state == _ST_SUFFIX_END:
            #  Try to read an operand.
            if token.is_operand():
                #  Get the suffix number.
                sfx_val = token.get_operand_value().simplify()

                #  Domain check.
                if sfx_val.is_negative or sfx_val.is_zero:
                    err = _pe.Error(_ml_error.PE_ML_DOMAIN_ERROR,
                                    _msg_id.MSG_PE_ML_DOMAIN_ERROR_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(expression,
                                          token.get_position(),
                                          token.get_position() + len(token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_ML_DOMAIN_ERROR_SFX)

                    raise err

                #  Raise an error if the suffix is useless.
                if sfx_val == _math_cst.ONE:
                    err = _pe.Error(_ml_error.PE_ML_USELESS_OPERAND,
                                    _msg_id.MSG_PE_ML_USELESS_OPERAND_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(expression,
                                          token.get_position(),
                                          token.get_position() + len(token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_ML_USELESS_OPERAND_SFX)

                    raise err

                #  Set the suffix number.
                ptr.set_suffix_number(sfx_val)

                #  Next token.
                cursor += 1

            #  Register the ending position to current working node.
            ptr.register_ending_position_in_source_text(token_list[cursor].get_position() - 1)

            #  Jump to root state.
            state = _ST_ROOT
        elif state == _ST_INNER_EL_BEGIN:
            #  Set the fail and end state.
            el_fail_state = _ST_RT_ERROR
            el_end_state = _ST_INNER_EL_END

            #  Save the starting position.
            inner_el_starting = token.get_position()

            #  Jump to read the electronic descriptor.
            state = _ST_EL_BEGIN
        elif state == _ST_INNER_EL_END:
            #  Create a new electronic node and set its source range.
            new_node = _ast_base.ASTNodeElectronic(el_charge, ptr)
            new_node.register_source_text_range(inner_el_starting, token.get_position() - 1)

            #  Link the new created node with current working node.
            ptr.append_child(new_node)

            #  Jump to root state.
            state = _ST_ROOT
        elif state == _ST_ABBREVIATION:
            #  Create a new abbreviation node and set its starting position and right parenthesis position.
            new_node = _ast_base.ASTNodeAbbreviation(token.get_symbol()[1:-1], ptr)
            new_node.register_starting_position_in_source_text(token.get_position())
            new_node.set_right_parenthesis_position(token.get_position() + len(token.get_symbol()) - 1)

            #  Link the new created node with current working node.
            ptr.append_child(new_node)

            #  Set the working node pointer to the new created node.
            ptr = new_node

            #  Next token.
            cursor += 1

            #  Jump to read the suffix.
            state = _ST_SUFFIX_BEGIN
        elif state == _ST_LEFT_PARENTHESIS:
            #  Create a new hydrate group node and set its starting position..
            hyd = _ast_base.ASTNodeHydrateGroup()
            hyd.register_starting_position_in_source_text(token.get_position() + 1)

            #  Create a new parenthesis wrapper node and set its starting position.
            pw = _ast_base.ASTNodeParenthesisWrapper(hyd, ptr)
            pw.register_starting_position_in_source_text(token.get_position())

            #  Link the hydrate group node with the parenthesis wrapper node.
            hyd.set_parent_node(pw)

            #  Create a new molecule node and set its starting position.
            mol = _ast_base.ASTNodeMolecule(hyd)
            mol.register_starting_position_in_source_text(token.get_position() + 1)

            #  Finish the links.
            hyd.append_child(mol)
            ptr.append_child(pw)

            #  Set the working pointer to the new created molecule node.
            ptr = mol

            #  Next token.
            cursor += 1

            #  Jump to root state.
            state = _ST_ROOT
        elif state == _ST_RIGHT_PARENTHESIS:
            #  Find the parenthesis wrapper node in parent nodes.
            while ptr is not None:
                if ptr.is_molecule() or ptr.is_hydrate_group():
                    #  Set the ending position.
                    ptr.register_ending_position_in_source_text(token.get_position() - 1)
                elif ptr.is_parenthesis():
                    break
                else:
                    raise RuntimeError("Never reach this condition.")

                #  Go to parent node.
                ptr = ptr.get_parent_node()

            #  Raise an error if the node can't be found.
            if ptr is None:
                err = _pe.Error(_ml_error.PE_ML_PARENTHESIS_MISMATCH,
                                _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position(),
                                      _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_MISSING_LEFT)

                raise err

            #  Save the right parenthesis position.
            assert isinstance(ptr, _ast_base.ASTNodeParenthesisWrapper)
            ptr.set_right_parenthesis_position(token.get_position())

            #  Next token.
            cursor += 1

            #  Jump to read the suffix.
            state = _ST_SUFFIX_BEGIN
        elif state == _ST_HYDRATE_DOT:
            #  Set the ending position of current working molecule.
            ptr.register_ending_position_in_source_text(token.get_position() - 1)

            #  Go to the parent node.
            ptr = ptr.get_parent_node()
            """:type : _ast_base._ASTNodeBaseML"""

            #  Create a new molecule node and set its starting position.
            new_node = _ast_base.ASTNodeMolecule(ptr)
            new_node.register_starting_position_in_source_text(token.get_position() + 1)

            #  Link the new created node with current working node.
            ptr.append_child(new_node)
            ptr = new_node

            #  Next token.
            cursor += 1

            #  Jump to root state.
            state = _ST_ROOT
        elif state == _ST_STATUS:
            if not token_list[cursor + 1].is_end():
                err = _pe.Error(_ml_error.PE_ML_CONFLICT_STATUS,
                                _msg_id.MSG_PE_ML_MISPLACED_STATUS_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position() + len(token.get_symbol()) - 1,
                                      _msg_id.MSG_PE_ML_MISPLACED_STATUS_CONFLICTED)

                raise err

            #  Get new status ID.
            if token.is_gas_status():
                new_status = _ml_status.STATUS_GAS
            elif token.is_liquid_status():
                new_status = _ml_status.STATUS_LIQUID
            elif token.is_solid_status():
                new_status = _ml_status.STATUS_SOLID
            else:
                new_status = _ml_status.STATUS_AQUEOUS

            #  Set the status.
            ptr.set_status(new_status)

            #  Next token.
            cursor += 1

            #  Jump to root state.
            state = _ST_ROOT
        else:
            raise RuntimeError("Never reach this condition.")

    #  Calculate the ending position.
    ending_pos = token_list[-1].get_position() - 1

    #  Pre-create an error.
    err = _pe.Error(_ml_error.PE_ML_PARENTHESIS_MISMATCH,
                    _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                    options)

    #  Initialize the mismatch flag.
    mismatch_flag = False

    #  Check whether there are still some parenthesis nodes in parent nodes.
    while ptr is not None:
        if ptr.is_molecule() or ptr.is_hydrate_group():
            #  Set the ending position.
            ptr.register_ending_position_in_source_text(ending_pos)
        elif ptr.is_parenthesis():
            #  Mark the flag and add a description.
            mismatch_flag = True
            err.push_traceback_ex(expression,
                                  ptr.get_starting_position_in_source_text(),
                                  ptr.get_starting_position_in_source_text(),
                                  _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_MISSING_RIGHT)
        else:
            raise RuntimeError("Never reach this condition.")

        #  Go to the parent node.
        ptr = ptr.get_parent_node()

    #  Raise an error if the flag has been marked.
    if mismatch_flag:
        raise err

    #  Now, we have constructed the whole AST, but we got a lot of useless hydrate group node.
    #  So we have to remove them (all hydrate groups nodes which have only 1 child).

    #  Get iterate order.
    unpack_order = _ast_utils.do_bfs(root, True)

    #  Initialize unpacked node container.
    unpacked = {}

    for node in unpack_order:
        if node.is_hydrate_group():
            assert isinstance(node, _ast_base.ASTNodeHydrateGroup)

            if len(node) == 1:
                #  Get the child node and reset its parent
                child = unpacked[id(node[0])]
                child.set_parent_node(node.get_parent_node())

                #  Save the unpack result.
                unpacked[id(node)] = child
            else:
                #  Update children links.
                for child_id in range(0, len(node)):
                    node[child_id] = unpacked[id(node[child_id])]

                #  Save the unpack result.
                unpacked[id(node)] = node
        elif node.is_molecule():
            assert isinstance(node, _ast_base.ASTNodeMolecule)

            #  Update children links.
            for child_id in range(0, len(node)):
                node[child_id] = unpacked[id(node[child_id])]

            #  Save the unpack result.
            unpacked[id(node)] = node
        elif node.is_parenthesis():
            assert isinstance(node, _ast_base.ASTNodeParenthesisWrapper)

            #  Update children links.
            node.set_inner_node(unpacked[id(node.get_inner_node())])

            #  Save  the unpack result.
            unpacked[id(node)] = node
        else:
            #  Save  the unpack result.
            unpacked[id(node)] = node

    return unpacked[id(root)]