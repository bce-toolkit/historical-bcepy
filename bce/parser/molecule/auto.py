#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.math.constant as _math_cst
import bce.parser.molecule.ast_generator as _ml_ast_gen
import bce.parser.molecule.ast_base as _ml_ast_base
import bce.parser.molecule.ast_parser as _ml_parser
import bce.parser.molecule.token as _ml_token
import bce.option as _opt


def tokenize_and_parse_molecule(expression, remove_prefix, options):
    """Tokenize and parse specified molecule expression.

    :type expression: str
    :type remove_prefix: bool
    :type options: _opt.Option
    :param expression: The molecule expression.
    :param remove_prefix: Set to True if you want to remove the prefix number. Otherwise, set to False.
    :param options: The BCE options.
    :rtype : _ml_parser.ResultContainer
    :return: The parsing result.
    """

    #  Tokenize.
    token_list = _ml_token.tokenize(expression, options)

    #  Generate the AST.
    ast_root = _ml_ast_gen.generate_ast_from_token_list(expression, token_list, options)

    #  Remove the prefix if specified.
    if remove_prefix:
        assert isinstance(ast_root, _ml_ast_base.ASTNodeHydrateGroup) or \
               isinstance(ast_root, _ml_ast_base.ASTNodeMolecule)
        ast_root.set_prefix_number(_math_cst.ONE)

    #  Parse and return.
    return _ml_parser.parse_ast(expression, ast_root, options)