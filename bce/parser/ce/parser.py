#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.math.constant as _math_const
import bce.parser.common.error as _pe
import bce.parser.molecule.token as _ml_token
import bce.parser.molecule.parser as _ml_parser
import bce.locale.msg_id as _msg_id

#  Add this for PyCharm auto-hinting.
import bce.option as _opt

#  Item sides.
PARSED_CE_ITEM_SIDE_LEFT = 1
PARSED_CE_ITEM_SIDE_RIGHT = 2

#  Item operators.
PARSED_CE_ITEM_OP_PLUS = 1
PARSED_CE_ITEM_OP_MINUS = 2


class ParsedCEItem:
    """Item class of ParsedCE class."""

    def __init__(self, op, parsed_ml, origin_pfx):
        """Initialize the class with specific operator and the parsed molecule.

        :type op: int
        :type parsed_ml: _ml_parser.MoleculeProperty
        :param op: The operator before the molecule.
        :param parsed_ml: The parsed molecule data.
        :param origin_pfx: The origin prefix data.
        """

        self.__o = op
        self.__m = parsed_ml
        self.__orig_pfx = origin_pfx

    def get_operator(self):
        """Get the operator.

        :rtype : int
        :return: The operator (one of PARSED_CE_ITEM_OP_*).
        """

        return self.__o

    def is_plus_operator(self):
        """Get whether the token is a plus operator token.

        :rtype : bool
        :return: Return True if this token is a plus operator.
        """

        return self.__o == PARSED_CE_ITEM_OP_PLUS

    def is_minus_operator(self):
        """Get whether the token is a minus operator token.

        :rtype : bool
        :return: Return True if this token is a minus operator.
        """

        return self.__o == PARSED_CE_ITEM_OP_MINUS

    def get_molecule(self):
        """Get the parsed molecule.

        :rtype : _ml_parser.MoleculeProperty
        :return: The parsed molecule.
        """

        return self.__m

    def get_origin_prefix(self):
        """Get the origin prefix.

        :return: The origin prefix.
        """

        return self.__orig_pfx


class ParsedCE:
    """Class for containing parsed chemical equation."""

    def __init__(self, left_items, right_items, form):
        """Initialize the class with specific items on left side and right side and the
        form of the chemical equation.

        :type left_items: list
        :type right_items: list
        :type form: int
        :param left_items: Items on left side.
        :param right_items: Items on right side.
        :param form: Form indicator (one of TOKENIZED_CE_FORM_* in bce.parser.ce.token).
        """

        self.__l = left_items
        self.__r = right_items
        self.__f = form

    def get_left_items(self):
        """Get items on left side.

        :rtype : list of ParsedCEItem
        :return: A list contains items on left side.
        """

        return self.__l

    def get_right_items(self):
        """Get items on right side.

        :rtype : list of ParsedCEItem
        :return: A list contains items on right side.
        """

        return self.__r

    def get_form(self):
        """Get the form of the chemical equation.

        :rtype : int
        :return: The form indicator (one of TOKENIZED_CE_FORM_* in bce.parser.ce.token).
        """

        return self.__f


def parse(expression, tokenized_ce, options):
    """Parse the tokenized chemical equation.

    :type expression: str
    :type tokenized_ce: _ml_token.TokenizedCE
    :type options: _opt.Option
    :param expression: Origin chemical equation.
    :param tokenized_ce: The tokenized chemical equation.
    :param options: The BCE options.
    :rtype : ParsedCE
    :return: The parsed chemical equation.
    :raise RuntimeError: When a bug appears.
    """

    #  Initialize.
    cur_side = PARSED_CE_ITEM_SIDE_LEFT
    cur_op = PARSED_CE_ITEM_OP_PLUS
    r_left = []
    r_right = []
    token_list = tokenized_ce.get_token_list()

    for token in token_list:
        if token.is_equal():
            #  Set current side to right side.
            cur_side = PARSED_CE_ITEM_SIDE_RIGHT
            cur_op = PARSED_CE_ITEM_OP_PLUS
            continue

        if token.is_operator_plus() or token.is_operator_separator():
            #  Set current operator to plus operator.
            cur_op = PARSED_CE_ITEM_OP_PLUS
            continue

        if token.is_operator_minus():
            #  Set current operator to minus operator.
            cur_op = PARSED_CE_ITEM_OP_MINUS
            continue

        if token.is_molecule():
            #  Get molecule expression.
            ml_symbol = token.get_symbol()

            try:
                #  Tokenize.
                ml_tokenized = _ml_token.tokenize(ml_symbol, options)

                #  Parse the molecule.
                ml_parsed = _ml_parser.parse(ml_symbol, ml_tokenized, options)

                #  Get its prefix.
                ml_prefix = ml_parsed.get_prefix()

                #  If it's not a hydrate molecule and it has a prefix, remove the prefix.
                if (not ml_parsed.is_hydrate()) and ml_prefix != _math_const.ONE:
                    #  Divide the count of each atom by the prefix.
                    ml_parsed.divide_common_factor(ml_prefix)

                    #  Set the prefix to 1.
                    ml_parsed.set_prefix(_math_const.ONE)

                    #  Remove the prefix token.
                    ml_parsed.set_token_list(ml_parsed.get_token_list()[1:])

                    #  Simplify.
                    ml_parsed.simplify_atoms()

                #  Create a new item.
                new_item = ParsedCEItem(cur_op, ml_parsed, ml_prefix)

                #  Append the item to the list of its side.
                if cur_side == PARSED_CE_ITEM_SIDE_LEFT:
                    r_left.append(new_item)
                else:
                    r_right.append(new_item)
            except _pe.Error as err:
                #  Add note about where the error raised from.
                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position() + len(ml_symbol) - 1,
                                      _msg_id.MSG_PE_CE_SUB_ML_ERROR_TRACE_MESSAGE)

                #  Re-raise the error.
                raise err

            continue

        #  We should never reach this condition.
        raise RuntimeError("Unreachable condition (invalid token type).")

    return ParsedCE(r_left, r_right, tokenized_ce.get_form())