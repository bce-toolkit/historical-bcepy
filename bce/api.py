#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.decompiler.ce.collect_symbol as _decompiler_ce_csm
import bce.decompiler.ce.to_bce as _decompiler_ce_to_bce
import bce.decompiler.ce.to_mathml as _decompiler_ce_to_mathml
import bce.logic.balancer.checker as _bce_check
import bce.logic.balancer.main as _bce_main
import bce.logic.common.error as _le
import bce.parser.ce.parser as _ce_parser
import bce.parser.ce.substitution as _ce_subst
import bce.parser.ce.token as _ce_token
import bce.parser.common.error as _pe
import bce.utils.input_checker as _input_chk
import bce.option as _opt

DECOMPILER_TEXT = 1
DECOMPILER_MATHML = 2
DECOMPILER_COLLECT_SYMBOLS = 3


class ParserErrorWrapper(Exception):
    """Parser error."""
    pass


class LogicErrorWrapper(Exception):
    """Logic error."""
    pass


class InvalidCharacterException(Exception):
    """Invalid character exception."""
    pass


class SubstitutionErrorWrapper(Exception):
    """Substitution error."""
    pass


def balance_chemical_equation(expression, decompilers, options):
    """Balance a chemical equation.

    :type expression: str
    :type decompilers: list[int]
    :type options: _opt.Option
    :param expression: The chemical equation expression.
    :param decompilers: The list that contains the decompiler IDs.
    :param options: The BCE options.
    :rtype: list
    :return: A list contains the decompiled balancing result.
    """

    #  Check characters.
    if not _input_chk.check_input_expression_characters(expression):
        raise InvalidCharacterException("Invalid character.")

    #  Initialize the result container.
    ret = []

    try:
        #  Parse the chemical equation.
        ce = _ce_parser.parse(expression, _ce_token.tokenize(expression, options), options)

        #  Balance the chemical equation.
        _bce_main.balance_chemical_equation(ce, options)

        #  Decompile.
        for dec_id in decompilers:
            if dec_id == DECOMPILER_TEXT:
                ret.append(_decompiler_ce_to_bce.decompile_ce(ce))
            elif dec_id == DECOMPILER_MATHML:
                ret.append(_decompiler_ce_to_mathml.decompile_ce(ce, options).to_string())
            elif dec_id == DECOMPILER_COLLECT_SYMBOLS:
                ret.append(_decompiler_ce_csm.collect_symbols(ce))
            else:
                raise ValueError("Unsupported decompiler ID.")
    except _pe.Error as err1:
        raise ParserErrorWrapper(err1.to_string())
    except _le.LogicError as err2:
        raise LogicErrorWrapper(err2.to_string())

    return ret


def is_chemical_equation_balanced(expression, options):
    """Check whether a chemical equation is balanced.

    :type expression: str
    :type options: _opt.Option
    :param expression: The chemical equation expression.
    :param options: The BCE options.
    :rtype : bool
    :return: Return True if it is balanced.
    """

    #  Backup the protected math symbol header.
    prot_header = options.get_protected_math_symbol_header()

    #  Fake a protected math symbol header.
    options.set_protected_math_symbol_header("-")

    try:
        #  Parse the chemical equation.
        ce = _ce_parser.parse(expression, _ce_token.tokenize(expression, options), options)

        #  Restore the protected math symbol header.
        options.set_protected_math_symbol_header(prot_header)

        #  Check whether the chemical equation is balanced.
        return _bce_check.check_whether_balanced(ce)
    except _pe.Error as err:
        #  Restore the protected math symbol header.
        options.set_protected_math_symbol_header(prot_header)

        return ParserErrorWrapper(err.to_string())


def substitute_chemical_equation(expression, subst_map, decompilers, options):
    """Substitute a chemical equation.

    :type expression: str
    :type subst_map: dict
    :type decompilers: list[int]
    :type options: _opt.Option
    :param expression: The chemical equation.
    :param subst_map: The substitution map.
    :param decompilers: The list that contains the decompiler IDs.
    :param options: The BCE options.
    :rtype : list
    :return: A list that contains the substitution result.
    """

    #  Save the protected math symbol header.
    prot_symbol = options.get_protected_math_symbol_header()

    #  Fake the header.
    options.set_protected_math_symbol_header("-")

    #  Parse the chemical equation.
    ce = _ce_parser.parse(expression, _ce_token.tokenize(expression, options), options)

    #  Restore the protected math symbol header.
    options.set_protected_math_symbol_header(prot_symbol)

    try:
        #  Do substitution.
        ce = _ce_subst.substitute_ce(ce, subst_map, options)
    except _ce_subst.SubstituteError:
        raise SubstitutionErrorWrapper("Substitute error.")

    #  Initialize the result container.
    ret = []

    #  Decompile.
    for dec_id in decompilers:
        if dec_id == DECOMPILER_TEXT:
            ret.append(_decompiler_ce_to_bce.decompile_ce(ce))
        elif dec_id == DECOMPILER_MATHML:
            ret.append(_decompiler_ce_to_mathml.decompile_ce(ce, options).to_string())
        elif dec_id == DECOMPILER_COLLECT_SYMBOLS:
            ret.append(_decompiler_ce_csm.collect_symbols(ce))
        else:
            raise ValueError("Unsupported decompiler ID.")

    return ret
