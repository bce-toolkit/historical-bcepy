#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.ce.base as _ce_base


def _collect_mexp_symbols(value):
    """Get symbols in a math expression.

    :param value: The math expression.
    :rtype : list of str
    :return: A list of symbols.
    """

    #  Get symbols.
    fsm = value.free_symbols

    #  Initialize symbol list.
    ret = []

    #  Pop symbols.
    while len(fsm) != 0:
        ret.append(fsm.pop().name)

    return ret


def collect_symbols(ce):
    """Collect all symbols in a chemical equation.

    :type ce: _ce_base.ChemicalEquation
    :param ce: The chemical equation.
    :rtype : list[str]
    :return: A list that contains all symbols.
    """

    #  Initialize.
    ret = []
    flag = {}

    #  Process left items.
    for idx in range(0, ce.get_left_item_count()):
        #  Get the item.
        item = ce.get_left_item(idx)

        #  Collect symbols.
        fsm_list = _collect_mexp_symbols(item.get_coefficient().simplify())

        #  Merge.
        for fsm_item in fsm_list:
            if fsm_item not in flag:
                flag[fsm_item] = True
                ret.append(fsm_item)

    #  Process right items.
    for idx in range(0, ce.get_right_item_count()):
        #  Get the item.
        item = ce.get_right_item(idx)

        #  Collect symbols.
        fsm_list = _collect_mexp_symbols(item.get_coefficient().simplify())

        #  Merge.
        for fsm_item in fsm_list:
            if fsm_item not in flag:
                flag[fsm_item] = True
                ret.append(fsm_item)

    return ret