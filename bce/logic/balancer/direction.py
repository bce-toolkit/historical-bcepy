#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.ce.base as _ce_base

GSD_UNDETERMINED = 0
GSD_LEFT_TO_RIGHT = 1
GSD_RIGHT_TO_LEFT = 2


def guess_reaction_direction(ce):
    """Guess the direction of a reaction.

    :type ce: _ce_base.ChemicalEquation
    :param ce: The chemical equation of the reaction.
    :rtype : int
    :return: The direction descriptor (one of GSD_*).
    """

    #  Calculate the sum of the prefix coefficients of gas on the left side.
    gas_left = 0
    for substance_id in range(0, ce.get_left_item_count()):
        substance = ce.get_left_item(substance_id)
        substance_ast = substance.get_molecule_ast()
        if substance_ast.is_gas_status():
            gas_left += substance.get_coefficient() * substance_ast.get_prefix_number()

    #  Calculate the sum of the prefix coefficients of gas on the right side.
    gas_right = 0
    for substance_id in range(0, ce.get_right_item_count()):
        substance = ce.get_right_item(substance_id)
        substance_ast = substance.get_molecule_ast()
        if substance.get_molecule_ast().is_gas_status():
            gas_right += substance.get_coefficient() * substance_ast.get_prefix_number()

    #  Determine.
    if gas_left == gas_right:
        return GSD_UNDETERMINED
    elif gas_left < gas_right:
        return GSD_LEFT_TO_RIGHT
    else:
        return GSD_RIGHT_TO_LEFT
