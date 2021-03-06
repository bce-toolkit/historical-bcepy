#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

from bce.locale.msg_id import *

MESSAGES = {
    MSG_PE_COMMON_ERROR_HEADER: "An parser error occurred (Code: $1):",
    MSG_PE_COMMON_DESCRIPTION_HEADER: "Description:",
    MSG_PE_COMMON_TRACEBACK_HEADER: "Traceback:",
    MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_DESCRIPTION: "Duplicated decimal dot.",
    MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_PREVIOUS: "Here's the previous decimal dot.",
    MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_DUPLICATED: "Here's the duplicated decimal dot.",
    MSG_PE_MEXP_USE_PROTECTED_SYMBOL_HEADER_DESCRIPTION: "Used protected symbol header.",
    MSG_PE_MEXP_USE_PROTECTED_SYMBOL_HEADER_TB_MESSAGE: "This symbol begins with the protected symbol header '$1'.",
    MSG_PE_MEXP_UNRECOGNIZED_TOKEN_DESCRIPTION: "Unrecognized token.",
    MSG_PE_MEXP_UNRECOGNIZED_TOKEN_TB_MESSAGE: "This token can't be recognized.",
    MSG_PE_MEXP_MISSING_OPERAND_DESCRIPTION: "Missing operand.",
    MSG_PE_MEXP_MISSING_OPERAND_LEFT: "This operator has no left operand.",
    MSG_PE_MEXP_MISSING_OPERAND_RIGHT: "This operator has no right operand.",
    MSG_PE_MEXP_MISSING_OPERATOR_DESCRIPTION: "Missing operator.",
    MSG_PE_MEXP_MISSING_OPERATOR_MUL_BEFORE: "Missing a multiply operator before this token.",
    MSG_PE_MEXP_FN_UNSUPPORTED_DESCRIPTION: "Unsupported function.",
    MSG_PE_MEXP_FN_UNSUPPORTED_TB_MESSAGE: "The function '$1' hasn't been supported yet.",
    MSG_PE_MEXP_NO_CONTENT_DESCRIPTION: "No content",
    MSG_PE_MEXP_NO_CONTENT_PARENTHESIS: "There is no content between these parentheses.",
    MSG_PE_MEXP_NO_CONTENT_ARGUMENT: "This argument has no content.",
    MSG_PE_MEXP_PARENTHESIS_MISMATCH_DESCRIPTION: "Parenthesis mismatch.",
    MSG_PE_MEXP_PARENTHESIS_MISMATCH_MISSING_LEFT: "Missing left parenthesis matches with this parenthesis.",
    MSG_PE_MEXP_PARENTHESIS_MISMATCH_MISSING_RIGHT: "Missing right parenthesis matches with this parenthesis.",
    MSG_PE_MEXP_PARENTHESIS_MISMATCH_INCORRECT: "Incorrect parenthesis, this parenthesis should be changed to '$1'.",
    MSG_PE_MEXP_FN_ARGC_MISMATCH_DESCRIPTION: "Argument count mismatch.",
    MSG_PE_MEXP_FN_ARGC_MISMATCH_TB_MESSAGE: "This function requires $1 argument(s), but $2 argument(s) " +
                                             "was/were provided.",
    MSG_PE_MEXP_ILLEGAL_ARG_SEPARATOR_DESCRIPTION: "Illegal argument separator.",
    MSG_PE_MEXP_ILLEGAL_ARG_SEPARATOR_TB_MESSAGE: "This argument separator was misplaced.",
    MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_DESCRIPTION: "Divided zero.",
    MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_OPERATOR: "The right operand of this operator is zero.",
    MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_POW: "The base number is zero when the exponent number is negative.",
    MSG_PE_MEXP_RPNEV_SQRT_NEG_ARG_DESCRIPTION: "Negative square root argument.",
    MSG_PE_MEXP_RPNEV_SQRT_NEG_ARG_TB_MESSAGE: "The argument of the sqrt() function is negative.",
    MSG_PE_ML_UNRECOGNIZED_TOKEN_DESCRIPTION: "Unrecognized token.",
    MSG_PE_ML_UNRECOGNIZED_TOKEN_TB_MESSAGE: "This token can't be recognized.",
    MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION: "Parenthesis mismatch.",
    MSG_PE_ML_PARENTHESIS_MISMATCH_MISSING_LEFT: "Missing left parenthesis matches with this parenthesis.",
    MSG_PE_ML_PARENTHESIS_MISMATCH_MISSING_RIGHT: "Missing right parenthesis matches with this parenthesis.",
    MSG_PE_ML_PARENTHESIS_MISMATCH_INCORRECT: "Incorrect parenthesis, this parenthesis should be changed to '$1'.",
    MSG_PE_ML_NO_CONTENT_DESCRIPTION: "No content.",
    MSG_PE_ML_NO_CONTENT_BEFORE: "There is no content before this position.",
    MSG_PE_ML_NO_CONTENT_AFTER: "There is no content after this position.",
    MSG_PE_ML_NO_CONTENT_INSIDE: "There is no content inside.",
    MSG_PE_ML_TRACEBACK_ERROR_MEXP: "An error occurred when parsing and evaluating this math expression.",
    MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION: "Unexpected token.",
    MSG_PE_ML_UNEXPECTED_TOKEN_DEFAULT: "This token is unexpected.",
    MSG_PE_ML_UNEXPECTED_TOKEN_EL_POSITIVITY_OR_INTEGER: "Expect positivity descriptor(e+/e-) or an integer here.",
    MSG_PE_ML_UNEXPECTED_TOKEN_EL_END: "Expect a '>' here.",
    MSG_PE_ML_UNEXPECTED_TOKEN_EL_MISPLACED: "Misplaced electronic descriptor. It should be put at the end of a " +
                                             "molecule block.",
    MSG_PE_ML_UNEXPECTED_TOKEN_STATUS_MISPLACED: "Misplaced status descriptor. It should be put at the end of the " +
                                                 "molecule.",
    MSG_PE_ML_DOMAIN_ERROR_DESCRIPTION: "Domain error.",
    MSG_PE_ML_DOMAIN_ERROR_PFX: "The prefix number shouldn't be less than or equal to zero.",
    MSG_PE_ML_DOMAIN_ERROR_EL_CHG: "The electronic charge shouldn't be less than or equal to zero.",
    MSG_PE_ML_DOMAIN_ERROR_SFX: "The suffix number shouldn't be less than or equal to zero.",
    MSG_PE_ML_USELESS_OPERAND_DESCRIPTION: "Useless operand.",
    MSG_PE_ML_USELESS_OPERAND_PFX: "The prefix number is useless and it should be removed.",
    MSG_PE_ML_USELESS_OPERAND_EL_CHG: "The charge number is useless and it should be removed.",
    MSG_PE_ML_USELESS_OPERAND_SFX: "The suffix number is useless and it should be removed.",
    MSG_PE_ML_ATOM_ELIMINATED_DESCRIPTION: "Atom eliminated.",
    MSG_PE_ML_ATOM_ELIMINATED_TB_MESSAGE: "Atom '$1' was eliminated.",
    MSG_PE_ML_UNSUPPORTED_ABBREVIATION_DESCRIPTION: "Unsupported abbreviation.",
    MSG_PE_ML_UNSUPPORTED_ABBREVIATION_TB_MESSAGE: "This abbreviation is unsupported.",
    MSG_PE_CE_NO_CONTENT_DESCRIPTION: "No content.",
    MSG_PE_CE_NO_CONTENT_OPERATOR_BETWEEN: "There is no content between these two operators.",
    MSG_PE_CE_NO_CONTENT_OPERATOR_BEFORE: "There is no content before this operator.",
    MSG_PE_CE_NO_CONTENT_OPERATOR_AFTER: "There is no content after this operator.",
    MSG_PE_CE_MIXED_FORM_DESCRIPTION: "Mixed form.",
    MSG_PE_CE_MIXED_FORM_TB_MESSAGE: "The chemical equation mixed normal form and auto-arranging form.",
    MSG_PE_CE_DUPLICATED_EQUAL_SIGN_DESCRIPTION: "Duplicated equal sign.",
    MSG_PE_CE_DUPLICATED_EQUAL_SIGN_PREVIOUS: "Here's the previous equal sign.",
    MSG_PE_CE_DUPLICATED_EQUAL_SIGN_DUPLICATED: "Here's the duplicated one.",
    MSG_PE_CE_ONLY_ONE_MOLECULE_DESCRIPTION: "Only one molecule.",
    MSG_PE_CE_ONLY_ONE_MOLECULE_TB_MESSAGE: "There is only one molecule in the chemical equation.",
    MSG_PE_CE_NO_EQUAL_SIGN_DESCRIPTION: "No equal sign.",
    MSG_PE_CE_NO_EQUAL_SIGN_TB_MESSAGE: "There is no equal sign in this chemical equation.",
    MSG_PE_CE_SUB_ML_ERROR_TRACE_MESSAGE: "An error occurred when parsing the molecule.",
    MSG_PE_CE_EMPTY_EXPRESSION_DESCRIPTION: "Empty expression.",
    MSG_PE_CE_PARENTHESIS_MISMATCH_DESCRIPTION: "Parenthesis mismatch.",
    MSG_PE_CE_PARENTHESIS_MISMATCH_MISSING_LEFT: "Missing left parenthesis matches with this parenthesis.",
    MSG_PE_CE_PARENTHESIS_MISMATCH_MISSING_RIGHT: "Missing right parenthesis matches with this parenthesis.",
    MSG_LE_COMMON_ERROR_HEADER: "A logic error occurred (Code: $1):",
    MSG_LE_COMMON_DESCRIPTION_HEADER: "Description:",
    MSG_LE_BCE_AUTO_ARRANGE_WITH_MULTI_ANSWER: "Can't balance chemical equations that have multiple answers.",
    MSG_LE_BCE_SIDE_ELIMINATED_ALL: "All molecules in the chemical equation was eliminated.",
    MSG_LE_BCE_SIDE_ELIMINATED_LEFT: "All molecules on the left side of the chemical equation was eliminated.",
    MSG_LE_BCE_SIDE_ELIMINATED_RIGHT: "All molecules on the right side of the chemical equation was eliminated.",
    MSG_LE_BCE_CONFLICTED_EQUATIONS: "This chemical equation is conflicted, and it can't be balanced.",
    MSG_SH_CONSOLE_INVALID_CHARACTER: "The expression contains at least one invalid character.",
}
