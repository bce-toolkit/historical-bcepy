#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.locale.msg_id as _msg_id
import bce.math.constant as _math_cst
import bce.parser.common.error as _pe
import bce.parser.molecule.ast.base as _ast_base
import bce.parser.molecule.ast.bfs as _ast_bfs
import bce.parser.molecule.error as _ml_error
import bce.parser.molecule.status as _ml_status
import bce.parser.molecule.token as _ml_token
import bce.option as _opt

#  States of the state machine.
_STATE_ROOT = 1
_STATE_ATOM = 2
_STATE_ABBREVIATION = 3
_STATE_LEFT_PARENTHESIS = 4
_STATE_RIGHT_PARENTHESIS = 5
_STATE_ELECTRONIC = 6
_STATE_HYDRATE_DOT = 7
_STATE_PREFIX_NUMBER = 8
_STATE_SUFFIX_NUMBER = 9
_STATE_MOLECULE_STATUS = 10


def generate_ast(expression, token_list, options):
    """Generate an AST from the token list.

    :type expression: str
    :type token_list: list[_ml_token.Token]
    :type options: _opt.Option
    :param expression: The origin expression.
    :param token_list: The token list.
    :param options: The BCE options.
    :rtype : _ast_base.ASTNodeHydrateGroup | _ast_base.ASTNodeMolecule
    :return: The root node of the generated AST.
    """

    #  Initialize the molecule status container.
    molecule_status = None

    #  Initialize the state machine.
    state = _STATE_ROOT

    #  Generate initial AST.
    root = _ast_base.ASTNodeHydrateGroup()
    node = _ast_base.ASTNodeMolecule(root)
    root.append_child(node)

    #  Register the starting position.
    root.register_starting_position_in_source_text(0)
    node.register_starting_position_in_source_text(0)

    #  Initialize the token cursor.
    cursor = 0

    while True:
        #  Get current token.
        token = token_list[cursor]

        if state == _STATE_ROOT:
            #  Find molecule in parent nodes and current node.
            while node is not None and not node.is_molecule():
                node = node.get_parent_node()
            if node is None:
                raise RuntimeError("BUG: Can't find molecule group.")

            #  Redirect by rules.
            if token.is_operand() and len(node) == 0:
                state = _STATE_PREFIX_NUMBER
            elif token.is_symbol():
                state = _STATE_ATOM
            elif token.is_abbreviation():
                state = _STATE_ABBREVIATION
            elif token.is_left_parenthesis():
                state = _STATE_LEFT_PARENTHESIS
            elif token.is_right_parenthesis():
                state = _STATE_RIGHT_PARENTHESIS
            elif token.is_electronic_begin():
                state = _STATE_ELECTRONIC
            elif token.is_hydrate_dot():
                state = _STATE_HYDRATE_DOT
            elif token.is_status():
                state = _STATE_MOLECULE_STATUS
            elif token.is_end():
                break
            else:
                #  Raise an error if the token can't be recognized.
                err = _pe.Error(_ml_error.PE_ML_UNEXPECTED_TOKEN,
                                _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position() + len(token.get_symbol()) - 1,
                                      _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_DEFAULT)

                raise err
        elif state == _STATE_ATOM:
            #  Create a new atom node and register its starting position.
            new_node = _ast_base.ASTNodeAtom(token.get_symbol(), node)
            new_node.register_starting_position_in_source_text(token.get_position())

            #  Add the node to the molecule group.
            node.append_child(new_node)

            #  Switch the node pointer to the new created node.
            node = new_node

            #  Next token.
            cursor += 1

            #  Go to read the suffix number.
            state = _STATE_SUFFIX_NUMBER
        elif state == _STATE_ABBREVIATION:
            #  Create a new abbreviation node and register its starting position.
            new_node = _ast_base.ASTNodeAbbreviation(token.get_symbol()[1:-1], node)
            new_node.register_starting_position_in_source_text(token.get_position())

            #  Add the node to the molecule group.
            node.append_child(new_node)

            #  Switch the node pointer to the new created node.
            node = new_node

            #  Next token.
            cursor += 1

            #  Go to read the suffix number.
            state = _STATE_SUFFIX_NUMBER
        elif state == _STATE_LEFT_PARENTHESIS:
            #  Create new nodes.
            new_hydrate_grp = _ast_base.ASTNodeHydrateGroup()
            new_molecule = _ast_base.ASTNodeMolecule(new_hydrate_grp)
            new_parenthesis = _ast_base.ASTNodeParenthesisWrapper(new_hydrate_grp, node)

            #  Link them correctly and them add the new created parenthesis node to the molecule group.
            new_hydrate_grp.set_parent_node(new_parenthesis)
            new_hydrate_grp.append_child(new_molecule)
            node.append_child(new_parenthesis)

            #  Switch the node pointer to the new created molecule node.
            node = new_molecule

            #  Register their starting positions.
            new_hydrate_grp.register_starting_position_in_source_text(token.get_position() + 1)
            new_molecule.register_starting_position_in_source_text(token.get_position() + 1)
            new_parenthesis.register_starting_position_in_source_text(token.get_position())

            #  Next token.
            cursor += 1

            #  Go to root state.
            state = _STATE_ROOT
        elif state == _STATE_RIGHT_PARENTHESIS:
            #  Find parenthesis node in parent nodes and current node.
            while node is not None and not node.is_parenthesis():
                #  Register the ending position of current working node.
                node.register_ending_position_in_source_text(token.get_position() - 1)

                #  Go to the parent node.
                node = node.get_parent_node()

            #  Raise an error if the node can't be found.
            if node is None:
                err = _pe.Error(_ml_error.PE_ML_PARENTHESIS_MISMATCH,
                                _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position(),
                                      _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_MISSING_LEFT)

                raise err

            #  Register the ending position of current working node.
            node.set_right_parenthesis_position(token.get_position())

            #  Next token.
            cursor += 1

            #  Go to read the suffix number.
            state = _STATE_SUFFIX_NUMBER
        elif state == _STATE_ELECTRONIC:
            #  Save the starting position of the electronic descriptor.
            e_start_pos = token.get_position()

            #  Next token.
            cursor += 1
            token = token_list[cursor]

            #  Try to read the prefix number.
            e_pfx = _math_cst.ONE
            e_pfx_start = token.get_position()
            has_e_pfx_number = False
            while token.is_operand():
                #  Mark the flag.
                has_e_pfx_number = True

                #  Process the prefix number.
                e_pfx *= token.get_operand_value().simplify()

                #  Next token.
                cursor += 1
                token = token_list[cursor]
            e_pfx = e_pfx.simplify()

            #  Domain check.
            if e_pfx.is_negative or e_pfx.is_zero:
                err = _pe.Error(_ml_error.PE_ML_DOMAIN_ERROR,
                                _msg_id.MSG_PE_ML_DOMAIN_ERROR_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      e_pfx_start,
                                      token.get_position() - 1,
                                      _msg_id.MSG_PE_ML_DOMAIN_ERROR_EL_CHG)

                raise err

            #  Validate.
            if has_e_pfx_number and e_pfx == _math_cst.ONE:
                err = _pe.Error(_ml_error.PE_ML_USELESS_OPERAND,
                                _msg_id.MSG_PE_ML_USELESS_OPERAND_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      e_pfx_start,
                                      token.get_position() - 1,
                                      _msg_id.MSG_PE_ML_USELESS_OPERAND_EL_CHG)

                raise err

            #  Process the electronic positivity flag.
            if token.is_electronic_positive_flag():
                pass
            elif token.is_electronic_negative_flag():
                e_pfx = -e_pfx
            else:
                if token.is_end():
                    err = _pe.Error(_ml_error.PE_ML_PARENTHESIS_MISMATCH,
                                    _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                                    options)
                    err.push_traceback_ex(expression,
                                          e_start_pos,
                                          token.get_position() - 1,
                                          _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_MISSING_RIGHT)
                else:
                    #  Raise an error if current working token is not an electronic positivity flag.
                    err = _pe.Error(_ml_error.PE_ML_UNEXPECTED_TOKEN,
                                    _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(expression,
                                          token.get_position(),
                                          token.get_position() + len(token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_EL_POSITIVITY_OR_INTEGER)

                raise err

            #  Next token.
            cursor += 1
            token = token_list[cursor]

            #  Raise an error if current working token is not '>'.
            if not token.is_electronic_end():
                if token.is_end():
                    err = _pe.Error(_ml_error.PE_ML_PARENTHESIS_MISMATCH,
                                    _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                                    options)
                    err.push_traceback_ex(expression,
                                          e_start_pos,
                                          token.get_position() - 1,
                                          _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_MISSING_RIGHT)
                else:
                    err = _pe.Error(_ml_error.PE_ML_UNEXPECTED_TOKEN,
                                    _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(expression,
                                          token.get_position(),
                                          token.get_position() + len(token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_EL_END)

                raise err

            #  Next token.
            cursor += 1
            token = token_list[cursor]

            #  Raise an error if the electronic descriptor is not at the end of a molecule block.
            if not (token.is_right_parenthesis() or token.is_hydrate_dot() or token.is_end() or token.is_status()):
                err = _pe.Error(_ml_error.PE_ML_UNEXPECTED_TOKEN,
                                _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      e_start_pos,
                                      token.get_position() - 1,
                                      _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_EL_MISPLACED)

                raise err

            #  Set the electronic count.
            node.set_electronic_count(e_pfx)

            #  Go to root state.
            state = _STATE_ROOT
        elif state == _STATE_HYDRATE_DOT:
            #  Save the ending position of current working node.
            node.register_ending_position_in_source_text(token.get_position() - 1)

            #  Go to parent node.
            node = node.get_parent_node()
            assert isinstance(node, _ast_base.ASTNodeHydrateGroup)

            #  Create a new molecule node and set its starting position.
            new_molecule = _ast_base.ASTNodeMolecule(node)
            new_molecule.register_starting_position_in_source_text(token.get_position() + 1)

            #  Add the new created molecule node to the hydrate group node.
            node.append_child(new_molecule)

            #  Switch the node pointer to the new created molecule node.
            node = new_molecule

            #  Next token.
            cursor += 1

            #  Go to root state.
            state = _STATE_ROOT
        elif state == _STATE_PREFIX_NUMBER:
            #  Save the starting position of the prefix.
            pfx_start = token.get_position()

            #  Read prefix numbers.
            has_pfx_number = False
            while token.is_operand():
                #  Mark the flag.
                has_pfx_number = True

                #  Process the prefix number.
                node.set_prefix_number(node.get_prefix_number() * token.get_operand_value().simplify())

                #  Next token.
                cursor += 1
                token = token_list[cursor]
            pfx = node.get_prefix_number().simplify()

            #  Domain check.
            if pfx.is_negative or pfx.is_zero:
                err = _pe.Error(_ml_error.PE_ML_DOMAIN_ERROR,
                                _msg_id.MSG_PE_ML_DOMAIN_ERROR_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      pfx_start,
                                      token.get_position() - 1,
                                      _msg_id.MSG_PE_ML_DOMAIN_ERROR_PFX)

                raise err

            #  Validate.
            if has_pfx_number and pfx == _math_cst.ONE:
                err = _pe.Error(_ml_error.PE_ML_USELESS_OPERAND,
                                _msg_id.MSG_PE_ML_USELESS_OPERAND_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      pfx_start,
                                      token.get_position() - 1,
                                      _msg_id.MSG_PE_ML_USELESS_OPERAND_PFX)

                raise err

            #  Set the prefix number.
            node.set_prefix_number(pfx)

            #  Go to root state.
            state = _STATE_ROOT
        elif state == _STATE_SUFFIX_NUMBER:
            #  Save the starting position of the suffix.
            sfx_start = token.get_position()

            #  Read suffix numbers.
            has_sfx_number = False
            while token.is_operand():
                #  Mark the flag.
                has_sfx_number = True

                #  Process the suffix number.
                node.set_suffix_number(node.get_suffix_number() * token.get_operand_value().simplify())

                #  Next token.
                cursor += 1
                token = token_list[cursor]

            sfx = node.get_suffix_number().simplify()

            #  Domain check.
            if sfx.is_negative or sfx.is_zero:
                err = _pe.Error(_ml_error.PE_ML_DOMAIN_ERROR,
                                _msg_id.MSG_PE_ML_DOMAIN_ERROR_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      sfx_start,
                                      token.get_position() - 1,
                                      _msg_id.MSG_PE_ML_DOMAIN_ERROR_SFX)

                raise err

            #  Validate.
            if has_sfx_number and sfx == _math_cst.ONE:
                err = _pe.Error(_ml_error.PE_ML_USELESS_OPERAND,
                                _msg_id.MSG_PE_ML_USELESS_OPERAND_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      sfx_start,
                                      token.get_position() - 1,
                                      _msg_id.MSG_PE_ML_USELESS_OPERAND_SFX)

                raise err

            #  Register the ending position of current working node.
            node.register_ending_position_in_source_text(token.get_position() - 1)

            #  Go to root state.
            state = _STATE_ROOT
        elif state == _STATE_MOLECULE_STATUS:
            #  Raise an error if the token is not at the end of the molecule.
            if not token_list[cursor + 1].is_end():
                err = _pe.Error(_ml_error.PE_ML_UNEXPECTED_TOKEN,
                                _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position() + len(token.get_symbol()) - 1,
                                      _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_STATUS_MISPLACED)

                raise err

            #  Fetch the molecule status.
            if token.is_gas_status():
                molecule_status = _ml_status.STATUS_GAS
            elif token.is_liquid_status():
                molecule_status = _ml_status.STATUS_LIQUID
            elif token.is_solid_status():
                molecule_status = _ml_status.STATUS_SOLID
            elif token.is_aqueous_status():
                molecule_status = _ml_status.STATUS_AQUEOUS
            else:
                raise RuntimeError("BUG: Unrecognized status.")

            #  Next token.
            cursor += 1

            #  Go to root state.
            state = _STATE_ROOT
        else:
            raise RuntimeError("BUG: Unrecognized state.")

    #  Get the ending position.
    ending_pos = token_list[-1].get_position() - 1

    #  Initialize the parenthesis-mismatched flag.
    mismatch_flag = False

    #  Pre-create an error.
    err = _pe.Error(_ml_error.PE_ML_PARENTHESIS_MISMATCH,
                    _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                    options)

    while node is not None:
        #  Register the ending position of current working node.
        node.register_ending_position_in_source_text(ending_pos)

        #  Mark the error flag and add an error description if current node is a parenthesis node.
        if node.is_parenthesis():
            mismatch_flag = True
            err.push_traceback_ex(expression,
                                  node.get_starting_position_in_source_text(),
                                  node.get_starting_position_in_source_text(),
                                  _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_MISSING_RIGHT)

        #  Go to parent node.
        node = node.get_parent_node()

    #  Raise an error if we have met at least 1 parenthesis node.
    if mismatch_flag:
        raise err

    #  Now, we have constructed the whole AST, but we got a lot of useless hydrate group node.
    #  So we have to remove them (all hydrate groups nodes which have only 1 child).

    #  Get iterate order.
    unpack_order = _ast_bfs.do_bfs(root, True)

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

    #  Set molecule status.
    root = unpacked[id(root)]
    """:type : _ast_base.ASTNodeHydrateGroup | _ast_base.ASTNodeMolecule"""
    root.set_status(molecule_status)

    return root
