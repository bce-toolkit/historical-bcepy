#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.ce.token as _ce_token
import bce.parser.ce.parser as _ce_parser
# noinspection PyUnresolvedReferences
import bce.parser.molecule.ast_base as _ast_base
import bce.parser.molecule.ast_parser as _ast_parser
import bce.parser.molecule.ast_substitution as _ast_subst
import bce.math.constant as _math_cst
import bce.math.equation as _math_equ
import bce.logic.arrange as _logic_arrange
import bce.option as _opt


def _substitute_atom_dictionary(origin_dict, subst_map):
    """Do substitution on an atom dictionary.

    :type origin_dict: dict
    :type subst_map: dict
    :param origin_dict: The origin atom dictionary.
    :param subst_map: The substitution map.
    :rtype : dict
    :return: The substituted map.
    """

    #  Initialize a new map.
    ret = {}

    #  Iterate all atoms.
    for atom_symbol in origin_dict:
        #  Do substitution on the coefficient and simplify it.
        val = origin_dict[atom_symbol].subs(subst_map).simplify()

        #  Add the atom if the coefficient is not zero.
        if not val.is_zero:
            ret[atom_symbol] = val

    return ret


def substitute_ce(parsed_ce, subst_map, options):
    """Do substitution on a parsed chemical equation.

    :type subst_map: dict
    :type parsed_ce: _ce_parser.ParsedCE
    :type options: _opt.Option
    :param parsed_ce: The parsed chemical equation.
    :param subst_map: The substitution map.
    :param options: The BCE options.
    :rtype : _logic_arrange.CombinedResult
    :return: The combined result (presents with CombinedResult class).
    """

    assert parsed_ce.get_form() == _ce_token.TOKENIZED_CE_FORM_NORMAL

    #  Save the origin protected math symbol header.
    protect_hdr = options.get_protected_math_symbol_header()

    #  Ignore the protected math symbol during substitution progress.
    options.set_protected_math_symbol_header("_")

    #  Initialize the coefficient container and molecule containers.
    coeff = []
    left_items = []
    right_items = []

    for item in parsed_ce.get_left_items():
        #  Do substitution on current molecule.
        mol = _ast_subst.substitute_ast(item.get_molecule().get_ast_root(), subst_map)
        """:type : _ast_base.ASTNodeMolecule | _ast_base.ASTNodeHydrateGroup"""

        #  Ignore the molecule if the whole molecule has been eliminated.
        if mol is None:
            continue

        #  Treat the prefix number as the balanced coefficient.
        coeff.append(mol.get_prefix_number())

        #  Remove the prefix number.
        mol.set_prefix_number(_math_cst.ONE)

        #  Re-wrap the molecule and add it to the container.
        atom_dict = _substitute_atom_dictionary(item.get_molecule().get_atom_dictionary(), subst_map)
        left_items.append(_ce_parser.ParsedCEItem(item.get_operator(),
                                                  _ast_parser.ResultContainer(mol, mol.get_status(), atom_dict)))
    for item in parsed_ce.get_right_items():
        #  Do substitution on current molecule.
        mol = _ast_subst.substitute_ast(item.get_molecule().get_ast_root(), subst_map)
        """:type : _ast_base.ASTNodeMolecule | _ast_base.ASTNodeHydrateGroup"""

        #  Ignore the molecule if the whole molecule has been eliminated.
        if mol is None:
            continue

        #  Treat the prefix number as the balanced coefficient.
        coeff.append(mol.get_prefix_number())

        #  Remove the prefix number.
        mol.set_prefix_number(_math_cst.ONE)

        #  Re-wrap the molecule and add it to the container.
        atom_dict = _substitute_atom_dictionary(item.get_molecule().get_atom_dictionary(), subst_map)
        right_items.append(_ce_parser.ParsedCEItem(item.get_operator(),
                                                   _ast_parser.ResultContainer(mol, mol.get_status(), atom_dict)))

    #  Re-wrap the chemical equation and coefficients.
    new_ce = _ce_parser.ParsedCE(left_items, right_items, _ce_token.TOKENIZED_CE_FORM_NORMAL)
    new_coeff = _math_equ.SolvedEquation(coeff, 0)

    #  Sort out.
    srt = _logic_arrange.sort_out_results(new_coeff, _ce_token.TOKENIZED_CE_FORM_NORMAL, options)

    #  Do combination.
    ret = _logic_arrange.combine_result(new_ce, srt, options)

    #  Restore the protected math symbol header.
    options.set_protected_math_symbol_header(protect_hdr)

    return ret