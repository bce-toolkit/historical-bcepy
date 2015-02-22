#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.ce.parser as _ce_parser
import bce.math.matrix as _math_mtx
import bce.math.constant as _math_const


def build_matrix(parsed_ce):
    """Construct linear equations from the parsed chemical equation.

    :type parsed_ce: _ce_parser.ParsedCE
    :param parsed_ce: The parsed chemical equation.
    :rtype : _math_mtx.Matrix
    :return: A matrix contains the linear equations.
    """

    #  A dictionary that contains the row index of each atom / electronic.
    ref_atom_idx = {}

    #  Row index counter.
    ref_atom_counter = 0

    #  Cache molecules on the left side and the right side.
    left_mls = parsed_ce.get_left_items()
    right_mls = parsed_ce.get_right_items()
    total_list = left_mls + right_mls

    #  First loop, calculate the row index of each atom / electronic.
    for process_ml in total_list:
        #  Get molecule information.
        ml_info = process_ml.get_molecule()

        #  Get the electronic count of the molecule.
        e_count = ml_info.get_electronic_count()

        #  Process electronic.
        if (not e_count.is_zero) and (not "e" in ref_atom_idx):
            #  Write the row index of the electronic and increase the row counter.
            ref_atom_idx["e"] = ref_atom_counter
            ref_atom_counter += 1

        #  Get the atom dictionary of the molecule.
        atom_dict = ml_info.get_atom_dictionary()

        #  Process atoms.
        for atom in atom_dict:
            if not atom in ref_atom_idx:
                #  Write the row index of the atom and increase the row counter.
                ref_atom_idx[atom] = ref_atom_counter
                ref_atom_counter += 1

    #  Build an empty matrix that only contains zero.
    mtx = _math_mtx.Matrix(len(ref_atom_idx), len(total_list) + 1, _math_const.ZERO)

    #  Initialize column index counter.
    col_id = 0

    #  Process items on the left side.
    for process_ml in left_mls:
        #  Get molecule information.
        ml_info = process_ml.get_molecule()

        #  Get the electronic count of the molecule.
        e_count = ml_info.get_electronic_count()

        #  Get whether the operator before the molecule is '+' or '=' or nothing.
        #  Note that no operator is the same as '+' and '=' is the same as '+'
        #  either.
        is_plus_op = (process_ml.get_operator() == _ce_parser.PARSED_CE_ITEM_OP_PLUS)

        #  If the molecule has electronic, write the its count to specific position.
        if not e_count.is_zero:
            if is_plus_op:
                mtx.write_item_by_position(ref_atom_idx["e"], col_id, e_count)
            else:
                mtx.write_item_by_position(ref_atom_idx["e"], col_id, -e_count)

        #  Get the atom dictionary of the molecule.
        atom_dict = ml_info.get_atom_dictionary()

        for atom in atom_dict:
            #  Write the count of each atom to specific position.
            if is_plus_op:
                mtx.write_item_by_position(ref_atom_idx[atom], col_id, atom_dict[atom])
            else:
                mtx.write_item_by_position(ref_atom_idx[atom], col_id, -atom_dict[atom])

        #  Increase the column counter.
        col_id += 1

    #  Process items on the right side.
    for process_ml in right_mls:
        #  Get molecule information.
        ml_info = process_ml.get_molecule()

        #  Get the electronic count of the molecule.
        e_count = ml_info.get_electronic_count()

        #  Get whether the operator before the molecule is '+' or '=' or nothing.
        #  Note that no operator is the same as '+' and '=' is the same as '+'
        #  either.
        is_plus_op = (process_ml.get_operator() == _ce_parser.PARSED_CE_ITEM_OP_PLUS)

        #  If the molecule has electronic, write the its count to specific position.
        if not e_count.is_zero:
            if is_plus_op:
                mtx.write_item_by_position(ref_atom_idx["e"], col_id, -e_count)
            else:
                mtx.write_item_by_position(ref_atom_idx["e"], col_id, e_count)

        #  Get the atom dictionary of the molecule.
        atom_dict = ml_info.get_atom_dictionary()

        for atom in atom_dict:
            #  Write the count of each atom to specific position.
            if is_plus_op:
                mtx.write_item_by_position(ref_atom_idx[atom], col_id, -atom_dict[atom])
            else:
                mtx.write_item_by_position(ref_atom_idx[atom], col_id, atom_dict[atom])

        #  Increase the column counter.
        col_id += 1

    return mtx