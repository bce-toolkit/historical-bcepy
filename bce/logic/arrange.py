#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.math.equation as _math_equ
import bce.math.constant as _math_const
import bce.locale.msg_id as _msg_id
import bce.logic.error as _le
import bce.parser.common.token as _base_token
import bce.parser.ce.token as _ce_token
import sympy as _sympy
import copy

#  Add this for PyCharm auto-hinting.
import bce.parser.ce.parser as _ce_parser
import bce.parser.molecule.token as _ml_token
import bce.option as _opt


class CombinedResultItem:
    """Item class of class CombinedResult."""

    def __init__(self, molecule_token_list, operator, coeff, molecule_is_hydrate):
        """Initialize the result item.

        :type molecule_token_list: list
        :type operator: int
        :type molecule_is_hydrate: bool
        :param molecule_token_list: The token list of the molecule.
        :param operator: The connection operator.
        :param coeff: The coefficient number.
        :param molecule_is_hydrate: Whether the molecule is a hydrate.
        """

        self.__m = molecule_token_list
        self.__o = operator
        self.__c = coeff
        self.__h = molecule_is_hydrate

    def get_molecule_token_list(self):
        """Get the token list of the molecule.

        :rtype : list of _ml_token.Token
        :return: The token list.
        """

        return self.__m

    def get_operator(self):
        """Get the ID of the connection operator.

        :rtype : int
        :return: The operator ID.
        """

        return self.__o

    def get_coefficient(self):
        """Get the coefficient number.

        :return: The coefficient number.
        """

        return self.__c

    def is_hydrate_molecule(self):
        """Get whether the molecule is hydrate.

        :rtype : bool
        :return: Return True if the molecule is hydrate.
        """

        return self.__h


class CombinedResult:
    """A class that contains the result combined the balanced coefficient and origin
    molecule."""

    def __init__(self, left_items, right_items):
        """Initialize the class with specific left and right items.

        :type left_items: list of [CombinedResultItem]
        :type right_items: list of [CombinedResultItem]
        :param left_items: A list contains all items on the left side.
        :param right_items: A list contains all items on the right side.
        """

        self.__li = left_items
        self.__ri = right_items

    def get_left_items(self):
        """Get the list that contains all items on the left side.

        :rtype : list of CombinedResultItem
        :return: The list.
        """

        return self.__li

    def get_right_items(self):
        """Get the list that contains all items on the right side.

        :rtype : list of CombinedResultItem
        :return: The list.
        """

        return self.__ri


def sort_out_results(result, ce_form, options):
    """Do equivalent transformation to integerize the balanced efficients.

    :type result: _math_equ.SolvedEquation
    :type ce_form: int
    :type options: _opt.Option
    :param result: Answer list returned by the solve_equation() routine.
    :param ce_form: The form of the chemical equation.
    :param options: The BCE options.
    :rtype : list
    :return: The processed answer list.
    """

    #  Get the answer list and the count of unknowns in the answer list.
    unk_count = result.get_unknown_count()
    origin_ans = result.get_answer_list()

    #  Initialize new answer list.
    new_ans = []

    #  If there's only one unknown in the answer list, replace it with 1.
    if unk_count == 1:
        origin_sym = _sympy.Symbol(_math_equ.unknown_id_to_symbol(0, options.get_protected_math_symbol_header()))
        for ans in origin_ans:
            new_ans.append(ans.subs({origin_sym: _math_const.ONE}))
    else:
        if ce_form == _ce_token.TOKENIZED_CE_FORM_AUTO_SIDING:
            raise _le.LogicError(_le.LE_MULTIPLE_ANSWER,
                                 _msg_id.MSG_LE_ARRANGER_MULTI_ANSWER,
                                 options)

        new_ans = copy.copy(origin_ans)

    #  Initialize the least common multiple of all numeric denominators.
    denominator_lcm = _math_const.ONE

    for ans_id in range(0, len(new_ans)):
        #  Simplify origin answer.
        val = new_ans[ans_id].simplify()

        #  Get the denominator.
        nd = val.as_numer_denom()
        nd_denominator = nd[1]

        if nd_denominator.is_number:
            #  Calculate the LCM.
            denominator_lcm = _sympy.lcm(denominator_lcm, nd_denominator)

        #  Write new answer.
        new_ans[ans_id] = val

    #  Multiply all items in the answer list by |denominator_lcm|.
    for ans_id in range(0, len(new_ans)):
        new_ans[ans_id] *= denominator_lcm

    return new_ans


def combine_result(parsed_ce, sorted_result, options):
    """Combine balanced coefficients with parsed chemical equation / expression information.

    :type parsed_ce: _ce_parser.ParsedCE
    :type sorted_result: list
    :type options: _opt.Option
    :param parsed_ce: The parsed chemical equation / expression information.
    :param sorted_result: Result returned by sort_out_results() routine.
    :param options: BCE options.
    :rtype : CombinedResult
    :return: The combined result (presents with CombinedResult class).
    :raise _le.LogicError: Raise if we meet logic errors.
    """

    #  Initialize.
    left_items = []
    right_items = []

    #  Cache required values.
    auto_correct_enabled = options.is_auto_correct_enabled()
    pd_l = parsed_ce.get_left_items()
    pd_r = parsed_ce.get_right_items()

    #  Initialize result list iterator.
    result_id = 0

    #  Process items on left side.
    for pd_item in pd_l:
        #  Get the coefficient.
        coeff = sorted_result[result_id]

        if not coeff.is_zero:
            #  Get molecule information.
            ml_info = pd_item.get_molecule()

            #  If the coefficient is a negative number, it should be moved to the right side.
            if coeff.is_negative:
                #  Raise an error if the form of the CE is normal and the auto-correct function
                #  is disabled.
                if parsed_ce.get_form() == _ce_token.TOKENIZED_CE_FORM_NORMAL and \
                        not auto_correct_enabled:
                    ml_symbol = _base_token.untokenize(ml_info.get_token_list())
                    raise _le.LogicError(_le.LE_WRONG_SIDE,
                                         _msg_id.MSG_LE_WRONG_SIDE,
                                         options,
                                         {"$1": ml_symbol})

                right_items.append(CombinedResultItem(ml_info.get_token_list(),
                                                      pd_item.get_operator(),
                                                      -coeff,
                                                      ml_info.is_hydrate()))
            else:
                left_items.append(CombinedResultItem(ml_info.get_token_list(),
                                                     pd_item.get_operator(),
                                                     coeff,
                                                     ml_info.is_hydrate()))
        else:
            #  Remove the molecule if its coefficient is zero.
            #  Raise an error if the auto-correct function is disabled.
            if not auto_correct_enabled:
                raise _le.LogicError(_le.LE_ZERO_COEFFICIENT,
                                     _msg_id.MSG_LE_ARRANGER_ZERO_COEFFICIENT,
                                     options,
                                     {"$1": _base_token.untokenize(pd_item.get_molecule().get_token_list())})

        #  Increase the iterator.
        result_id += 1

    #  Process items on right side.
    for pd_item in pd_r:
        #  Get the coefficient.
        coeff = sorted_result[result_id]

        if not coeff.is_zero:
            #  Get molecule information.
            ml_info = pd_item.get_molecule()

            #  If the coefficient is a negative number, it should be moved to the left side.
            if coeff.is_negative:
                if parsed_ce.get_form() == _ce_token.TOKENIZED_CE_FORM_NORMAL and not auto_correct_enabled:
                    raise _le.LogicError(_le.LE_WRONG_SIDE,
                                         _msg_id.MSG_LE_WRONG_SIDE,
                                         options,
                                         {"$1": _base_token.untokenize(ml_info.get_token_list())})

                left_items.append(CombinedResultItem(ml_info.get_token_list(),
                                                     pd_item.get_operator(),
                                                     -coeff,
                                                     ml_info.is_hydrate()))
            else:
                right_items.append(CombinedResultItem(ml_info.get_token_list(),
                                                      pd_item.get_operator(),
                                                      coeff,
                                                      ml_info.is_hydrate()))
        else:
            #  Remove the molecule if its coefficient is zero.
            #  Raise an error if the auto-correct function is disabled.
            if not auto_correct_enabled:
                raise _le.LogicError(_le.LE_ZERO_COEFFICIENT,
                                     _msg_id.MSG_LE_ARRANGER_ZERO_COEFFICIENT,
                                     options,
                                     {"$1": _base_token.untokenize(pd_item.get_molecule().get_token_list())})

        #  Increase the iterator.
        result_id += 1

    #  Raise an error if all items have been eliminated.
    if len(left_items) == 0 and len(right_items) == 0:
        raise _le.LogicError(_le.LE_SIDE_ELIMINATED,
                             _msg_id.MSG_LE_SIDE_ELIMINATED_ALL,
                             options)

    #  Raise an error if there's no item on left side.
    if len(left_items) == 0:
        raise _le.LogicError(_le.LE_SIDE_ELIMINATED,
                             _msg_id.MSG_LE_SIDE_ELIMINATED_LEFT,
                             options)

    #  Raise an error if there's no item on the right side.
    if len(right_items) == 0:
        raise _le.LogicError(_le.LE_SIDE_ELIMINATED,
                             _msg_id.MSG_LE_SIDE_ELIMINATED_RIGHT,
                             options)

    return CombinedResult(left_items, right_items)
