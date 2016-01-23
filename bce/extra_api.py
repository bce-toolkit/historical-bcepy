#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#


import bce.decompiler.mexp.to_bce as _decompiler_mexp_to_bce
import bce.decompiler.mexp.to_mathml as _decompiler_mexp_to_mathml
import bce.parser.common.error as _pe
import bce.parser.mexp.evaluate as _mexp_ev
import bce.parser.molecule.token as _ml_token
import bce.parser.molecule.ast.generator as _ml_ast_gen
import bce.parser.molecule.ast.parser as _ml_ast_parser
import bce.api as _api
import bce.option as _opt


def decompile_mexp(value, decompilers, options):
    """Decompile a math expression.

    :type decompilers: list[int]
    :type options: _opt.Option
    :param value: The math expression.
    :param decompilers:  A list that contains the decompiler IDs.
    :param options: The BCE options.
    :rtype : list[str]
    :return: A list that contains the decompiling result.
    """

    #  Initialize.
    ret = []

    #  Decompile.
    for dec_id in decompilers:
        if dec_id == _api.DECOMPILER_TEXT:
            ret.append(_decompiler_mexp_to_bce.decompile_mexp(value))
        elif dec_id == _api.DECOMPILER_MATHML:
            ret.append(_decompiler_mexp_to_mathml.decompile_mexp(
                value,
                options.get_protected_math_symbol_header()
            ).to_string())
        else:
            raise ValueError("Unsupported decompiler ID.")

    return ret


def parse_molecule(expression, options):
    """Parse a molecule.

    :type expression: str
    :type options: _opt.Option
    :param expression: The molecule expression.
    :param options: The BCE options.
    :rtype: dict
    :return: The atoms dictionary.
    """

    #  Save the protected math symbol header.
    prot_header = options.get_protected_math_symbol_header()

    #  Fake the header.
    options.set_protected_math_symbol_header("-")

    try:
        #  Tokenize.
        token_list = _ml_token.tokenize(expression, options)

        #  Generate the AST.
        ast = _ml_ast_gen.generate_ast(expression, token_list, options)

        #  Parse.
        parsed = _ml_ast_parser.parse_ast(expression, ast, options)

        #  Restore the protected math symbol header.
        options.set_protected_math_symbol_header(prot_header)

        return parsed
    except _pe.Error as err:
        #  Restore the protected math symbol header.
        options.set_protected_math_symbol_header(prot_header)

        raise _api.ParserErrorWrapper(err.to_string())


def evaluate_math_expression(expression, options):
    """Parse and evaluate a math expression.

    :type expression: str
    :type options: _opt.Option
    :param expression: The math expression.
    :param options: The BCE options.
    :return: The evaluated value.
    """

    try:
        value = _mexp_ev.evaluate_math_expression(expression, options)
    except _pe.Error as err:
        raise _api.ParserErrorWrapper(err.to_string())

    return value
