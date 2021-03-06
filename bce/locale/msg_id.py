#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

MSG_PE_COMMON_ERROR_HEADER = "error.parser.common.header"
MSG_PE_COMMON_DESCRIPTION_HEADER = "error.parser.common.description"
MSG_PE_COMMON_TRACEBACK_HEADER = "error.parser.common.traceback"
MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_DESCRIPTION = "error.parser.mexp.duplicated_decimal_dot.description"
MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_PREVIOUS = "error.parser.mexp.duplicated_decimal_dot.previous"
MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_DUPLICATED = "error.parser.mexp.duplicated_decimal_dot.duplicated"
MSG_PE_MEXP_USE_PROTECTED_SYMBOL_HEADER_DESCRIPTION = "error.parser.mexp.protected_symbol_header.description"
MSG_PE_MEXP_USE_PROTECTED_SYMBOL_HEADER_TB_MESSAGE = "error.parser.mexp.protected_symbol_header.message"
MSG_PE_MEXP_UNRECOGNIZED_TOKEN_DESCRIPTION = "error.parser.mexp.unrecognized_token.description"
MSG_PE_MEXP_UNRECOGNIZED_TOKEN_TB_MESSAGE = "error.parser.mexp.unrecognized_token.message"
MSG_PE_MEXP_MISSING_OPERAND_DESCRIPTION = "error.parser.mexp.missing_operand.description"
MSG_PE_MEXP_MISSING_OPERAND_LEFT = "error.parser.mexp.missing_operand.no_left"
MSG_PE_MEXP_MISSING_OPERAND_RIGHT = "error.parser.mexp.missing_operand.no_right"
MSG_PE_MEXP_MISSING_OPERATOR_DESCRIPTION = "error.parser.mexp.missing_operator.description"
MSG_PE_MEXP_MISSING_OPERATOR_MUL_BEFORE = "error.parser.mexp.missing_operator.missing_multiply_before"
MSG_PE_MEXP_FN_UNSUPPORTED_DESCRIPTION = "error.parser.mexp.unsupported_function.description"
MSG_PE_MEXP_FN_UNSUPPORTED_TB_MESSAGE = "error.parser.mexp.unsupported_function.message"
MSG_PE_MEXP_NO_CONTENT_DESCRIPTION = "error.parser.mexp.no_content.description"
MSG_PE_MEXP_NO_CONTENT_PARENTHESIS = "error.parser.mexp.no_content.between_parentheses"
MSG_PE_MEXP_NO_CONTENT_ARGUMENT = "error.parser.mexp.no_content.within_argument"
MSG_PE_MEXP_PARENTHESIS_MISMATCH_DESCRIPTION = "error.parser.mexp.parenthesis_mismatch.description"
MSG_PE_MEXP_PARENTHESIS_MISMATCH_MISSING_LEFT = "error.parser.mexp.parenthesis_mismatch.no_left"
MSG_PE_MEXP_PARENTHESIS_MISMATCH_MISSING_RIGHT = "error.parser.mexp.parenthesis_mismatch.no_right"
MSG_PE_MEXP_PARENTHESIS_MISMATCH_INCORRECT = "error.parser.mexp.parenthesis_mismatch.incorrect"
MSG_PE_MEXP_FN_ARGC_MISMATCH_DESCRIPTION = "error.parser.mexp.function_argument_count_mismatch.description"
MSG_PE_MEXP_FN_ARGC_MISMATCH_TB_MESSAGE = "error.parser.mexp.function_argument_count_mismatch.message"
MSG_PE_MEXP_ILLEGAL_ARG_SEPARATOR_DESCRIPTION = "error.parser.mexp.illegal_argument_separator.description"
MSG_PE_MEXP_ILLEGAL_ARG_SEPARATOR_TB_MESSAGE = "error.parser.mexp.illegal_argument_separator.message"
MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_DESCRIPTION = "error.parser.mexp.divide_zero.descriptor"
MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_OPERATOR = "error.parser.mexp.divide_zero.error_operator"
MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_POW = "error.parser.mexp.divide_zero.pow_function"
MSG_PE_MEXP_RPNEV_SQRT_NEG_ARG_DESCRIPTION = "error.parser.mexp.sqrt_with_negative_operand.description"
MSG_PE_MEXP_RPNEV_SQRT_NEG_ARG_TB_MESSAGE = "error.parser.mexp.sqrt_with_negative_operand.message"

MSG_PE_ML_UNRECOGNIZED_TOKEN_DESCRIPTION = "error.parser.molecule.unrecognized_token.description"
MSG_PE_ML_UNRECOGNIZED_TOKEN_TB_MESSAGE = "error.parser.molecule.unrecognized_token.message"
MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION = "error.parser.molecule.parenthesis_mismatch.description"
MSG_PE_ML_PARENTHESIS_MISMATCH_MISSING_LEFT = "error.parser.molecule.parenthesis_mismatch.no_left"
MSG_PE_ML_PARENTHESIS_MISMATCH_MISSING_RIGHT = "error.parser.molecule.parenthesis_mismatch.no_right"
MSG_PE_ML_PARENTHESIS_MISMATCH_INCORRECT = "error.parser.molecule.parenthesis_mismatch.incorrect"
MSG_PE_ML_NO_CONTENT_DESCRIPTION = "error.parser.molecule.no_content.description"
MSG_PE_ML_NO_CONTENT_BEFORE = "error.parser.molecule.no_content.before"
MSG_PE_ML_NO_CONTENT_AFTER = "error.parser.molecule.no_content.after"
MSG_PE_ML_NO_CONTENT_INSIDE = "error.parser.molecule.no_content.inside"
MSG_PE_ML_TRACEBACK_ERROR_MEXP = "error.parser.molecule.error_parsing_traceback.mexp"

MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION = "error.parser.molecule.unexpected_token.description"
MSG_PE_ML_UNEXPECTED_TOKEN_DEFAULT = "error.parser.molecule.unexpected_token.default_message"
MSG_PE_ML_UNEXPECTED_TOKEN_EL_POSITIVITY_OR_INTEGER = "error.parser.molecule.unexpected_token." + \
                                                      "expect_positivity_or_integer"
MSG_PE_ML_UNEXPECTED_TOKEN_EL_END = "error.parser.molecule.unexpected_token.expect_electronic_end"
MSG_PE_ML_UNEXPECTED_TOKEN_EL_MISPLACED = "error.parser.molecule.unexpected_token.misplaced.electronic"
MSG_PE_ML_UNEXPECTED_TOKEN_STATUS_MISPLACED = "error.parser.molecule.unexpected_token.misplaced.status"
MSG_PE_ML_DOMAIN_ERROR_DESCRIPTION = "error.parser.molecule.domain_error.description"
MSG_PE_ML_DOMAIN_ERROR_PFX = "error.parser.molecule.domain_error.prefix"
MSG_PE_ML_DOMAIN_ERROR_EL_CHG = "error.parser.molecule.domain_error.electronic_charge"
MSG_PE_ML_DOMAIN_ERROR_SFX = "error.parser.molecule.domain_error.suffix"
MSG_PE_ML_USELESS_OPERAND_DESCRIPTION = "error.parser.molecule.useless_operand.description"
MSG_PE_ML_USELESS_OPERAND_PFX = "error.parser.molecule.useless_operand.prefix"
MSG_PE_ML_USELESS_OPERAND_EL_CHG = "error.parser.molecule.useless_operand.electronic_charge"
MSG_PE_ML_USELESS_OPERAND_SFX = "error.parser.molecule.useless_operand.suffix"
MSG_PE_ML_ATOM_ELIMINATED_DESCRIPTION = "error.parser.molecule.atom_eliminated.description"
MSG_PE_ML_ATOM_ELIMINATED_TB_MESSAGE = "error.parser.molecule.atom_eliminated.message"
MSG_PE_ML_UNSUPPORTED_ABBREVIATION_DESCRIPTION = "error.parser.molecule.unsupported_abbreviation.description"
MSG_PE_ML_UNSUPPORTED_ABBREVIATION_TB_MESSAGE = "error.parser.molecule.unsupported_abbreviation.message"
MSG_PE_CE_NO_CONTENT_DESCRIPTION = "error.parser.chemical_equation.no_content.description"
MSG_PE_CE_NO_CONTENT_OPERATOR_BETWEEN = "error.parser.chemical_equation.no_content.between_operators"
MSG_PE_CE_NO_CONTENT_OPERATOR_BEFORE = "error.parser.chemical_equation.no_content.before_operator"
MSG_PE_CE_NO_CONTENT_OPERATOR_AFTER = "error.parser.chemical_equation.no_content.after_operator"
MSG_PE_CE_MIXED_FORM_DESCRIPTION = "error.parser.chemical_equation.mixed_form.description"
MSG_PE_CE_MIXED_FORM_TB_MESSAGE = "error.parser.chemical_equation.mixed_form.message"
MSG_PE_CE_DUPLICATED_EQUAL_SIGN_DESCRIPTION = "error.parser.chemical_equation.duplicated_equal_sign.description"
MSG_PE_CE_DUPLICATED_EQUAL_SIGN_PREVIOUS = "error.parser.chemical_equation.duplicated_equal_sign.previous"
MSG_PE_CE_DUPLICATED_EQUAL_SIGN_DUPLICATED = "error.parser.chemical_equation.duplicated_equal_sign.duplicated"
MSG_PE_CE_ONLY_ONE_MOLECULE_DESCRIPTION = "error.parser.chemical_equation.only_one_molecule.description"
MSG_PE_CE_ONLY_ONE_MOLECULE_TB_MESSAGE = "error.parser.chemical_equation.only_one_molecule.description"
MSG_PE_CE_NO_EQUAL_SIGN_DESCRIPTION = "error.parser.chemical_equation.no_equal_sign.description"
MSG_PE_CE_NO_EQUAL_SIGN_TB_MESSAGE = "error.parser.chemical_equation.no_equal_sign.message"
MSG_PE_CE_SUB_ML_ERROR_TRACE_MESSAGE = "error.parser.chemical_equation.error_parsing_traceback.molecule"
MSG_PE_CE_EMPTY_EXPRESSION_DESCRIPTION = "error.parser.chemical_equation.empty_expression.description"
MSG_PE_CE_PARENTHESIS_MISMATCH_DESCRIPTION = "error.parser.chemical_equation.parenthesis_mismatch.description"
MSG_PE_CE_PARENTHESIS_MISMATCH_MISSING_LEFT = "error.parser.chemical_equation.parenthesis_mismatch.description"
MSG_PE_CE_PARENTHESIS_MISMATCH_MISSING_RIGHT = "error.parser.chemical_equation.parenthesis_mismatch.description"
MSG_LE_COMMON_ERROR_HEADER = "error.logic.common.header.error"
MSG_LE_COMMON_DESCRIPTION_HEADER = "error.logic.common.header.description"
MSG_LE_BCE_AUTO_ARRANGE_WITH_MULTI_ANSWER = "error.logic.arranger.multi_answer"
MSG_LE_BCE_SIDE_ELIMINATED_ALL = "error.logic.other.side_eliminated.all"
MSG_LE_BCE_SIDE_ELIMINATED_LEFT = "error.logic.other.side_eliminated.left"
MSG_LE_BCE_SIDE_ELIMINATED_RIGHT = "error.logic.other.side_eliminated.right"
MSG_LE_BCE_CONFLICTED_EQUATIONS = "error.logic.other.conflicted_equations"
MSG_SH_CONSOLE_INVALID_CHARACTER = "error.shell.console.invalid_character"
