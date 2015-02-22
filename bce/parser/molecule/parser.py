#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.base.stack as _adt_stack
import bce.math.constant as _math_consts
import bce.parser.common.error as _pe
import bce.parser.molecule.token as _ml_token
import bce.parser.molecule.error as _ml_errors
import bce.parser.molecule.abbreviation as _mb_abbr
import bce.parser.mexp.utils as _mexp_utils
import bce.locale.msg_id as _msg_id

#  Add this for PyCharm auto-hinting.
import bce.option as _opt


class MoleculeStatus:
    """Molecule status descriptor."""

    Unspecified = 0
    Aqueous = 1
    Gas = 2
    Liquid = 3
    Solid = 4


class MoleculeProperty:
    """Class for containing properties of a parsed molecule."""

    def __init__(self):
        """Initialize an empty class."""

        self.__atom = {}
        self.__is_hydrate = False
        self.__prefix = _math_consts.ONE
        self.__toklist = []
        self.__e = _math_consts.ZERO
        self.__stat = MoleculeStatus.Unspecified
        self.__stat_pos = -1

    def set_hydrate(self, state):
        """Set whether the molecule is a hydrate.

        :type state: bool
        :param state: A bool value that contains whether the molecule is a hydrate.
        """

        self.__is_hydrate = state

    def is_hydrate(self):
        """Get whether the molecule is a hydrate.

        :rtype : bool
        :return: Return True if the molecule is hydrate.
        """

        return self.__is_hydrate

    def is_empty(self):
        """Get whether the molecule is empty(no atom, no electronic, no status descriptor).

        :rtype : bool
        :return: Return True if the molecule is empty.
        """

        return len(self.__atom) == 0 and self.__e.is_zero and self.is_unspecfied_status()

    def set_prefix(self, prefix):
        """Set the prefix number of the molecule.

        :param prefix: The prefix number.
        """

        self.__prefix = prefix

    def get_prefix(self):
        """Get the prefix number of the molecule.

        :return: The prefix number.
        """

        return self.__prefix

    def set_token_list(self, token_list):
        """Set the token list of the molecule.

        :type token_list: list of _ml_token.Token
        :param token_list: The token list.
        """

        self.__toklist = token_list

    def get_token_list(self):
        """Get the token list of the molecule.

        :rtype : list of _ml_token.Token
        :return: The token list.
        """

        return self.__toklist

    def clear_atom(self):
        """Remove all atoms."""

        self.__atom = {}

    def add_atom(self, atom_symbol, atom_count, multiples=_math_consts.ONE):
        """Add atom to the molecule.

        :type atom_symbol: str
        :param atom_symbol: The symbol of the atom.
        :param atom_count: The count of the atom.
        :param multiples: The multiples count.
        """

        #  Get the increment.
        inc = atom_count * self.__prefix * multiples

        if not (atom_symbol in self.__atom):
            #  Create a new atom if the atom symbol isn't in the dictionary.
            self.__atom[atom_symbol] = inc
        else:
            self.__atom[atom_symbol] += inc

    def divide_common_factor(self, factor):
        """Divide the count of all atoms and electronic by a factor.

        :param factor: The factor.
        """

        for atom_symbol in self.__atom:
            self.__atom[atom_symbol] /= factor

        self.__e /= factor

    def get_atom_dictionary(self):
        """Get a dictionary maps the atoms' name to its count.

        :rtype : dict
        :return: The dictionary.
        """

        return self.__atom

    def simplify_atoms(self):
        """Simplify the count of all atoms.

        :rtype : list
        :return: Return a list that contains the symbol of atoms whose count is zero after simplifying.
        """

        est = []
        atom_lst = []

        for atom in self.__atom:
            atom_lst.append(atom)

        for atom in atom_lst:
            orig_cnt = self.__atom[atom]

            #  Simplify the expression only for math expressions.
            if len(orig_cnt.free_symbols) != 0:
                cnt = self.__atom[atom].simplify()
            else:
                cnt = self.__atom[atom]

            if cnt.is_zero:
                #  Eliminate the atom if its count is zero.
                del self.__atom[atom]
                est.append(atom)
            else:
                #  Increase the atom count.
                self.__atom[atom] = cnt

        return est

    def is_atom_empty(self):
        """Get whether there's no atom in the molecule.

        :rtype : bool
        :return: Return True if there's no atom in the molecule.
        """

        return len(self.__atom) == 0

    def add_electronic(self, e_count, multiples=_math_consts.ONE):
        """Add electronic count of the molecule.

        :param e_count: The electronic count incremental.
        :param multiples: The multiples count.
        """

        self.__e += self.__prefix * e_count * multiples

    def get_electronic_count(self):
        """Get the electronic count of the molecule.

        :return: The electronic count.
        """

        return self.__e

    def set_electronic(self, new_value):
        """Set the electronic count of the molecule.

        :param new_value: The new electronic count.
        """

        self.__e = new_value

    def merge_atoms(self, mp, multiples=_math_consts.ONE):
        """Merge atoms from another instance of this class.

        :type mp: MoleculeProperty
        :param mp: The another instance of this class.
        :param multiples: The multiples count.
        """

        mpd = mp.get_atom_dictionary()

        #  Process each atom.
        for atom in mpd:
            self.add_atom(atom, mpd[atom], multiples)

    def set_status(self, status, token_id):
        """Set molecule status.

        :type status: int
        :param status: The molecule status (one of MoleculeStatus.*).
        :type token_id: int
        :param token_id: The token ID of the status descriptor.
        """

        self.__stat = status
        self.__stat_pos = token_id

    def get_status(self):
        """Get molecule status.

        :rtype : int
        :return: The molecule status (one of MoleculeStatus.*).
        """

        return self.__stat

    def get_last_status_token_id(self):
        """Get the token ID of the last status descriptor.

        :rtype : int
        :return: The ID.
        """

        return self.__stat_pos

    def is_aqueous(self):
        """Get whether the molecule is aqueous.

        :rtype : bool
        :return: Whether the molecule is aqueous.
        """

        return self.__stat == MoleculeStatus.Aqueous

    def is_gas(self):
        """Get whether the molecule is gas.

        :rtype : bool
        :return: Whether the molecule is gas.
        """

        return self.__stat == MoleculeStatus.Gas

    def is_liquid(self):
        """Get whether the molecule is liquid.

        :rtype : bool
        :return: Whether the molecule is liquid.
        """

        return self.__stat == MoleculeStatus.Liquid

    def is_solid(self):
        """Get whether the molecule is solid.

        :rtype : bool
        :return: Whether the molecule is solid.
        """

        return self.__stat == MoleculeStatus.Solid

    def is_unspecfied_status(self):
        """Get whether the molecule status is unspecified.

        :rtype : bool
        :return: Whether the molecule status is unspecified.
        """

        return self.__stat == MoleculeStatus.Unspecified


class _ParsedSuffix:
    """Class for containing parsed suffix."""

    def __init__(self, jmp, sfx, el_count):
        """Initialize the class.

        :type jmp: int
        :param jmp: The jump-steps count.
        :param sfx: The suffix.
        :param el_count: The electronic count.
        """

        self.__jmp = jmp
        self.__sfx = sfx
        self.__el_cnt = el_count

    def get_jump_number(self):
        """Get the jump-steps count.

        :rtype : int
        :return: The count.
        """

        return self.__jmp

    def get_suffix_value(self):
        """Get the suffix number.

        :return: The suffix number.
        """

        return self.__sfx

    def get_electronic_count(self):
        """Get the electronic count.

        :return: The electronic count.
        """

        return self.__el_cnt


def _read_suffix_number(expression, token_list, token_id, options):
    """Read the suffix number of specific token.

    :type expression: str
    :type token_list: list
    :type token_id: int
    :type options: _opt.Option
    :param expression: The expression.
    :param token_list: The token list.
    :param token_id: The startup token ID.
    :param options: The BCE options.
    :rtype : _ParsedSuffix
    :return: The suffix information.
    :raise _pe.Error: Raise this error if there's a syntax error.
    """

    #  Initialize.
    token_cnt = len(token_list)
    el_token = None
    el = _math_consts.ZERO
    sfx_token = None
    sfx = _math_consts.ONE
    cur_id = token_id + 1

    #  Try read electronic token.
    if cur_id < token_cnt and token_list[cur_id].is_electronic():
        el_token = token_list[cur_id]
        cur_id += 1

    #  Try read operand token.
    if cur_id < token_cnt and token_list[cur_id].is_operand():
        sfx_token = token_list[cur_id]
        cur_id += 1

    #  Parse suffix.
    if not (sfx_token is None):
        if sfx_token.is_integer_operand():
            sfx = _mexp_utils.convert_int_string_to_rational(sfx_token.get_symbol())
        else:
            sfx = sfx_token.get_evaluated_mexp()

        #  Raise an error if the suffix is negative or zero.
        if sfx.is_zero or sfx.is_negative:
            err = _pe.Error(_ml_errors.PE_ML_ILLEGAL_SUFFIX,
                            _msg_id.MSG_PE_ML_ILLEGAL_SUFFIX_DESCRIPTION,
                            options)

            err.push_traceback_ex(expression,
                                  sfx_token.get_position(),
                                  sfx_token.get_position() + len(sfx_token.get_symbol()) - 1,
                                  _msg_id.MSG_PE_ML_ILLEGAL_SUFFIX_TB_MESSAGE)

            raise err

    #  Process electronics.
    if not (el_token is None):
        el = el_token.get_electronic_data().get_count() * sfx

    return _ParsedSuffix(cur_id - token_id, sfx, el)


def _merge_molecule_list(expression, ml_list, token_list, options):
    """Merge a molecule list to one molecule.

    :type expression: str
    :type ml_list: list of MoleculeProperty
    :type token_list: list of _ml_token.Token
    :type options: _opt.Option
    :rtype : MoleculeProperty
    :param expression: The expression.
    :param ml_list: The molecule list.
    :param token_list: The token list.
    :param options: The BCE options.
    :return: The merged molecule.
    """

    #  If there's only one molecule in the list, we don't have to do the merging operation.
    if len(ml_list) == 1:
        return ml_list[0]

    #  Initialize a new hydrate molecule property object.
    ret = MoleculeProperty()
    ret.set_hydrate(True)

    for cur_ml in ml_list:
        #  Merge atoms.
        ret.merge_atoms(cur_ml, _math_consts.ONE)

        #  Merge electronic.
        ret.add_electronic(cur_ml.get_electronic_count(), _math_consts.ONE)

        #  Check and merge molecule status.
        if not cur_ml.is_unspecfied_status():
            if (not ret.is_unspecfied_status()) and cur_ml.get_status() != ret.get_status():
                #  Get last status token and current status token.
                last_stat_tok = token_list[ret.get_last_status_token_id()]
                cur_stat_tok = token_list[cur_ml.get_last_status_token_id()]

                err = _pe.Error(_ml_errors.PE_ML_CONFLICTED_STATUS,
                                _msg_id.MSG_PE_ML_CONFLICTED_STATUS_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      cur_stat_tok.get_position(),
                                      cur_stat_tok.get_position() + len(cur_stat_tok.get_symbol()) - 1,
                                      _msg_id.MSG_PE_ML_CONFLICTED_STATUS_CURRENT)

                err.push_traceback_ex(expression,
                                      last_stat_tok.get_position(),
                                      last_stat_tok.get_position() + len(last_stat_tok.get_symbol()) - 1,
                                      _msg_id.MSG_PE_ML_CONFLICTED_STATUS_LAST)

                raise err

            #  Set status.
            ret.set_status(cur_ml.get_status(), cur_ml.get_last_status_token_id())

    return ret


def parse(expression, token_list, options):
    """Parse a molecule.

    :type expression: str
    :type token_list: list of _ml_token.Token
    :type options: _opt.Option
    :param expression: The molecule expression.
    :param token_list: The token list of the molecule.
    :param options: The BCE options.
    :rtype : MoleculeProperty
    :return: An instance of MoleculeProperty class that contains the parsed molecule.
    :raise _pe.Error: When we meet a parser error.
    """

    #  Initialize the parser.
    cur_molecule = MoleculeProperty()
    cur_hyd_ml = []
    """:type : list of MoleculeProperty"""
    cur_hyd_pp = -1
    ml_stack = _adt_stack.Stack()
    p_pos_stack = _adt_stack.Stack()
    hyd_ml_stack = _adt_stack.Stack()
    hyd_pp_stack = _adt_stack.Stack()

    token_id = 0
    token_cnt = len(token_list)

    while token_id < token_cnt:
        token = token_list[token_id]

        #  Get previous token.
        if token_id != 0:
            prev_tok = token_list[token_id - 1]
        else:
            prev_tok = None

        #  Standalone numbers are only allowed to be prefix numbers.
        #
        #  Following usage is allowed:
        #    1) 2A
        #       ^
        #
        #    2) CuSO4.5H2O
        #             ^
        #
        #    3) A(3B)
        #         ^
        if token.is_operand() and \
                (prev_tok is None or prev_tok.is_left_parenthesis() or prev_tok.is_hydrate_dot()):
            if token.is_integer_operand():
                pfx = _mexp_utils.convert_int_string_to_rational(token.get_symbol())
            else:
                pfx = token.get_evaluated_mexp()

            #  Raise an error if the prefix number is less than or equal to zero.
            if pfx.is_negative or pfx.is_zero:
                err = _pe.Error(_ml_errors.PE_ML_ILLEGAL_PREFIX,
                                _msg_id.MSG_PE_ML_ILLEGAL_PREFIX_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position() + len(token.get_symbol()) - 1,
                                      _msg_id.MSG_PE_ML_ILLEGAL_PREFIX_TB_MESSAGE)

                raise err

            #  Set the prefix number.
            cur_molecule.set_prefix(pfx)

            #  Go to next position.
            token_id += 1

            continue

        if token.is_symbol():
            #  Read suffix number.
            sfx_info = _read_suffix_number(expression, token_list, token_id, options)

            #  Add electronic(s).
            cur_molecule.add_electronic(sfx_info.get_electronic_count())

            #  Add an atom.
            cur_molecule.add_atom(token.get_symbol(), sfx_info.get_suffix_value())

            #  Go to next or next two position (depends on whether the suffix exists).
            token_id += sfx_info.get_jump_number()

            continue

        if token.is_hydrate_dot():
            #  Raise an error if there's no content between the hydrate dot and previous hydrate dot/start position.
            if cur_hyd_pp + 1 == token.get_position():
                err = _pe.Error(_ml_errors.PE_ML_NO_CONTENT,
                                _msg_id.MSG_PE_ML_NO_CONTENT_DESCRIPTION,
                                options)

                if cur_hyd_pp == -1 or (len(p_pos_stack) != 0 and p_pos_stack.top() == cur_hyd_pp):
                    err.push_traceback_ex(expression,
                                          token.get_position(),
                                          token.get_position(),
                                          _msg_id.MSG_PE_ML_NO_CONTENT_HYDRATE_BEFORE)
                else:
                    err.push_traceback_ex(expression,
                                          cur_hyd_pp,
                                          token.get_position(),
                                          _msg_id.MSG_PE_ML_NO_CONTENT_HYDRATE_BETWEEN)

                raise err

            #  Simplify the count of all atoms and remove the atoms whose count is zero after simplifying.
            elim = cur_molecule.simplify_atoms()
            if len(elim) != 0:
                err = _pe.Error(_ml_errors.PE_ML_NO_DATA,
                                _msg_id.MSG_PE_ML_NO_DATA_DESCRIPTION,
                                options)

                while len(elim) != 0:
                    err.push_traceback_ex(expression,
                                          cur_hyd_pp + 1,
                                          token.get_position() - 1,
                                          _msg_id.MSG_PE_ML_NO_DATA_ATOM_ELIMINATED,
                                          {"$1": elim.pop()})

                raise err

            #  Raise an error if the sub molecule is empty.
            if cur_molecule.is_empty():
                err = _pe.Error(_ml_errors.PE_ML_EMPTY_MOLECULE,
                                _msg_id.MSG_PE_ML_EMPTY_MOLECULE_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      cur_hyd_pp + 1,
                                      token.get_position() - 1,
                                      _msg_id.MSG_PE_ML_EMPTY_MOLECULE_TB_MESSAGE)

                raise err

            #  Insert the sub molecule to the list.
            cur_hyd_ml.append(cur_molecule)

            #  Set current position as previous hydrate dot position.
            cur_hyd_pp = token.get_position()

            #  Initialize a new sub molecule instance.
            cur_molecule = MoleculeProperty()

            #  Go to next position.
            token_id += 1

            continue

        if token.is_status():
            #  Get target status ID.
            if token.is_aqueous_status():
                target_stat = MoleculeStatus.Aqueous
            elif token.is_gas_status():
                target_stat = MoleculeStatus.Gas
            elif token.is_liquid_status():
                target_stat = MoleculeStatus.Liquid
            else:
                target_stat = MoleculeStatus.Solid

            #  Check the conflictual.
            if (not cur_molecule.is_unspecfied_status()) and cur_molecule.get_status() != target_stat:
                last_stat_tok = token_list[cur_molecule.get_last_status_token_id()]

                err = _pe.Error(_ml_errors.PE_ML_CONFLICTED_STATUS,
                                _msg_id.MSG_PE_ML_CONFLICTED_STATUS_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position() + len(token.get_symbol()) - 1,
                                      _msg_id.MSG_PE_ML_CONFLICTED_STATUS_CURRENT)

                err.push_traceback_ex(expression,
                                      last_stat_tok.get_position(),
                                      last_stat_tok.get_position() + len(last_stat_tok.get_symbol()) - 1,
                                      _msg_id.MSG_PE_ML_CONFLICTED_STATUS_LAST)

                raise err

            #  Set status.
            cur_molecule.set_status(target_stat, token_id)

            #  Go to next position.
            token_id += 1

            continue

        if token.is_left_parenthesis():
            #  Save current molecule state.
            ml_stack.push(cur_molecule)

            #  Push current position onto the stack.
            p_pos_stack.push(token.get_position())

            #  Push sub molecule and previous hydrate dot position onto the stack.
            hyd_ml_stack.push(cur_hyd_ml)
            hyd_pp_stack.push(cur_hyd_pp)

            #  Create a new inner molecule.
            cur_molecule = MoleculeProperty()

            #  Initialize a new sub molecule list and reset previous hydrate dot position.
            cur_hyd_ml = []
            cur_hyd_pp = token.get_position()

            #  Go to next position.
            token_id += 1

            continue

        if token.is_right_parenthesis():
            #  Raise an runtime error if there's no left parenthesis in the stack.
            #  Actually, this shouldn't happen because we have checked it when tokenizing.
            if len(p_pos_stack) == 0:
                err = _pe.Error(_ml_errors.PE_ML_PARENTHESIS_MISMATCH,
                                _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      token.get_position(),
                                      token.get_position(),
                                      _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_LEFT)

                raise err

            #  Get the position of the left parenthesis matches with this right parenthesis.
            prev_p_pos = p_pos_stack.top()

            #  Raise an error if there's no content between two parentheses.
            if prev_p_pos + 1 == token.get_position():
                err = _pe.Error(_ml_errors.PE_ML_NO_CONTENT,
                                _msg_id.MSG_PE_ML_NO_CONTENT_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      prev_p_pos,
                                      token.get_position(),
                                      _msg_id.MSG_PE_ML_NO_CONTENT_PARENTHESIS)

                raise err

            #  Raise an error if there's no position between previous hydrate dot and this parenthesis.
            if cur_hyd_pp + 1 == token.get_position():
                err = _pe.Error(_ml_errors.PE_ML_NO_CONTENT,
                                _msg_id.MSG_PE_ML_NO_CONTENT_DESCRIPTION,
                                options)

                if cur_hyd_pp == prev_p_pos:
                    raise RuntimeError("Never reach this condition.")
                else:
                    err.push_traceback_ex(expression,
                                          cur_hyd_pp,
                                          token.get_position(),
                                          _msg_id.MSG_PE_ML_NO_CONTENT_HYDRATE_BETWEEN)

                raise err

            #  Simplify the count of all atoms and remove the atoms whose count is zero after simplifying.
            elim = cur_molecule.simplify_atoms()
            if len(elim) != 0:
                err = _pe.Error(_ml_errors.PE_ML_NO_DATA,
                                _msg_id.MSG_PE_ML_NO_DATA_DESCRIPTION,
                                options)

                while len(elim) != 0:
                    err.push_traceback_ex(expression,
                                          cur_hyd_pp + 1,
                                          token.get_position() - 1,
                                          _msg_id.MSG_PE_ML_NO_DATA_ATOM_ELIMINATED,
                                          {"$1": elim.pop()})

                raise err

            #  Raise an error if the sub molecule is empty.
            if cur_molecule.is_empty():
                err = _pe.Error(_ml_errors.PE_ML_EMPTY_MOLECULE,
                                _msg_id.MSG_PE_ML_EMPTY_MOLECULE_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      cur_hyd_pp + 1,
                                      token.get_position() - 1,
                                      _msg_id.MSG_PE_ML_EMPTY_MOLECULE_TB_MESSAGE)

                raise err

            #  Insert the sub molecule to the list.
            cur_hyd_ml.append(cur_molecule)

            #  Merge sub molecules.
            cur_molecule = _merge_molecule_list(expression, cur_hyd_ml, token_list, options)

            #  Pop stacks.
            p_pos_stack.pop()
            cur_hyd_pp = hyd_pp_stack.pop()
            cur_hyd_ml = hyd_ml_stack.pop()

            #  Raise an error if there's no parsed data between two parentheses.
            if cur_molecule.is_empty():
                err = _pe.Error(_ml_errors.PE_ML_NO_DATA,
                                _msg_id.MSG_PE_ML_NO_DATA_DESCRIPTION,
                                options)

                err.push_traceback_ex(expression,
                                      prev_p_pos,
                                      token.get_position(),
                                      _msg_id.MSG_PE_ML_NO_DATA_PARENTHESIS)

                raise err

            #  Read suffix number.
            sfx_info = _read_suffix_number(expression, token_list, token_id, options)

            #  Backup current molecule.
            tmp_ml = cur_molecule

            #  Restore previous molecule.
            cur_molecule = ml_stack.pop()

            #  Merge two molecules.
            cur_molecule.merge_atoms(tmp_ml, sfx_info.get_suffix_value())

            #  Merge electronic count.
            cur_molecule.add_electronic(tmp_ml.get_electronic_count(), sfx_info.get_suffix_value())

            #  Merge molecule status.
            if not tmp_ml.is_unspecfied_status():
                if (not cur_molecule.is_unspecfied_status()) and tmp_ml.get_status() != cur_molecule.get_status():
                    last_stat_tok = token_list[cur_molecule.get_last_status_token_id()]
                    cur_stat_tok = token_list[tmp_ml.get_last_status_token_id()]

                    err = _pe.Error(_ml_errors.PE_ML_CONFLICTED_STATUS,
                                    _msg_id.MSG_PE_ML_CONFLICTED_STATUS_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(expression,
                                          cur_stat_tok.get_position(),
                                          cur_stat_tok.get_position() + len(cur_stat_tok.get_symbol()) - 1,
                                          _msg_id.MSG_PE_ML_CONFLICTED_STATUS_CURRENT)

                    err.push_traceback_ex(expression,
                                          last_stat_tok.get_position(),
                                          last_stat_tok.get_position() + len(last_stat_tok.get_symbol()) - 1,
                                          _msg_id.MSG_PE_ML_CONFLICTED_STATUS_LAST)

                    raise err

                cur_molecule.set_status(tmp_ml.get_status(), tmp_ml.get_last_status_token_id())

            #  Add electronic.
            cur_molecule.add_electronic(sfx_info.get_electronic_count())

            #  Go to next or next two position (depends on whether the suffix exists).
            token_id += sfx_info.get_jump_number()

            continue

        if token.is_abbreviation():
            #  Read suffix number.
            sfx_info = _read_suffix_number(expression, token_list, token_id, options)

            #  Get the symbol of the abbreviation.
            tmp_symbol = token.get_symbol()
            abbr_sym = tmp_symbol[1:len(tmp_symbol) - 1]

            #  Lookup user customized abbreviation dictionary first if it's enabled.
            override_by_custom_abbr = False

            if options.is_user_abbreviation_dictionary_enabled():
                cus_abbrs = options.get_user_abbreviation_dictionary()
                if abbr_sym in cus_abbrs:
                    abbr_dict = cus_abbrs[abbr_sym]
                    override_by_custom_abbr = True

            #  Lookup native abbreviation dictionary if the abbreviation was not found
            #  in user's dictionary.
            if not override_by_custom_abbr:
                #  Raise an error if the abbreviation isn't in the native dictionary.
                if not (abbr_sym in _mb_abbr.ABBREVIATIONS):
                    err = _pe.Error(_ml_errors.PE_ML_UNSUPPORTED_ABBREVIATION,
                                    _msg_id.MSG_PE_ML_ABBREVIATION_UNSUPPORTED_DESCRIPTION,
                                    options)

                    err.push_traceback_ex(expression,
                                          token.get_position(),
                                          token.get_position() + len(token.get_symbol()) - 1,
                                          _msg_id.MSG_PE_ML_ABBREVIATION_UNSUPPORTED_TB_MESSAGE)

                    raise err

                #  Get the atom-count dictionary.
                abbr_dict = _mb_abbr.ABBREVIATIONS[abbr_sym]

            #  Process each atom.
            for atom in abbr_dict:
                if atom == "e":
                    cur_molecule.add_electronic(abbr_dict[atom], sfx_info.get_suffix_value())
                else:
                    cur_molecule.add_atom(atom, abbr_dict[atom], sfx_info.get_suffix_value())

            #  Add electronic.
            cur_molecule.add_electronic(sfx_info.get_electronic_count())

            #  Go to next position.
            token_id += sfx_info.get_jump_number()

            continue

        if token.is_electronic():
            #  Add electronic.
            cur_molecule.add_electronic(token.get_electronic_data().get_count())

            #  Go to next position.
            token_id += 1

            continue

        #  Raise an error if the token is unexpected.
        err = _pe.Error(_ml_errors.PE_ML_UNEXPECTED_TOKEN,
                        _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              token.get_position(),
                              token.get_position() + len(token.get_symbol()) - 1,
                              _msg_id.MSG_PE_ML_UNEXPECTED_TOKEN_TB_MESSAGE)

        raise err

    #  Raise an error if the stack is not empty.
    #  Actually, this shouldn't happen because we have checked it when tokenizing.
    if len(p_pos_stack) != 0:
        err = _pe.Error(_ml_errors.PE_ML_PARENTHESIS_MISMATCH,
                        _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION,
                        options)

        while len(p_pos_stack) != 0:
            prev_p_pos = p_pos_stack.pop()
            err.push_traceback_ex(expression,
                                  prev_p_pos,
                                  prev_p_pos,
                                  _msg_id.MSG_PE_ML_PARENTHESIS_MISMATCH_RIGHT)

        raise err

    #  Simplify the count of all atoms and remove the atoms whose count is zero after simplifying.
    elim = cur_molecule.simplify_atoms()
    if len(elim) != 0:
        err = _pe.Error(_ml_errors.PE_ML_NO_DATA,
                        _msg_id.MSG_PE_ML_NO_DATA_DESCRIPTION,
                        options)

        while len(elim) != 0:
            err.push_traceback_ex(expression,
                                  cur_hyd_pp + 1,
                                  len(expression) - 1,
                                  _msg_id.MSG_PE_ML_NO_DATA_ATOM_ELIMINATED,
                                  {"$1": elim.pop()})

        raise err

    #  Raise an error if the sub molecule is empty.
    if cur_molecule.is_empty():
        err = _pe.Error(_ml_errors.PE_ML_EMPTY_MOLECULE,
                        _msg_id.MSG_PE_ML_EMPTY_MOLECULE_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              cur_hyd_pp + 1,
                              len(expression) - 1,
                              _msg_id.MSG_PE_ML_EMPTY_MOLECULE_TB_MESSAGE)

        raise err

    #  Commit the last sub module.
    cur_hyd_ml.append(cur_molecule)

    #  Merge sub molecules.
    cur_molecule = _merge_molecule_list(expression, cur_hyd_ml, token_list, options)

    #  Simplify the count of all atoms and remove the atoms whose count is zero after simplifying.
    elim = cur_molecule.simplify_atoms()
    if len(elim) != 0:
        err = _pe.Error(_ml_errors.PE_ML_NO_DATA,
                        _msg_id.MSG_PE_ML_NO_DATA_DESCRIPTION,
                        options)

        while len(elim) != 0:
            err.push_traceback_ex(expression,
                                  0,
                                  len(expression) - 1,
                                  _msg_id.MSG_PE_ML_NO_DATA_ATOM_ELIMINATED,
                                  {"$1": elim.pop()})

        raise err

    #  Raise an error if the molecule is empty.
    if cur_molecule.is_empty():
        err = _pe.Error(_ml_errors.PE_ML_EMPTY_MOLECULE,
                        _msg_id.MSG_PE_ML_EMPTY_MOLECULE_DESCRIPTION,
                        options)

        err.push_traceback_ex(expression,
                              0,
                              len(expression) - 1,
                              _msg_id.MSG_PE_ML_EMPTY_MOLECULE_TB_MESSAGE)

        raise err

    #  Set the token list of the molecule.
    cur_molecule.set_token_list(token_list)

    return cur_molecule