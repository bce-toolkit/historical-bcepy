#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.math.constant as _math_cst
import bce.parser.ce.base as _ce_base
import bce.parser.molecule.ast.substitution as _ml_ast_subst
import bce.parser.molecule.ast.parser as _ml_ast_parser
import bce.parser.common.error as _pe
import bce.option as _opt
import sympy as _sympy


class SubstituteError(Exception):
    """Chemical equation substitution error."""
    pass


def _check_substituted_mexp(value):
    """Check the substituted math expression.

    :param value: The value math expression.
    :raise SubstituteError: Raise this error if the value is invalid.
    """

    if isinstance(value, _sympy.S.ComplexInfinity.__class__):
        raise SubstituteError("Divided zero.")


def substitute_ce(ce, subst_map, options):
    """Do substitution on a chemical equation.

    :type ce: _ce_base.ChemicalEquation
    :type subst_map: dict
    :type options: _opt.Option
    :param ce: The chemical equation required to be substituted (represented by ChemicalEquation class).
    :param subst_map: The substitution map.
    :param options: The BCE options.
    :rtype : _ce_base.ChemicalEquation
    :return: The substituted chemical equation (represented by ChemicalEquation class).
    """

    if ce.get_left_item_count() == 0 or ce.get_right_item_count() == 0:
        raise SubstituteError("Unsupported form.")

    #  Initialize an empty chemical equation.
    new_ce = _ce_base.ChemicalEquation()

    #  Process left items.
    for idx in range(0, ce.get_left_item_count()):
        #  Get the item.
        item = ce.get_left_item(idx)

        #  Get and substitute the AST.
        try:
            ast_root = _ml_ast_subst.substitute_ast(item.get_molecule_ast(), subst_map)
        except _ml_ast_subst.SubstituteError:
            raise SubstituteError("Can't substitute sub-molecule.")

        #  Substitute the origin coefficient.
        item_coeff = item.get_coefficient().subs(subst_map).simplify()
        _check_substituted_mexp(item_coeff)

        if ast_root is None:
            continue

        #  Get and substitute the coefficient.
        coeff = (item_coeff * ast_root.get_prefix_number()).simplify()
        _check_substituted_mexp(coeff)

        #  Clear the prefix number of the AST.
        ast_root.set_prefix_number(_math_cst.ONE)

        #  Re-parse the AST.
        try:
            #  Re-parse.
            atom_dict = _ml_ast_parser.parse_ast("-", ast_root, options)

            #  Add the substituted item.
            new_ce.append_left_item(item.get_operator_id(), coeff, ast_root, atom_dict)
        except _pe.Error:
            raise SubstituteError("Re-parse error.")

    #  Process right items.
    for idx in range(0, ce.get_right_item_count()):
        #  Get the item.
        item = ce.get_right_item(idx)

        #  Get and substitute the AST.
        try:
            ast_root = _ml_ast_subst.substitute_ast(item.get_molecule_ast(), subst_map)
        except _ml_ast_subst.SubstituteError:
            raise SubstituteError("Can't substitute sub-molecule.")

        #  Substitute the origin coefficient.
        item_coeff = item.get_coefficient().subs(subst_map).simplify()
        _check_substituted_mexp(item_coeff)

        if ast_root is None:
            continue

        #  Get and substitute the coefficient.
        coeff = (item_coeff * ast_root.get_prefix_number()).simplify()
        _check_substituted_mexp(coeff)

        #  Clear the prefix number of the AST.
        ast_root.set_prefix_number(_math_cst.ONE)

        try:
            #  Re-parse.
            atom_dict = _ml_ast_parser.parse_ast("-", ast_root, options)

            #  Add the substituted item.
            new_ce.append_right_item(item.get_operator_id(), coeff, ast_root, atom_dict)
        except _pe.Error:
            raise SubstituteError("Re-parse error.")

    #  Remove items with coefficient 0.
    new_ce.remove_items_with_coefficient_zero()

    #  Move items that have negative coefficient to another side.
    new_ce.move_items_with_negative_coefficient_to_another_side()

    #  Integerize the coefficients.
    new_ce.coefficients_integerize()

    #  Check.
    if new_ce.get_left_item_count() == 0 or new_ce.get_right_item_count() == 0:
        raise SubstituteError("Side(s) eliminated.")

    return new_ce