#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.decompiler.molecule.ast_to_mathml as _ml_decompiler
import bce.parser.ce.base as _ce_base
import bce.utils.mathml.all as _mathml
import bce.option as _opt


def decompile_ce(ce, options):
    """Decompile the combined balanced result to a human-readable form (string).

    :type ce: _ce_base.ChemicalEquation
    :type options: _opt.Option
    :param ce: The chemical equation (represented by ChemicalEquation class).
    :param options: The BCE options.
    :return: The decompiling result.
    """

    assert ce.get_left_item_count() != 0 and ce.get_right_item_count() != 0

    #  Initialize an empty CE expression.
    r = _mathml.RowComponent()

    #  Process items on left side.
    for idx in range(0, ce.get_left_item_count()):
        #  Get the item.
        item = ce.get_left_item(idx)

        #  Insert operator.
        if item.is_operator_plus():
            if len(r) != 0:
                r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_PLUS))

        if item.is_operator_minus():
            r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_MINUS))

        #  Get the AST root node.
        ast_root = item.get_molecule_ast()

        #  Backup the prefix number.
        origin_coefficient = ast_root.get_prefix_number()

        #  Set the prefix to the balanced coefficient.
        ast_root.set_prefix_number(item.get_coefficient() * origin_coefficient)

        #  Decompile the molecule.
        r.append_object(_ml_decompiler.decompile_ast(ast_root, options))

        #  Restore the prefix number.
        ast_root.set_prefix_number(origin_coefficient)

    #  Insert '='.
    r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_EQUAL))

    #  Mark whether processing molecule is the first molecule on right side.
    r_is_first = True

    #  Process items on right side.
    for idx in range(0, ce.get_right_item_count()):
        #  Get the item.
        item = ce.get_right_item(idx)

        #  Insert operator.
        if item.is_operator_plus():
            if not r_is_first:
                r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_PLUS))

        if item.is_operator_minus():
            r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_MINUS))

        #  Get the AST root node.
        ast_root = item.get_molecule_ast()

        #  Backup the prefix number.
        origin_coefficient = ast_root.get_prefix_number()

        #  Set the prefix to the balanced coefficient.
        ast_root.set_prefix_number(item.get_coefficient() * origin_coefficient)

        #  Decompile the molecule.
        r.append_object(_ml_decompiler.decompile_ast(ast_root, options))

        #  Restore the prefix number.
        ast_root.set_prefix_number(origin_coefficient)

        #  Switch off the mark.
        r_is_first = False

    return r
