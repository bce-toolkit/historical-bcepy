#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.parser.common.error as _pe
import bce.parser.molecule.ast.bfs as _ast_bfs
import bce.parser.molecule.abbreviation as _ml_abbr
import bce.parser.molecule.error as _ml_error
import bce.parser.molecule.ast.base as _ast_base
import bce.locale.msg_id as _msg_id
import bce.option as _opt


class MergeUtil:
    """Merge utility."""

    def __init__(self):
        """Initialize the class."""

        self.__data = {}

    def __len__(self):
        """Get the count of atoms in the atom dictionary.

        :rtype : int
        :return: The count.
        """

        return len(self.__data)

    def get_keys(self):
        """Get all keys of the atom dictionary.

        :rtype : list[str]
        :return: A list that contains all keys.
        """

        #  Initialize.
        r = []

        #  Get all keys.
        for key in self.__data:
            r.append(key)

        return r

    def multiply(self, coeff):
        """Multiply the coefficient of each atom with specified coefficient.

        :param coeff: The coefficient.
        """

        for key in self.__data:
            self.__data[key] = self.__data[key] * coeff

    def add(self, key, value):
        """Add an atom.

        :type key: str
        :param key: The atom symbol.
        :param value: The coefficient.
        """

        if key in self.__data:
            self.__data[key] = self.__data[key] + value
        else:
            self.__data[key] = value

    def merge(self, another, coeff):
        """Merge with another instance.

        :type another: MergeUtil
        :param another: Another instance.
        :param coeff: The merge coefficient.
        """

        for key in another.__data:
            self.add(key, another.__data[key] * coeff)

    def simplify(self):
        """Simplify.

        :rtype : list[str]
        :return: A list that contains all atoms which were eliminated after simplifying.
        """

        #  Initialize the eliminated atoms list.
        r = []

        #  Simplify the coefficient of each atom.
        for key in self.__data:
            #  Do simplifying.
            val = self.__data[key].simplify()

            #  Save the simplified value.
            self.__data[key] = val

            #  Put the atom into the eliminated atoms list if its coefficient equals to 0.
            if val.is_zero:
                r.append(key)

        #  Remove atoms that is in the eliminated atoms list from the atom dictionary.
        for key in r:
            self.__data.pop(key)

        return r

    def get_data(self):
        """Get the atom dictionary.

        :rtype : dict
        :return: The data.
        """
        return self.__data


def _macro_simplify(expression, mu_obj, node, options):
    """Macro for simplifying.

    :type expression: str
    :type mu_obj: MergeUtil
    :type node: _ast_base._ASTNodeBaseML
    :type options: _opt.Option
    :param expression: The origin expression.
    :param mu_obj: The MergeUtil object.
    :param node: The work node.
    :param options: The BCE options.
    """

    #  Simplify.
    removed = mu_obj.simplify()

    #  Pre-create an atom-eliminated error.
    err = _pe.Error(_ml_error.PE_ML_ATOM_ELIMINATED,
                    _msg_id.MSG_PE_ML_ATOM_ELIMINATED_DESCRIPTION,
                    options)

    #  Initialize the error flag.
    flag = False

    for symbol in removed:
        if symbol != "e":
            #  Mark the flag.
            flag = True

            #  Add a description.
            err.push_traceback_ex(expression,
                                  node.get_starting_position_in_source_text(),
                                  node.get_ending_position_in_source_text(),
                                  _msg_id.MSG_PE_ML_ATOM_ELIMINATED_TB_MESSAGE,
                                  {"$1": symbol})

    #  Raise the error if the flag was marked.
    if flag:
        raise err


def parse_ast(expression, root_node, options):
    """Parse an AST.

    :type expression: str
    :type root_node: _ast_base.ASTNodeHydrateGroup | _ast_base.ASTNodeMolecule
    :type options: _opt.Option
    :param expression: The origin expression.
    :param root_node: The root node of the AST.
    :param options: The BCE options.
    :rtype : dict
    :return: The parsed atoms dictionary.
    """

    #  Get the iteration order.
    work_list = _ast_bfs.do_bfs(root_node, True)

    #  Initialize the parsed node container.
    parsed = {}
    """:type : dict[int, MergeUtil]"""

    #  Iterate nodes from the leaves to the root.
    for work_node in work_list:
        if work_node.is_hydrate_group() or work_node.is_molecule():
            assert isinstance(work_node, _ast_base.ASTNodeHydrateGroup) or \
                isinstance(work_node, _ast_base.ASTNodeMolecule)

            #  Get the prefix number.
            coeff = work_node.get_prefix_number()

            #  Initialize a new merge utility.
            build = MergeUtil()

            #  Process the electronics.
            if work_node.is_molecule():
                el_charge = work_node.get_electronic_count().simplify()
                if not el_charge.is_zero:
                    build.add("e", el_charge * coeff)

            #  Iterate all children.
            for child_id in range(0, len(work_node)):
                #  Get child node and its parsing result.
                child = work_node[child_id]
                child_parsed = parsed[id(child)]

                #  Content check.
                if work_node.is_hydrate_group() and len(child_parsed) == 0:
                    assert isinstance(child, _ast_base.ASTNodeMolecule)

                    err = _pe.Error(_ml_error.PE_ML_NO_CONTENT,
                                    _msg_id.MSG_PE_ML_NO_CONTENT_DESCRIPTION,
                                    options)

                    if child_id == 0:
                        err.push_traceback_ex(expression,
                                              child.get_ending_position_in_source_text() + 1,
                                              child.get_ending_position_in_source_text() + 1,
                                              _msg_id.MSG_PE_ML_NO_CONTENT_BEFORE)
                    elif child_id == len(work_node) - 1:
                        err.push_traceback_ex(expression,
                                              child.get_starting_position_in_source_text() - 1,
                                              child.get_starting_position_in_source_text() - 1,
                                              _msg_id.MSG_PE_ML_NO_CONTENT_AFTER)
                    else:
                        err.push_traceback_ex(expression,
                                              child.get_starting_position_in_source_text() - 1,
                                              child.get_ending_position_in_source_text() + 1,
                                              _msg_id.MSG_PE_ML_NO_CONTENT_INSIDE)

                    raise err

                #  Merge.
                build.merge(child_parsed, coeff)

            #  Do simplifying.
            _macro_simplify(expression, build, work_node, options)

            #  Save the parsed result.
            parsed[id(work_node)] = build
        elif work_node.is_atom():
            assert isinstance(work_node, _ast_base.ASTNodeAtom)

            #  Get suffix number.
            coeff = work_node.get_suffix_number()

            #  Initialize a new merge utility.
            build = MergeUtil()

            #  Add the atom.
            build.add(work_node.get_atom_symbol(), coeff)

            #  Save the parsed result.
            parsed[id(work_node)] = build
        elif work_node.is_parenthesis():
            assert isinstance(work_node, _ast_base.ASTNodeParenthesisWrapper)

            #  Get suffix number.
            coeff = work_node.get_suffix_number()

            #  Initialize a new merge utility.
            build = MergeUtil()

            #  Get inner node and its parsing result.
            inner_parsed = parsed[id(work_node.get_inner_node())]

            #  Content check.
            if len(inner_parsed) == 0:
                err = _pe.Error(_ml_error.PE_ML_NO_CONTENT,
                                _msg_id.MSG_PE_ML_NO_CONTENT_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      work_node.get_starting_position_in_source_text(),
                                      work_node.get_right_parenthesis_position(),
                                      _msg_id.MSG_PE_ML_NO_CONTENT_INSIDE)

                raise err

            #  Merge.
            build.merge(inner_parsed, coeff)

            #  Do simplifying.
            _macro_simplify(expression, build, work_node, options)

            #  Save the parsed result.
            parsed[id(work_node)] = build
        elif work_node.is_abbreviation():
            assert isinstance(work_node, _ast_base.ASTNodeAbbreviation)

            #  Get the abbreviation symbol.
            abbr_symbol = work_node.get_abbreviation_symbol()

            #  Check symbol length.
            if len(abbr_symbol) == 0:
                err = _pe.Error(_ml_error.PE_ML_NO_CONTENT,
                                _msg_id.MSG_PE_ML_NO_CONTENT_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      work_node.get_starting_position_in_source_text(),
                                      work_node.get_right_parenthesis_position(),
                                      _msg_id.MSG_PE_ML_NO_CONTENT_INSIDE)

                raise err

            #  Initialize the resolving result container.
            abbr_resolved = None

            #  Try to resolve in the user defined dictionary.
            if options.is_user_abbreviation_dictionary_enabled():
                user_dict = options.get_user_abbreviation_dictionary()
                if abbr_symbol in user_dict:
                    abbr_resolved = user_dict[abbr_symbol]

            #  Try to resolve in system dictionary if it hasn't been resolved.
            if abbr_resolved is None and abbr_symbol in _ml_abbr.ABBREVIATIONS:
                abbr_resolved = _ml_abbr.ABBREVIATIONS[abbr_symbol]

            #  Raise an error if the abbreviation can't be resolved.
            if abbr_resolved is None:
                err = _pe.Error(_ml_error.PE_ML_UNSUPPORTED_ABBREVIATION,
                                _msg_id.MSG_PE_ML_UNSUPPORTED_ABBREVIATION_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      work_node.get_starting_position_in_source_text() + 1,
                                      work_node.get_right_parenthesis_position() - 1,
                                      _msg_id.MSG_PE_ML_UNSUPPORTED_ABBREVIATION_TB_MESSAGE)

                raise err

            #  Initialize a new merge utility.
            build = MergeUtil()

            #  Get the suffix number.
            coeff = work_node.get_suffix_number()

            #  Add atoms.
            for atom_symbol in abbr_resolved:
                build.add(atom_symbol, abbr_resolved[atom_symbol] * coeff)

            #  Do simplifying.
            _macro_simplify(expression, build, work_node, options)

            #  Save the parsed result.
            parsed[id(work_node)] = build
        else:
            raise RuntimeError("Never reach this condition.")

    #  Get the parsing result of the root node.
    root_node_parsed = parsed[id(root_node)]

    #  Content check.
    if len(root_node_parsed) == 0:
        err = _pe.Error(_ml_error.PE_ML_NO_CONTENT,
                        _msg_id.MSG_PE_ML_NO_CONTENT_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              0,
                              len(expression) - 1,
                              _msg_id.MSG_PE_ML_NO_CONTENT_INSIDE)

        raise err

    return root_node_parsed.get_data()
