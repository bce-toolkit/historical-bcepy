#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.decompiler.molecule.ast_to_bce as _ml_decompiler
import bce.parser.ce.base as _ce_base


def decompile_ce(ce):
    """Decompile the chemical equation.

    :type ce: _ce_base.ChemicalEquation
    :param ce: The chemical equation (represented by ChemicalEquation class).
    :rtype : str
    :return: The decompiling result.
    """

    assert ce.get_left_item_count() != 0 and ce.get_right_item_count() != 0

    #  Initialize an empty CE expression.
    r = ""

    #  Process items on left side.
    for idx in range(0, ce.get_left_item_count()):
        #  Get the item.
        item = ce.get_left_item(idx)

        #  Insert operator.
        if item.is_operator_plus():
            if len(r) != 0:
                r += "+"

        if item.is_operator_minus():
            r += "-"

        #  Get the AST root node.
        ast_root = item.get_molecule_ast()

        #  Backup the prefix number.
        origin_coefficient = ast_root.get_prefix_number()

        #  Set the prefix to the balanced coefficient.
        ast_root.set_prefix_number(item.get_coefficient() * origin_coefficient)

        #  Decompile the molecule.
        r += _ml_decompiler.decompile_ast(ast_root)

        #  Restore the prefix number.
        ast_root.set_prefix_number(origin_coefficient)

    #  Insert '='.
    r += "="

    #  Mark whether processing molecule is the first molecule on right side.
    r_is_first = True

    #  Process items on right side.
    for idx in range(0, ce.get_right_item_count()):
        #  Get the item.
        item = ce.get_right_item(idx)

        #  Insert operator.
        if item.is_operator_plus():
            if not r_is_first:
                r += "+"

        if item.is_operator_minus():
            r += "-"

        #  Get the AST root node.
        ast_root = item.get_molecule_ast()

        #  Backup the prefix number.
        origin_coefficient = ast_root.get_prefix_number()

        #  Set the prefix to the balanced coefficient.
        ast_root.set_prefix_number(item.get_coefficient() * origin_coefficient)

        #  Decompile the molecule.
        r += _ml_decompiler.decompile_ast(ast_root)

        #  Restore the prefix number.
        ast_root.set_prefix_number(origin_coefficient)

        #  Switch off the mark.
        r_is_first = False

    return r
