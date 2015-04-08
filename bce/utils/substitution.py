#!/usr/bin/env python
#
#  Copyright 2014-2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import copy as _cp
import sympy as _sympy
import bce.base.stack as _adt_stack
import bce.math.constant as _cst
import bce.parser.common.token as _com_token
import bce.parser.common.error as _pe
import bce.parser.electronic.token as _el_token
import bce.parser.molecule.token as _ml_token
import bce.parser.mexp.reprint as _mexp_rp
import bce.parser.ce.token as _ce_token
import bce.option as _opt


class SubstitutionSyntaxError(Exception):
    """Syntax error class."""

    pass


def _construct_electronic_token(charge, initial_index, initial_position):
    """Construct an electronic token.

    :rtype : _ml_token.Token
    :param charge: The charge value.
    :param initial_index: The index of the first token being created.
    :param initial_position: The position of the first token being created.
    :return: The token or None (when |charge| == 0).
    """

    #  Simplify the charge expression.
    charge = charge.simplify()

    #  Initialize token list and position/index counter.
    el_tokens = []
    el_cur_pos = 0
    el_cur_idx = 0

    if charge.is_Number:
        #  Don't generate the token if the charge equals to zero.
        if charge == _cst.ZERO:
            return None

        #  Get whether the charge is negative.
        is_neg = charge.is_negative

        #  Get the absolute charge value.
        abs_charge = abs(charge)

        #  Stringify the absolute charge value.
        abs_charge_str = str(abs_charge)

        #  Create new token if it doesn't equal to zero.
        if abs_charge != _cst.ONE:
            el_tokens.append(_el_token.create_integer_operand_token(abs_charge_str,
                                                                    el_cur_idx,
                                                                    el_cur_pos))

        #  Go to next position.
        el_cur_idx += 1
        el_cur_pos += len(abs_charge_str)

        #  Insert the electrical descriptor.
        if is_neg:
            el_tokens.append(_el_token.create_negative_electronic_token(el_cur_idx, el_cur_pos))
        else:
            el_tokens.append(_el_token.create_positive_electronic_token(el_cur_idx, el_cur_pos))
    else:
        #  Stringify the math expression.
        charge_str = _mexp_rp.reprint_mexp(charge)

        #  Create a MEXP token and insert it to the token list.
        el_tokens.append(_el_token.create_mexp_operand_token("{%s}" % charge_str, charge, el_cur_idx, el_cur_pos))

        #  Go to next position.
        el_cur_idx += 1
        el_cur_pos += (len(charge_str) + 2)

        #  Insert the electrical descriptor.
        el_tokens.append(_el_token.create_positive_electronic_token(el_cur_idx, el_cur_pos))

    #  Create data.
    el_data = _ml_token.ElectronicDataContainer(el_tokens, charge)

    #  Generate token symbol.
    token_symbol = "<%s>" % _com_token.untokenize(el_tokens)

    #  Create a new token.
    return _ml_token.create_electronic_token(token_symbol, el_data, initial_index, initial_position)


def _get_suffix_value(token_list, initial_token_id):
    """Get suffix value and the distance between specified token and the first token after the end of the suffix.

    :type token_list: list of _ml_token.Token
    :type initial_token_id: int
    :param token_list: The token list.
    :param initial_token_id: The initial token index.
    """

    #  If the token is at the end of the token list, the suffix value is 1.
    if initial_token_id + 1 >= len(token_list):
        return _cst.ONE, 1

    #  Get next token of the specified token.
    cur_token = token_list[initial_token_id + 1]

    if cur_token.is_integer_operand():
        #  Treat the integer token as the suffix.
        return _sympy.Integer(int(cur_token.get_symbol())), 2
    elif cur_token.is_mexp_operand():
        #  Treat the math expression token as the suffix.
        return cur_token.get_evaluated_mexp(), 2
    elif cur_token.is_electronic():
        #  If the electronic token is at the end of the token list, the suffix value is 1.
        if initial_token_id + 2 >= len(token_list):
            return _cst.ONE, 2

        #  Get the first token after the electronic token.
        cur_token = token_list[initial_token_id + 2]

        if cur_token.is_integer_operand():
            #  Treat the integer token as the suffix.
            return _sympy.Integer(int(cur_token.get_symbol())), 3
        elif cur_token.is_mexp_operand():
            #  Treat the math expression token as the suffix.
            return cur_token.get_evaluated_mexp(), 3
        else:
            return _cst.ONE, 2
    else:
        #  No suffix available, the suffix value is 1.
        return _cst.ONE, 1


def _is_hydrate_molecule(token_list):
    """Get whether a molecule is hydrate molecule.

    :type token_list: list of _ml_token.Token
    :rtype : bool
    :param token_list: The token list.
    """

    #  Initialize the parenthesis level.
    p_stack = 0

    for cur_token in token_list:
        if cur_token.is_left_parenthesis():
            #  Increase the level.
            p_stack += 1
        elif cur_token.is_right_parenthesis():
            #  Decrease the level.
            p_stack -= 1
        else:
            #  Stop iterating and return if the token is a hydrate dot and it's at root level.
            if p_stack == 0 and cur_token.is_hydrate_dot():
                return True

    return False


def _linearize_molecule_token_index_and_position(token_list):
    """Linearize the index and position of a molecule token list.

    :type token_list: list of _ml_token.Token
    :param token_list: The token list.
    """

    #  Initialize the allocators.
    cur_idx = 0
    cur_pos = 0

    while cur_idx < len(token_list):
        #  Set index and position.
        token_list[cur_idx].set_index(cur_idx)
        token_list[cur_idx].set_position(cur_pos)

        #  Increase the allocators.
        cur_pos += len(token_list[cur_idx].get_symbol())
        cur_idx += 1


def substitute_symbol_in_molecule(token_list, subst_map):
    """Substitute symbols of a tokenized molecule.

    :type token_list: list of _ml_token.Token
    :type subst_map: dict
    :param token_list: The token list.
    :param subst_map: The substitution map.
    :rtype : (list of _ml_token.Token, bool, unknown, bool)
    :return: A tuple (Substituted token list, Is negative, Prefix, Is hydrate).
    :raise SubstitutionSyntaxError: Raise if the routine found a syntax error.
    :raise ValueError: Raise if the substitution is invalid.
    """

    #  Initialize flags.
    hydrate_flag = _is_hydrate_molecule(token_list)
    is_negative_flag = False
    prefix_data = None

    #  Initialize the built list.
    ret = []
    """:type : list of _ml_token.Token"""

    #  Set start token.
    token_id = 0

    #  Iterate all tokens in the origin token list.
    while token_id < len(token_list):
        #  Get current token.
        cur_token = token_list[token_id]

        if cur_token.is_mexp_operand():
            #  Do substitution on the math expression.
            mexp_value = cur_token.get_evaluated_mexp().subs(subst_map).simplify()

            if mexp_value.is_Integer:
                if mexp_value != _cst.ONE:
                    #  Create a new integer token.
                    token_symbol = str(mexp_value)
                    ret.append(_ml_token.create_integer_operand_token(token_symbol, token_id, -1))
            else:
                #  Create a new math expression token.
                token_symbol = "{%s}" % _mexp_rp.reprint_mexp(mexp_value)
                ret.append(_ml_token.create_mexp_operand_token(token_symbol, mexp_value, token_id, -1))
        elif cur_token.is_electronic():
            #  Do substitution on the charge value.
            charge_value = cur_token.get_electronic_data().get_count().subs(subst_map).simplify()

            #  Create a new electronic token.
            new_token = _construct_electronic_token(charge_value, token_id, -1)

            #  Insert the token only if the charge value doesn't equal to zero.
            if not (new_token is None):
                ret.append(new_token)
        else:
            #  Clone the token.
            new_token = _cp.deepcopy(cur_token)

            #  Reset the index and the position (real index and fake position).
            new_token.set_index(token_id)
            new_token.set_position(-1)

            #  Insert the token.
            ret.append(new_token)

        #  Go to next token.
        token_id += 1

    #  Restart from the first token.
    token_id = 0

    #  Set a fake previous hydrate dot position.
    previous_hd_position = -1

    #  Initialize an empty parentheses stack and a stack to save the previous hydrate dot positions.
    pp_stack = _adt_stack.Stack()
    hdp_stack = _adt_stack.Stack()

    #  Iterate all tokens in the built list.
    while token_id < len(ret):
        #  Get current token.
        cur_token = ret[token_id]

        if cur_token.is_symbol():
            #  Get suffix value and distance.
            suffix_val, jmp_steps = _get_suffix_value(ret, token_id)

            #  Raise an error if it's negative.
            if suffix_val.is_negative:
                raise ValueError("Negative atom coefficient.")

            if suffix_val.simplify() == _cst.ZERO:
                if token_id + jmp_steps >= len(ret):
                    #  Remove all tokens from current token to the end of the list.
                    while token_id < len(ret):
                        ret.pop(token_id)
                else:
                    #  Get the token index of the first token after the suffix.
                    target_id = ret[token_id + jmp_steps].get_index()

                    #  Remove all tokens from current token to the end of the suffix.
                    while ret[token_id].get_index() != target_id:
                        ret.pop(token_id)
            else:
                #  Go to the first token after the suffix.
                token_id += jmp_steps
        elif cur_token.is_left_parenthesis():
            #  Push the index of the token in the list onto the stack.
            pp_stack.push(token_id)

            #  Push previous hydrate dot position onto the stack.
            hdp_stack.push(previous_hd_position)

            #  Go to next token.
            token_id += 1
        elif cur_token.is_abbreviation():
            #  Get suffix value and distance.
            suffix_val, jmp_steps = _get_suffix_value(ret, token_id)

            #  Raise an error if it's negative.
            if suffix_val.is_negative:
                raise ValueError("Negative abbreviation coefficient.")

            if suffix_val.simplify() == _cst.ZERO:
                #  Remove the abbreviation and its suffix.
                for i in range(0, jmp_steps):
                    ret.pop(token_id)
            else:
                #  Go to the first token after the suffix.
                token_id += jmp_steps
        elif cur_token.is_right_parenthesis():
            #  Raise an error if there's no left parenthesis in the stack.
            if len(pp_stack) == 0:
                raise SubstitutionSyntaxError("Parenthesis mismatch.")

            if previous_hd_position + 1 == token_id:
                ret.pop(previous_hd_position)
                token_id -= 1

            previous_hd_position = hdp_stack.pop()

            #  Pop a left parenthesis from the stack.
            left_p_pos = pp_stack.pop()

            #  Get suffix value and distance.
            suffix_val, jmp_steps = _get_suffix_value(ret, token_id)

            if left_p_pos + 1 == token_id:
                if jmp_steps == 1 or \
                        (jmp_steps == 2 and
                            (ret[token_id + 1].is_integer_operand() or ret[token_id + 1].is_mexp_operand())):
                    #  Remove tokens from the left parenthesis to the end of the suffix.
                    token_id = left_p_pos
                    for i in range(0, jmp_steps + 1):
                        ret.pop(token_id)
                else:
                    if jmp_steps == 2:
                        #  Nothing to do with the electronic descriptor.
                        continue

                    #  In this section, we will merge the suffix value with the electronic descriptor.

                    #  Delete two parentheses.
                    token_id = left_p_pos
                    for i in range(0, 2):
                        ret.pop(token_id)

                    if suffix_val == _cst.ZERO:
                        #  Remove the electronic descriptor and the suffix number.
                        for i in range(0, 2):
                            ret.pop(token_id)
                    else:
                        #  Get charge value.
                        charge_value = ret[token_id].get_electronic_data().get_count() * suffix_val

                        #  Remove the suffix number.
                        ret.pop(token_id + 1)

                        #  Create a new electronic descriptor token and check it.
                        new_token = _construct_electronic_token(charge_value, ret[token_id].get_index(), -1)
                        if new_token is None:
                            raise RuntimeError("Buggy: Never reach this condition.")

                        #  Replace the old electronic token.
                        ret[token_id] = new_token

                continue

            #  Raise an error if the suffix value is negative.
            if suffix_val.is_negative:
                raise ValueError("Negative parenthesis coefficient.")

            if suffix_val.simplify() == _cst.ZERO:
                if token_id + jmp_steps >= len(ret):
                    #  Delete all tokens from the left parenthesis to the end of the list.
                    token_id = left_p_pos
                    while token_id < len(ret):
                        ret.pop(token_id)
                else:
                    #  Get the token index of the first token after the suffix.
                    target_id = ret[token_id + jmp_steps].get_index()

                    #  Delete all tokens from the left parenthesis to the end of the suffix.
                    token_id = left_p_pos
                    while ret[token_id].get_index() != target_id:
                        ret.pop(token_id)
            else:
                #  Go to the first token after the suffix.
                token_id += jmp_steps
        elif cur_token.is_mexp_operand():
            #  Free integer token should only be placed before the molecule body.
            #  Raise an error if the syntax doesn't matches with the principle above.
            if token_id != 0 and (not ret[token_id - 1].is_hydrate_dot()) and \
                    (not ret[token_id - 1].is_left_parenthesis()):
                raise SubstitutionSyntaxError("Math expression token misplaced.")

            mexp_value = cur_token.get_evaluated_mexp()
            if mexp_value.is_negative:
                if len(pp_stack) != 0 or hydrate_flag:
                    raise ValueError("Negative prefix math expression.")
                is_negative_flag = True

            #  Go to next token.
            token_id += 1
        elif cur_token.is_integer_operand():
            #  Free integer token should only be placed before the molecule body.
            #  Raise an error if the syntax doesn't matches with the principle above.
            if token_id != 0 and (not ret[token_id - 1].is_hydrate_dot()) and \
                    (not ret[token_id - 1].is_left_parenthesis()):
                raise SubstitutionSyntaxError("Integer token misplaced.")

            #  Get the value of the integer.
            int_value = int(cur_token.get_symbol())

            if int_value < 0:
                #  Sub-molecule with negative coefficient is not allowed.
                if len(pp_stack) != 0 or hydrate_flag:
                    raise ValueError("Negative prefix number.")

                #  Mark the negative flag.
                is_negative_flag = True

                #  Go to the next token.
                token_id += 1
            elif int_value == 0:
                #  Pop tokens until reaching the end of the list or a hydrate dot token or a right parenthesis.
                p_counter = 0

                #  Read until the end of the list.
                while token_id < len(ret):
                    #  Get current scanning token.
                    scan_token = ret[token_id]

                    if scan_token.is_left_parenthesis():
                        #  Increase the parenthesis level.
                        p_counter += 1

                        #  Remove the token.
                        ret.pop(token_id)
                    elif scan_token.is_right_parenthesis():
                        #  Stop scanning if the right parenthesis and the integer operand are on the
                        #  same parenthesis level.
                        if p_counter == 0:
                            break

                        #  Decrease the parenthesis level.
                        p_counter -= 1

                        #  Remove the token.
                        ret.pop(token_id)
                    elif scan_token.is_hydrate_dot():
                        #  Remove the token.
                        ret.pop(token_id)

                        #  Stop scanning if the hydrate dot and the integer are on the same parenthesis level.
                        if p_counter == 0:
                            break
                    else:
                        #  Remove the token.
                        ret.pop(token_id)
            else:
                #  Go to next token.
                token_id += 1
        elif cur_token.is_hydrate_dot():
            if previous_hd_position + 1 == token_id:
                ret.pop(token_id)
            else:
                previous_hd_position = token_id
                token_id += 1
        else:
            #  Go to next token.
            token_id += 1

    #  Raise an error if there are still some parentheses in the stack.
    if len(pp_stack) != 0:
        raise SubstitutionSyntaxError("Parenthesis mismatch.")

    #  Remove the last token if the token is a hydrate dot.
    if len(ret) != 0 and ret[-1].is_hydrate_dot():
        ret.pop(-1)

    #  Get and remove molecule coefficient if possible.
    if len(ret) != 0 and (not hydrate_flag) and (ret[0].is_integer_operand() or ret[0].is_mexp_operand()):
        #  Get the coefficient.
        if ret[0].is_integer_operand():
            prefix_data = _sympy.Integer(int(ret[0].get_symbol()))
        else:
            prefix_data = ret[0].get_evaluated_mexp()

        #  Get the absolute value of the coefficient.
        if is_negative_flag:
            prefix_data = (-prefix_data).simplify()

        if prefix_data == _cst.ONE:
            prefix_data = None

        #  Remove the coefficient token.
        ret.pop(0)

    #  After substitution, the indexes and position data are mess.
    #  We have to sort them out.
    _linearize_molecule_token_index_and_position(ret)

    return ret, is_negative_flag, prefix_data, hydrate_flag


def substitute_symbol_in_ce(tokenized_ce, subst_map, options):
    """Substitute symbols in a chemical equation.

    :type tokenized_ce: _ce_token.TokenizedCE
    :type subst_map: dict
    :type options: _opt.Option
    :param tokenized_ce: The tokenized chemical equation / expression.
    :param subst_map: The substitution map.
    :param options: The BCE options.
    :rtype : list of _ce_token.Token
    :return: The substituted token list.
    """

    ret = []
    if tokenized_ce.get_form() != _ce_token.TOKENIZED_CE_FORM_NORMAL:
        raise ValueError("Unsupported type.")

    #  Get token list.
    ce_token_list = tokenized_ce.get_token_list()

    gcd_coeff = None
    lcm_denom = _cst.ONE
    integerize_flag = True

    presubst_tokens = []
    """:type : list[list[_ml_token.Token]]"""
    presubst_negative_flag = []
    presubst_prefix = []
    presubst_is_hydrate = []
    for cur_token in ce_token_list:
        if cur_token.is_molecule():
            #  Tokenize the molecule.
            try:
                tokenized_molecule = _ml_token.tokenize(cur_token.get_symbol(), options)
            except _pe.Error:
                raise SubstitutionSyntaxError("Can't tokenize the molecule.")

            #  Do substitution on the molecule.
            subst_tokens, negative_flag, prefix_data, is_hydrate = substitute_symbol_in_molecule(tokenized_molecule,
                                                                                                 subst_map)

            #  Calculate the LCM of denominators if all prefixes are rational.
            if len(subst_tokens) != 0:
                if not (prefix_data is None):
                    if integerize_flag:
                        if prefix_data.is_Rational:
                            nd = prefix_data.as_numer_denom()
                            if gcd_coeff is None:
                                gcd_coeff = nd[0]
                            else:
                                gcd_coeff = _sympy.gcd(gcd_coeff, nd[0])
                            lcm_denom = _sympy.lcm(lcm_denom, nd[1])
                        else:
                            integerize_flag = False
                else:
                    if integerize_flag:
                        gcd_coeff = _cst.ONE

            #  Ignore zero-length molecule.
            if len(subst_tokens) == 0:
                presubst_tokens.append([])
                presubst_negative_flag.append(None)
                presubst_prefix.append(None)
                presubst_is_hydrate.append(None)
            else:
                presubst_tokens.append(subst_tokens)
                presubst_negative_flag.append(negative_flag)
                presubst_prefix.append(prefix_data)
                presubst_is_hydrate.append(is_hydrate)
        else:
            presubst_tokens.append([])
            presubst_negative_flag.append(None)
            presubst_prefix.append(None)
            presubst_is_hydrate.append(None)

    if gcd_coeff is None:
        gcd_coeff = _cst.ONE

    if integerize_flag and (lcm_denom != _cst.ONE or gcd_coeff != _cst.ONE):
        token_id = 0
        while token_id < len(ce_token_list):
            cur_token = ce_token_list[token_id]
            if cur_token.is_molecule() and len(presubst_tokens[token_id]) != 0:
                if presubst_prefix[token_id] is None:
                    if presubst_is_hydrate[token_id]:
                        presubst_tokens[token_id].insert(0, _ml_token.create_left_parenthesis_token(-1, -1))
                        presubst_tokens[token_id].append(_ml_token.create_right_parenthesis_token(-1, -1))
                    presubst_prefix[token_id] = lcm_denom / gcd_coeff
                    token_id += 1
                    continue
                new_prefix = presubst_prefix[token_id] * lcm_denom / gcd_coeff

                if new_prefix == _cst.ONE:
                    presubst_prefix[token_id] = None
                else:
                    if presubst_is_hydrate[token_id]:
                        presubst_tokens[token_id].insert(0, _ml_token.create_left_parenthesis_token(-1, -1))
                        presubst_tokens[token_id].append(_ml_token.create_right_parenthesis_token(-1, -1))
                    presubst_prefix[token_id] = new_prefix
            token_id += 1

    #  Initialize reactant list and product list.
    reactants = []
    """:type : list[(int, list [_ml_token.Token])]"""
    products = []
    """:type : list[(int, list [_ml_token.Token])]"""

    #  Initialize flag (indicates whether we have met the equal sign).
    meet_equal = False

    #  Initialize operator sign.
    #  Note: 0 -> Plus, 1 -> Minus
    operator_sign = 0

    #  Start from the first token and set the last operator position (fake position).
    token_id = 0
    last_op_position = -1

    while token_id < len(ce_token_list):
        #  Get current token.
        cur_token = ce_token_list[token_id]

        if cur_token.is_equal():
            #  Check content.
            if last_op_position + 1 == token_id:
                raise SubstitutionSyntaxError("No content.")

            #  Check duplicated equal sign.
            if meet_equal:
                raise SubstitutionSyntaxError("Duplicated equal sign.")

            #  Set last operator position and mark the flag.
            last_op_position = token_id
            meet_equal = True

            #  Reset the sign to plus sign.
            operator_sign = 0

            #  Go to next token.
            token_id += 1
        elif cur_token.is_operator_plus():
            #  Check content.
            if last_op_position + 1 == token_id:
                raise SubstitutionSyntaxError("No content.")

            #  Set last operator position.
            last_op_position = token_id

            #  Set the sign to plus sign.
            operator_sign = 0

            #  Go to next token.
            token_id += 1
        elif cur_token.is_operator_minus():
            #  Check content.
            if last_op_position + 1 == token_id and not ce_token_list[last_op_position].is_equal():
                raise SubstitutionSyntaxError("No content.")

            #  Set last operator position.
            last_op_position = token_id

            #  Set the sign to minus sign.
            operator_sign = 1

            #  Go to next token.
            token_id += 1
        elif cur_token.is_molecule():
            subst_tokens = presubst_tokens[token_id]
            negative_flag = presubst_negative_flag[token_id]
            prefix_data = presubst_prefix[token_id]

            #  Ignore zero-length molecule.
            if len(subst_tokens) == 0:
                #  Go to next token.
                token_id += 1

                continue

            #  Set the side to put the molecule.
            #  Note: 0 -> Left, 1 -> Right.
            if meet_equal:
                put_side = 1
            else:
                put_side = 0

            #  If the sign is negative, put it to the opposite side.
            if negative_flag:
                put_side = 1 - put_side

            #  Insert the prefix token if have.
            if not (prefix_data is None):
                if prefix_data.is_Integer:
                    subst_tokens.insert(0,
                                        _ml_token.create_integer_operand_token(str(prefix_data), -1, -1))
                else:
                    subst_tokens.insert(0,
                                        _ml_token.create_mexp_operand_token("{%s}" % _mexp_rp.reprint_mexp(prefix_data),
                                                                            prefix_data,
                                                                            -1,
                                                                            -1))

            #  Insert the molecule to the correct side.
            if put_side == 0:
                reactants.append((operator_sign, subst_tokens))
            else:
                products.append((operator_sign, subst_tokens))

            #  Go to next token.
            token_id += 1
        else:
            raise ValueError("Unrecognized token.")

    #  Check reactant count and product count.
    if len(reactants) == 0:
        raise ValueError("No reactant.")
    if len(products) == 0:
        raise ValueError("No product.")

    #  Initialize the index and position allocators.
    cur_idx = 0
    cur_pos = 0

    for i in range(0, len(reactants)):
        #  Get current reactant.
        cur_reactant = reactants[i]

        if i == 0:
            if cur_reactant[0] == 1:
                #  Insert a minus operator and increase the allocators.
                ret.append(_ce_token.create_operator_minus_token(cur_idx, cur_pos))
                cur_idx += 1
                cur_pos += 1
        else:
            if cur_reactant[0] == 0:
                #  Insert a plus operator.
                ret.append(_ce_token.create_operator_plus_token(cur_idx, cur_pos))
            else:
                #  Insert a minus operator.
                ret.append(_ce_token.create_operator_minus_token(cur_idx, cur_pos))

            #  Increase the allocators.
            cur_idx += 1
            cur_pos += 1

        #  Get the molecule symbol.
        molecule_sym = _com_token.untokenize(cur_reactant[1])

        #  Create a new molecule token, insert it and increase the allocators.
        ret.append(_ce_token.create_molecule_token(molecule_sym, cur_idx, cur_pos))
        cur_idx += 1
        cur_pos += len(molecule_sym)

    #  Insert equal sign token and increase the allocator.
    ret.append(_ce_token.create_equal_token(cur_idx, cur_pos))
    cur_idx += 1
    cur_pos += 1

    for i in range(0, len(products)):
        #  Get current product.
        cur_product = products[i]
        if i == 0:
            if cur_product[0] == 1:
                #  Insert a minus operator and increase the allocators.
                ret.append(_ce_token.create_operator_minus_token(cur_idx, cur_pos))
                cur_idx += 1
                cur_pos += 1
        else:
            if cur_product[0] == 0:
                #  Insert a plus operator.
                ret.append(_ce_token.create_operator_plus_token(cur_idx, cur_pos))
            else:
                #  Insert a minus operator.
                ret.append(_ce_token.create_operator_minus_token(cur_idx, cur_pos))

            #  Increase the allocators.
            cur_idx += 1
            cur_pos += 1

        #  Get the molecule symbol.
        molecule_sym = _com_token.untokenize(cur_product[1])

        #  Create a new molecule token, insert it and increase the allocators.
        ret.append(_ce_token.create_molecule_token(molecule_sym, cur_idx, cur_pos))
        cur_idx += 1
        cur_pos += len(molecule_sym)

    return ret