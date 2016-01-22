#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.ce.base as _ce_base
import bce.math.matrix as _math_mtx
import bce.math.equation as _math_equ
import bce.math.constant as _math_const
import bce.option as _opt
import sympy as _sympy


def build_matrix(ce):
    """Construct linear equations from the a chemical equation.

    :type ce: _ce_base.ChemicalEquation
    :param ce: The chemical equation (represented by ChemicalEquation).
    :rtype : _math_mtx.Matrix
    :return: A matrix contains the linear equations.
    """

    #  A dictionary that contains the row index of each atom / electronic.
    ref_atom_idx = {}

    #  Row index counter.
    ref_atom_counter = 0

    #  Calculate the row index of each atom.
    #  Process left items.
    for idx in range(0, ce.get_left_item_count()):
        #  Get the atom dictionary of the molecule.
        atom_dict = ce.get_left_item(idx).get_atoms_dictionary()

        #  Process atoms.
        for atom_symbol in atom_dict:
            if atom_symbol not in ref_atom_idx:
                #  Write the row index of the atom and increase the row counter.
                ref_atom_idx[atom_symbol] = ref_atom_counter
                ref_atom_counter += 1

    #  Process right items.
    for idx in range(0, ce.get_right_item_count()):
        #  Get the atom dictionary of the molecule.
        atom_dict = ce.get_right_item(idx).get_atoms_dictionary()

        #  Process atoms.
        for atom_symbol in atom_dict:
            if atom_symbol not in ref_atom_idx:
                #  Write the row index of the atom and increase the row counter.
                ref_atom_idx[atom_symbol] = ref_atom_counter
                ref_atom_counter += 1

    #  Build an empty matrix that only contains zero.
    mtx = _math_mtx.Matrix(len(ref_atom_idx), len(ce) + 1, _math_const.ZERO)

    #  Initialize column index counter.
    col_id = 0

    #  Process items on the left side.
    for idx in range(0, ce.get_left_item_count()):
        #  Get the item.
        item = ce.get_left_item(idx)

        #  Get the atom dictionary of the molecule.
        atom_dict = item.get_atoms_dictionary()

        for atom in atom_dict:
            #  Write the count of each atom to specific position.
            if item.is_operator_plus():
                mtx.write_item_by_position(ref_atom_idx[atom], col_id, atom_dict[atom])
            else:
                mtx.write_item_by_position(ref_atom_idx[atom], col_id, -atom_dict[atom])

        #  Increase the column counter.
        col_id += 1

    #  Process items on the right side.
    for idx in range(0, ce.get_right_item_count()):
        #  Get the item.
        item = ce.get_right_item(idx)

        #  Get the atom dictionary of the molecule.
        atom_dict = item.get_atoms_dictionary()

        for atom in atom_dict:
            #  Write the count of each atom to specific position.
            if item.is_operator_plus():
                mtx.write_item_by_position(ref_atom_idx[atom], col_id, -atom_dict[atom])
            else:
                mtx.write_item_by_position(ref_atom_idx[atom], col_id, atom_dict[atom])

        #  Increase the column counter.
        col_id += 1

    return mtx


def matrix_post_solving(solve_result, options):
    """Post solving process.

    :type solve_result: _math_equ.SolvedEquation
    :type options: _opt.Option
    :param solve_result: The equations solving result.
    :param options: The BCE options.
    :rtype : _math_equ.SolvedEquation
    :return: The equations solving result after processing.
    """

    if solve_result.get_unknown_count() <= 1:
        #  Replace '[Xa]' with 1.

        #  Get the symbol of [Xa].
        replace_symbol = _sympy.Symbol(_math_equ.unknown_id_to_symbol(0, options.get_protected_math_symbol_header()))

        #  Replace.
        new_answer_list = []
        for origin_answer in solve_result.get_answer_list():
            new_answer_list.append(origin_answer.subs({replace_symbol: _math_const.ONE}))

        return _math_equ.SolvedEquation(new_answer_list, 0)
    else:
        return solve_result