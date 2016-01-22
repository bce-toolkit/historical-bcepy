#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.option as _opt
import bce.math.constant as _math_cst
import bce.decompiler.mexp.to_mathml as _mexp_decompiler
import bce.parser.molecule.ast.base as _ml_ast_base
import bce.parser.molecule.ast.bfs as _ml_ast_bfs
import bce.parser.molecule.status as _ml_status
import bce.utils.mathml.all as _mathml


def _decompile_operand(value, need_wrapping, options):
    """Decompile an operand.

    :type need_wrapping: bool
    :type options: _opt.Option
    :param value: The operand value (must be simplified).
    :param need_wrapping: Set to True if you need to wrap the expression when it is neither an integer nor a symbol.
                          Otherwise, set to False.
    :param options: The BCE options.
    :return: The decompiled DOM node.
    """

    if value.is_Integer:
        return _mathml.NumberComponent(str(value))
    else:
        if need_wrapping and not (value.is_Integer or value.is_Symbol):
            #  Use a pair of parentheses to wrap the decompiled expression.
            r = _mathml.RowComponent()
            r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_LEFT_PARENTHESIS))
            r.append_object(_mexp_decompiler.decompile_mexp(value, options.get_protected_math_symbol_header()))
            r.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_RIGHT_PARENTHESIS))
            return r
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

        #  Decompile the charge part.
        r.append_object(_decompile_operand(charge, True, options))

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
        sfx_dom = _decompile_operand(sfx, False, options)
    else:
        sfx_dom = None

    #  Do combination and return.
    if sfx_dom is None:
        return main_dom
    else:
        return _mathml.SubComponent(main_dom, sfx_dom)


def decompile_ast(root_node, options):
    """Decompile an AST to BCE expression.

    :type root_node: _ml_ast_base.ASTNodeHydrateGroup | _ml_ast_base.ASTNodeMolecule
    :type options: _opt.Option
    :param root_node: The root node of the AST.
    :param options: The BCE options.
    :return: The decompiled expression.
    """

    #  Get the decompile order.
    work_order = _ml_ast_bfs.do_bfs(root_node, True)

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
                build.append_object(_decompile_operand(pfx, True, options))
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
                build.append_object(_decompile_operand(pfx, True, options))

            #  Decompile children nodes.
            for child_id in range(0, len(work_node)):
                build.append_object(decompiled[id(work_node[child_id])])

            el_charge = work_node.get_electronic_count().simplify()
            if not el_charge.is_zero:
                if len(work_node) == 0:
                    build.append_object(_mathml.SuperComponent(_mathml.TextComponent("e"),
                                                               _decompile_super_electronic(
                                                                   el_charge,
                                                                   options)))
                else:
                    #  Find the innermost row component.
                    innermost = build
                    while innermost[-1].is_row():
                        innermost = innermost[-1]

                    #  Fetch the last item.
                    last_item = innermost[-1]

                    #  Add the electronic.
                    if last_item.is_sub():
                        assert isinstance(last_item, _mathml.SubComponent)
                        last_item = _mathml.SubAndSuperComponent(last_item.get_main_object(),
                                                                 last_item.get_sub_object(),
                                                                 _decompile_super_electronic(el_charge, options))
                    else:
                        last_item = _mathml.SuperComponent(last_item,
                                                           _decompile_super_electronic(el_charge, options))

                    #  Save the modified item.
                    innermost[-1] = last_item

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
        elif work_node.is_abbreviation():
            assert isinstance(work_node, _ml_ast_base.ASTNodeAbbreviation)

            #  Decompile and save the result.
            decompiled[id(work_node)] = _decompile_suffix(
                _mathml.TextComponent("[%s]" % work_node.get_abbreviation_symbol()),
                work_node,
                options)
        else:
            raise RuntimeError("Never reach this condition.")

    post_process = decompiled[id(root_node)]
    if root_node.get_status() is not None:
        if not post_process.is_row():
            tmp = _mathml.RowComponent()
            tmp.append_object(post_process)
            post_process = tmp
        post_process.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_LEFT_PARENTHESIS))
        if root_node.get_status() == _ml_status.STATUS_GAS:
            post_process.append_object(_mathml.TextComponent("g"))
        elif root_node.get_status() == _ml_status.STATUS_LIQUID:
            post_process.append_object(_mathml.TextComponent("l"))
        elif root_node.get_status() == _ml_status.STATUS_SOLID:
            post_process.append_object(_mathml.TextComponent("s"))
        elif root_node.get_status() == _ml_status.STATUS_AQUEOUS:
            post_process.append_object(_mathml.TextComponent("aq"))
        else:
            raise RuntimeError("BUG: No such molecule status.")
        post_process.append_object(_mathml.OperatorComponent(_mathml.OPERATOR_RIGHT_PARENTHESIS))

    return decompiled[id(root_node)]