#!/usr/bin/env python
#
#  Copyright 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.option as _opt
import bce.math.constant as _math_cst
import bce.parser.mexp.decompiler.to_mathml as _mexp_decompiler
import bce.parser.molecule.ast_base as _ml_ast_base
import bce.parser.molecule.ast_utils as _ml_ast_utils
import bce.parser.molecule.status as _ml_status
import bce.utils.mathml.all as _mathml


def _decompile_operand(value, options):
    """Decompile an operand.

    :type options: _opt.Option
    :param value: The operand value.
    :param options: The BCE options.
    :return: The decompiled DOM node.
    """

    #  WARN: $value must be simplified.
    if value.is_Integer:
        return _mathml.NumberComponent(str(value))
    else:
        return _mexp_decompiler.decompile_mexp(value, options.get_protected_math_symbol_header())


def _decompile_super_electronic(charge, options):
    """Decompile electronic charge value.

    :type options: _opt.Option
    :param charge: The charge number (must be simplified).
    :param options: The BCE options.
    :return: The decompiled DOM node.
    """

    #  Decompile the positivity part.
    if charge.is_negative:
        charge = -charge
        positivity = _mathml.OperatorComponent(_mathml.OPERATOR_MINUS)
    else:
        positivity = _mathml.OperatorComponent(_mathml.OPERATOR_PLUS)

    if charge == _math_cst.ONE:
        return positivity
    else:
        #  Initialize a row component to contain the decompiling result.
        r = _mathml.RowComponent()

        #  Get whether we need surrounding parentheses.
        surround = not (charge.is_Integer or charge.is_Symbol)

        #  Add left parenthesis if the flag was marked.
        if surround:
            r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_LEFT_PARENTHESIS))

        #  Decompile the charge part.
        r.append_object(_decompile_operand(charge, options))

        #  Add right parenthesis if the flag was marked.
        if surround:
            r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_RIGHT_PARENTHESIS))

        #  Add the positivity flag.
        r.append_object(positivity)

        return r


def _decompile_suffix(main_dom, node, options):
    """Decompile suffix part of specified node.

    :type node: _ml_ast_base._ASTNodeWithSuffix
    :type options: _opt.Option
    :param main_dom: The main DOM node.
    :param node: The AST node.
    :param options: The BCE options.
    :return: The decompiled DOM node.
    """

    #  Decompile the suffix number part.
    sfx = node.get_suffix_number().simplify()
    if sfx != _math_cst.ONE:
        sfx_dom = _decompile_operand(sfx, options)
    else:
        sfx_dom = None

    #  Decompile the electronic part.
    charge = node.get_suffix_electronic().simplify()
    if not charge.is_zero:
        chg_dom = _decompile_super_electronic(charge, options)
    else:
        chg_dom = None

    #  Do combination and return.
    if sfx_dom is None and chg_dom is None:
        return main_dom
    elif sfx_dom is None and chg_dom is not None:
        return _mathml.SuperComponent(main_dom, chg_dom)
    elif sfx_dom is not None and chg_dom is None:
        return _mathml.SubComponent(main_dom, sfx_dom)
    else:
        return _mathml.SubAndSuperComponent(main_dom, sfx_dom, chg_dom)


def decompile_ast(root_node, options):
    """Decompile an AST to BCE expression.

    :type root_node: _ml_ast_base._ASTNodeBaseML
    :type options: _opt.Option
    :param root_node: The root node of the AST.
    :param options: The BCE options.
    :return: The decompiled expression.
    """

    #  Get the decompile order.
    work_order = _ml_ast_utils.do_bfs(root_node, True)

    #  Initialize the decompiling result container.
    decompiled = {}

    for work_node in work_order:
        if work_node.is_hydrate_group():
            assert isinstance(work_node, _ml_ast_base.ASTNodeHydrateGroup)

            #  Initialize a row component to contain the decompiling result.
            build = _mathml.RowComponent()

            #  Decompile the prefix number part.
            pfx = work_node.get_prefix_number().simplify()
            if pfx != _math_cst.ONE:
                build.append_object(_decompile_operand(pfx, options))
                build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_LEFT_PARENTHESIS))
                surround = True
            else:
                surround = False

            #  Decompile children nodes.
            build.append_object(decompiled[id(work_node[0])])
            for child_id in range(1, len(work_node)):
                build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_DOT))
                build.append_object(decompiled[id(work_node[child_id])])

            #  Complete the surrounding parentheses if the flag was marked.
            if surround:
                build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_RIGHT_PARENTHESIS))

            #  Save decompiling result.
            decompiled[id(work_node)] = build
        elif work_node.is_molecule():
            assert isinstance(work_node, _ml_ast_base.ASTNodeMolecule)

            #  Initialize a row component to contain the decompiling result.
            build = _mathml.RowComponent()

            #  Decompile the prefix number part.
            pfx = work_node.get_prefix_number().simplify()
            if pfx != _math_cst.ONE:
                build.append_object(_decompile_operand(pfx, options))

            #  Decompile children nodes.
            for child_id in range(0, len(work_node)):
                build.append_object(decompiled[id(work_node[child_id])])

            status = work_node.get_status()
            if status == _ml_status.STATUS_GAS:
                build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_LEFT_PARENTHESIS))
                build.append_object(_mathml.TextComponent("g"))
                build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_RIGHT_PARENTHESIS))
            elif status == _ml_status.STATUS_LIQUID:
                build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_LEFT_PARENTHESIS))
                build.append_object(_mathml.TextComponent("l"))
                build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_RIGHT_PARENTHESIS))
            elif status == _ml_status.STATUS_SOLID:
                build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_LEFT_PARENTHESIS))
                build.append_object(_mathml.TextComponent("s"))
                build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_RIGHT_PARENTHESIS))
            elif status == _ml_status.STATUS_AQUEOUS:
                build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_LEFT_PARENTHESIS))
                build.append_object(_mathml.TextComponent("aq"))
                build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_RIGHT_PARENTHESIS))
            else:
                pass

            #  Save decompiling result.
            decompiled[id(work_node)] = build
        elif work_node.is_atom():
            assert isinstance(work_node, _ml_ast_base.ASTNodeAtom)

            #  Decompile and save the result.
            decompiled[id(work_node)] = _decompile_suffix(_mathml.TextComponent(work_node.get_atom_symbol()),
                                                          work_node,
                                                          options)
        elif work_node.is_parenthesis():
            assert isinstance(work_node, _ml_ast_base.ASTNodeParenthesisWrapper)

            #  Initialize a row component to contain the decompiling result.
            build = _mathml.RowComponent()

            #  Decompile.
            build.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_LEFT_PARENTHESIS))
            build.append_object(decompiled[id(work_node.get_inner_node())])
            build.append_object(_decompile_suffix(_mathml.OperatorComponent(_mathml.OPERATOR_RIGHT_PARENTHESIS),
                                                  work_node,
                                                  options))

            #  Save decompiling result.
            decompiled[id(work_node)] = build
        elif work_node.is_electronic():
            assert isinstance(work_node, _ml_ast_base.ASTNodeElectronic)

            #  Decompile and save the result.
            decompiled[id(work_node)] = _mathml.SuperComponent(_mathml.TextComponent("e"),
                                                               _decompile_super_electronic(
                                                                   work_node.get_electronic_count().simplify(),
                                                                   options))
        elif work_node.is_abbreviation():
            assert isinstance(work_node, _ml_ast_base.ASTNodeAbbreviation)

            #  Decompile and save the result.
            decompiled[id(work_node)] = _decompile_suffix(
                _mathml.TextComponent("[%s]" % work_node.get_abbreviation_symbol()),
                work_node,
                options)
        else:
            raise RuntimeError("Never reach this condition.")

    return decompiled[id(root_node)]