#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.math.constant as _math_cst
import bce.decompiler.mexp.to_bce as _mexp_decompiler
import bce.parser.molecule.ast.base as _ml_ast_base
import bce.parser.molecule.ast.bfs as _ml_ast_bfs
import bce.parser.molecule.status as _ml_status


def _decompile_operand(operand_value):
    """Decompile an operand.

    :param operand_value: The value of the operand (must be simplified).
    :rtype : str
    :return: The decompiled expression.
    """

    if operand_value.is_Integer:
        if operand_value == _math_cst.ONE:
            return ""
        else:
            return str(operand_value)
    else:
        return "{%s}" % _mexp_decompiler.decompile_mexp(operand_value)


def _decompile_electronic(charge):
    """Decompile an electronic charge value.

    :param charge: The charge value (must be simplified).
    :rtype : str
    :return: The decompiled expression.
    """

    #  Decompile the positivity part.
    if charge.is_negative:
        charge = -charge
        positivity = "e-"
    else:
        positivity = "e+"

    #  Decompile the charge part and do combination.
    return "<%s%s>" % (_decompile_operand(charge), positivity)


def _decompile_suffix(node):
    """Decompile the suffix part of specified node.

    :type node: _ml_ast_base._ASTNodeWithSuffix
    :param node: The node to be decompiled.
    :rtype : str
    :return: The decompiled expression.
    """

    #  Initialize the result.
    ret = ""

    #  Decompile the suffix number part if has.
    sfx = node.get_suffix_number().simplify()
    if not sfx.is_zero:
        ret += _decompile_operand(sfx)

    return ret


def decompile_ast(root_node):
    """Decompile an AST to BCE expression.

    :type root_node: _ml_ast_base.ASTNodeHydrateGroup | _ml_ast_base.ASTNodeMolecule
    :param root_node: The root node of the AST.
    :rtype : str
    :return: The decompiled expression.
    """

    #  Get the decompile order.
    work_order = _ml_ast_bfs.do_bfs(root_node, True)

    #  Initialize the decompiling result container.
    decompiled = {}

    for work_node in work_order:
        if work_node.is_hydrate_group():
            assert isinstance(work_node, _ml_ast_base.ASTNodeHydrateGroup)

            #  Decompile the prefix number part.
            pfx = work_node.get_prefix_number().simplify()
            if pfx != _math_cst.ONE:
                model = _decompile_operand(pfx) + "(%s)"
            else:
                model = "%s"

            #  Decompile children nodes.
            inner = decompiled[id(work_node[0])]
            for child_id in range(1, len(work_node)):
                inner += "." + decompiled[id(work_node[child_id])]

            #  Save decompiling result.
            decompiled[id(work_node)] = model % inner
        elif work_node.is_molecule():
            assert isinstance(work_node, _ml_ast_base.ASTNodeMolecule)

            #  Decompile the prefix number part.
            pfx = work_node.get_prefix_number().simplify()
            build = _decompile_operand(pfx)

            #  Decompile children nodes.
            for child_id in range(0, len(work_node)):
                build += decompiled[id(work_node[child_id])]

            #  Decompile the electronic part.
            el_charge = work_node.get_electronic_count().simplify()
            if not el_charge.is_zero:
                build += _decompile_electronic(el_charge)

            #  Save decompiling result.
            decompiled[id(work_node)] = build
        elif work_node.is_atom():
            assert isinstance(work_node, _ml_ast_base.ASTNodeAtom)

            #  Decompile and save the result.
            decompiled[id(work_node)] = work_node.get_atom_symbol() + _decompile_suffix(work_node)
        elif work_node.is_parenthesis():
            assert isinstance(work_node, _ml_ast_base.ASTNodeParenthesisWrapper)

            #  Decompile and save the result.
            decompiled[id(work_node)] = "(%s)%s" % (decompiled[id(work_node.get_inner_node())],
                                                    _decompile_suffix(work_node))
        elif work_node.is_abbreviation():
            assert isinstance(work_node, _ml_ast_base.ASTNodeAbbreviation)

            #  Decompile and save the result.
            decompiled[id(work_node)] = "[%s]%s" % (work_node.get_abbreviation_symbol(), _decompile_suffix(work_node))
        else:
            raise RuntimeError("Never reach this condition.")

    #  Post process.
    post_process = decompiled[id(root_node)]
    if root_node.get_status() == _ml_status.STATUS_GAS:
        post_process += "(g)"
    elif root_node.get_status() == _ml_status.STATUS_LIQUID:
        post_process += "(l)"
    elif root_node.get_status() == _ml_status.STATUS_SOLID:
        post_process += "(s)"
    elif root_node.get_status() == _ml_status.STATUS_AQUEOUS:
        post_process += "(aq)"
    else:
        pass

    return post_process