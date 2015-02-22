#!/usr/bin/env python

import bce.math.equation as _math_equ
import bce.parser.ce.token as _ce_token
import bce.parser.ce.parser as _ce_parser
import bce.locale.msg_id as _msg_id
import bce.logic.modeling as _logic_modeling
import bce.logic.arrange as _logic_arrange
import bce.logic.rebuild as _logic_rebuild
import bce.logic.error as _le
import copy as _py_copy

#  Add this for PyCharm auto-hinting.
import bce.option as _opt


def balance_chemical_equation(expression, options):
    """Balanced a chemical equation / expression and return an instance of
    CombinedResult class (in bce.logic.arrange) which contains the balanced
    coefficient of molecules.

    :type expression: str
    :type options: _opt.Option
    :param expression: The chemical equation / expression.
    :param options: BCE options.
    :rtype : _logic_arrange.CombinedResult
    :return: The instance of CombinedResult class.
    """

    #  Tokenize the chemical equation / expression.
    tokenized_ce = _ce_token.tokenize(expression, options)

    #  Parse tokenized chemical equation / expression.
    parsed_ce = _ce_parser.parse(expression, tokenized_ce, options)
    ce_form = parsed_ce.get_form()

    #  Build linear equations.
    equations = _logic_modeling.build_matrix(parsed_ce)
    equations_backup = _py_copy.deepcopy(equations)

    #  Solve the linear equations.
    sv_result = _math_equ.solve_equation(equations, options.get_protected_math_symbol_header())

    #  Check solved answers.
    if not _math_equ.check_solved_answer(equations_backup, sv_result):
        raise _le.LogicError(_le.LE_CONFLICT_EQUATIONS,
                             _msg_id.MSG_LE_CONFLICTED_EQUATIONS,
                             options)

    #  Do equivalent transformation to integerize the balanced efficients.
    result = _logic_arrange.sort_out_results(sv_result, ce_form, options)

    #  Perform auto-correction and moving-side operation, then return the
    #  balanced result.
    return _logic_arrange.combine_result(parsed_ce, result, options)


def build_answer(balanced_result):
    """Build a human-readable form of balanced result from an instance of CombinedResult.

    :type balanced_result: _logic_arrange.CombinedResult
    :param balanced_result: The instance of CombinedResult.
    :rtype : str
    :return: A string contains the balanced result.
    """

    return _logic_rebuild.rebuild_ce(balanced_result)


def auto_balance_chemical_equation(expression, options):
    """Balance a chemical equation / expression and return the balanced result.

    :type expression: str
    :type options: _opt.Option
    :param expression: The chemical equation / expression.
    :param options: BCE options.
    :rtype : str
    :return: A string contains the balanced result.
    """

    return build_answer(balance_chemical_equation(expression, options))