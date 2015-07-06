#!/usr/bin/env python
#
#  Copyright 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.option as _opt
import bce.parser.ce.parser as _ce_parser
import bce.parser.molecule.ast_base as _ml_ast_base
import bce.parser.molecule.decompiler.ast_to_mathml as _ml_decompiler
import bce.utils.mathml.all as _mathml
import bce.logic.arrange as _logic_arrange


def decompile_combined_result(combined_result, options):
    """Decompile the combined balanced result to a human-readable form (string).

    :type options: _opt.Option
    :type combined_result: _logic_arrange.CombinedResult
    :param combined_result: The combined result.
    :param options: The BCE options.
    :return: The rebuilt result.
    """

    #  Initialize an empty CE expression.
    r = _mathml.RowComponent()

    #  Cache items on left and right side.
    li = combined_result.get_left_items()
    ri = combined_result.get_right_items()

    #  Process items on left side.
    for item in li:
        #  Insert operator.
        if item.get_operator() == _ce_parser.PARSED_CE_ITEM_OP_PLUS:
            if len(r) != 0:
                r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_PLUS))

        if item.get_operator() == _ce_parser.PARSED_CE_ITEM_OP_MINUS:
            r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_MINUS))

        #  Get the AST root node.
        ast_root = item.get_molecule()
        assert isinstance(ast_root, _ml_ast_base.ASTNodeHydrateGroup) or \
            isinstance(ast_root, _ml_ast_base.ASTNodeMolecule)

        #  Save origin prefix number.
        origin_pfx = ast_root.get_prefix_number()

        #  Set the prefix to the balanced coefficient.
        ast_root.set_prefix_number(item.get_coefficient())

        #  Decompile the molecule.
        r.append_object(_ml_decompiler.decompile_ast(ast_root, options))

        #  Restore the prefix number.
        ast_root.set_prefix_number(origin_pfx)

    #  Insert '='.
    r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_EQUAL))

    #  Mark whether processing molecule is the first molecule on right side.
    r_is_first = True

    #  Process items on right side.
    for item in ri:
        #  Insert operator.
        if item.get_operator() == _ce_parser.PARSED_CE_ITEM_OP_PLUS:
            if not r_is_first:
                r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_PLUS))

        if item.get_operator() == _ce_parser.PARSED_CE_ITEM_OP_MINUS:
            r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_MINUS))

        #  Get the AST root node.
        ast_root = item.get_molecule()
        assert isinstance(ast_root, _ml_ast_base.ASTNodeHydrateGroup) or \
            isinstance(ast_root, _ml_ast_base.ASTNodeMolecule)

        #  Save origin prefix number.
        origin_pfx = ast_root.get_prefix_number()

        #  Set the prefix to the balanced coefficient.
        ast_root.set_prefix_number(item.get_coefficient())

        #  Decompile the molecule.
        r.append_object(_ml_decompiler.decompile_ast(ast_root, options))

        #  Restore the prefix number.
        ast_root.set_prefix_number(origin_pfx)

        #  Switch off the mark.
        r_is_first = False

    return r