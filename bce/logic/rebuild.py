#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.common.token as _base_token
import bce.math.constant as _math_const
import bce.parser.ce.parser as _ce_parser
import bce.parser.mexp.reprint as _mexp_repr

#  Add this for PyCharm auto-hinting.
import bce.logic.arrange as _logic_arrange


def rebuild_ce(combined_result):
    """Rebuild the combined balanced result to a human-readable form (string).

    :type combined_result: _logic_arrange.CombinedResult
    :param combined_result: The combined result.
    :rtype : str
    :return: The rebuilt result.
    """

    #  Initialize an empty CE expression.
    r = ""

    #  Cache items on left and right side.
    li = combined_result.get_left_items()
    ri = combined_result.get_right_items()

    #  Process items on left side.
    for item in li:
        #  Insert operator.
        if item.get_operator() == _ce_parser.PARSED_CE_ITEM_OP_PLUS:
            if len(r) != 0:
                r += "+"

        if item.get_operator() == _ce_parser.PARSED_CE_ITEM_OP_MINUS:
            r += "-"

        #  Get the coefficient.
        coeff = item.get_coefficient()

        #  Initialize molecule wrapping flag.
        wrap_molecule = False

        #  Insert coefficient.
        if coeff != _math_const.ONE:
            if len(coeff.free_symbols) == 0:
                r += str(coeff)

                #  Wrap the molecule if the molecule is hydrate.
                if item.is_hydrate_molecule():
                    wrap_molecule = True
            else:
                r += "{" + _mexp_repr.reprint_mexp(coeff) + "}"

        #  Insert molecule symbol.
        if wrap_molecule:
            r += "(%s)" % _base_token.untokenize(item.get_molecule_token_list())
        else:
            r += _base_token.untokenize(item.get_molecule_token_list())

    #  Insert '='.
    r += "="

    #  Mark whether processing molecule is the first molecule on right side.
    r_is_first = True

    #  Process items on right side.
    for item in ri:
        #  Insert operator.
        if item.get_operator() == _ce_parser.PARSED_CE_ITEM_OP_PLUS:
            if not r_is_first:
                r += "+"

        if item.get_operator() == _ce_parser.PARSED_CE_ITEM_OP_MINUS:
            r += "-"

        #  Get the coefficient.
        coeff = item.get_coefficient()

        #  Initialize molecule wrapping flag.
        wrap_molecule = False

        #  Insert coefficient.
        if coeff != _math_const.ONE:
            if len(coeff.free_symbols) == 0:
                r += str(coeff)

                #  Wrap the molecule if the molecule is hydrate.
                if item.is_hydrate_molecule():
                    wrap_molecule = True
            else:
                r += "{" + _mexp_repr.reprint_mexp(coeff) + "}"

        #  Insert molecule symbol.
        if wrap_molecule:
            r += "(%s)" % _base_token.untokenize(item.get_molecule_token_list())
        else:
            r += _base_token.untokenize(item.get_molecule_token_list())

        #  Switch off the mark.
        r_is_first = False

    return r