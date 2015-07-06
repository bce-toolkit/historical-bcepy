#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.molecule.ast_base as _ast_base
import bce.parser.molecule.ast_utils as _ast_utils


def substitute_ast(root_node, subst_map):
    """Substitution an AST and save the substituted one to a new AST.

    :type root_node: _ast_base._ASTNodeBaseML
    :type subst_map: dict
    :param root_node: The root node of the origin AST.
    :param subst_map: The substitution map.
    :rtype : _ast_base._ASTNodeBaseML | None
    :return: The root node of the new AST.
    """

    #  Get the substitution order.
    work_order = _ast_utils.do_bfs(root_node, True)

    #  Initialize the substituted node container.
    substituted = {}
    """:type : dict[int, _ast_base._ASTNodeBaseML | None]"""

    for work_node in work_order:
        if work_node.is_hydrate_group() or work_node.is_molecule():
            assert isinstance(work_node, _ast_base.ASTNodeHydrateGroup) or \
                   isinstance(work_node, _ast_base.ASTNodeMolecule)

            #  Get and substitute the prefix number.
            pfx = work_node.get_prefix_number().subs(subst_map).simplify()

            #  If the prefix equals to 0, remove the node.
            if pfx.is_zero:
                substituted[id(work_node)] = None
                continue

            #  Create a new node.
            if work_node.is_molecule():
                build = _ast_base.ASTNodeMolecule()
                build.set_status(work_node.get_status())
            else:
                build = _ast_base.ASTNodeHydrateGroup()

            #  Save the substituted prefix number.
            build.set_prefix_number(pfx)

            #  Iterate all children.
            for child_id in range(0, len(work_node)):
                #  Get the child node.
                child = substituted[id(work_node[child_id])]

                #  Add the child to the new created node if the child hasn't been removed.
                if child is not None:
                    child.set_parent_node(build)
                    build.append_child(child)

            #  Remove the node if there is nothing in the new created node.
            if len(build) == 0:
                substituted[id(work_node)] = None
            else:
                #  Save the substituted node.
                substituted[id(work_node)] = build
        elif work_node.is_atom():
            assert isinstance(work_node, _ast_base.ASTNodeAtom)

            #  Create a new node.
            build = _ast_base.ASTNodeAtom(work_node.get_atom_symbol())
            build.set_suffix_electronic(work_node.get_suffix_electronic().subs(subst_map).simplify())

            #  Get and substitute the suffix number.
            sfx = work_node.get_suffix_number().subs(subst_map).simplify()

            #  Remove the atom if the suffix number equals to 0.
            if sfx.is_zero:
                substituted[id(work_node)] = None
            else:
                #  Save the substituted suffix number.
                build.set_suffix_number(sfx)

                #  Save the substituted node.
                substituted[id(work_node)] = build
        elif work_node.is_parenthesis():
            assert isinstance(work_node, _ast_base.ASTNodeParenthesisWrapper)

            #  Get and substitute the suffix number.
            sfx = work_node.get_suffix_number().subs(subst_map).simplify()

            #  Remove the atom if the suffix number equals to 0.
            if sfx.is_zero:
                substituted[id(work_node)] = None
                continue

            #  Get and substitute the electronic charge number.
            charge = work_node.get_suffix_electronic().subs(subst_map).simplify()

            #  Get the substituted inner node.
            inner = substituted[id(work_node.get_inner_node())]
            if inner is None:
                if not charge.is_zero:
                    #  If the inner has been removed and the charge is not zero, move the electronic charge
                    #  inside the parenthesis node.

                    #  Create a new molecule node to contain the electronic node.
                    wrapper = _ast_base.ASTNodeMolecule()

                    #  Create the electronic node.
                    inner = _ast_base.ASTNodeElectronic(charge)

                    #  Link.
                    wrapper.append_child(inner)
                    inner.set_parent_node(wrapper)

                    #  Create a new parenthesis wrapper node.
                    build = _ast_base.ASTNodeParenthesisWrapper(wrapper)

                    #  Link.
                    wrapper.set_parent_node(build)

                    #  Save the suffix number.
                    build.set_suffix_number(sfx)

                    #  Save the substituted node.
                    substituted[id(work_node)] = build
                else:
                    #  The node should be removed when there is nothing inside and the charge equals to 0.
                    substituted[id(work_node)] = None
            else:
                #  Create a new parenthesis wrapper.
                build = _ast_base.ASTNodeParenthesisWrapper(inner)

                #  Link.
                inner.set_parent_node(build)

                #  Save the suffix number and charge.
                build.set_suffix_number(sfx)
                build.set_suffix_electronic(charge)

                #  Save the substituted node.
                substituted[id(work_node)] = build
        elif work_node.is_electronic():
            assert isinstance(work_node, _ast_base.ASTNodeElectronic)

            #  Get and substitute the charge number.
            charge = work_node.get_electronic_count().subs(subst_map).simplify()

            #  Remove the node if the charge number equals to 0.
            if charge.is_zero:
                substituted[id(work_node)] = None
                continue

            #  Create and save the substituted node.
            substituted[id(work_node)] = _ast_base.ASTNodeElectronic(charge)
        elif work_node.is_abbreviation():
            assert isinstance(work_node, _ast_base.ASTNodeAbbreviation)

            #  Create a new abbreviation node.
            build = _ast_base.ASTNodeAbbreviation(work_node.get_abbreviation_symbol())

            #  Get, substitute and save the electronic charge number.
            build.set_suffix_electronic(work_node.get_suffix_electronic().subs(subst_map).simplify())

            #  Get and substitute the suffix number.
            sfx = work_node.get_suffix_number().subs(subst_map).simplify()

            #  Remove the node if the suffix number equals to 0.
            if sfx.is_zero:
                substituted[id(work_node)] = None
            else:
                #  Save the suffix number.
                build.set_suffix_number(sfx)

                #  Create and save the substituted node.
                substituted[id(work_node)] = build
        else:
            raise RuntimeError("Never reach this condition.")

    return substituted[id(root_node)]