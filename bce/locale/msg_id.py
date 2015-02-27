#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

MSG_PE_COMMON_ERROR_HEADER = 1
MSG_PE_COMMON_DESCRIPTION_HEADER = 2
MSG_PE_COMMON_TRACEBACK_HEADER = 3
MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_DESCRIPTION = 100
MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_PREVIOUS = 101
MSG_PE_MEXP_DUPLICATED_DECIMAL_DOT_DUPLICATED = 102
MSG_PE_MEXP_EXCESSIVE_LEADING_ZERO_DESCRIPTION = 103
MSG_PE_MEXP_EXCESSIVE_LEADING_ZERO_TB_MESSAGE = 104
MSG_PE_MEXP_USE_PROTECTED_SYMBOL_HEADER_DESCRIPTION = 105
MSG_PE_MEXP_USE_PROTECTED_SYMBOL_HEADER_TB_MESSAGE = 106
MSG_PE_MEXP_UNRECOGNIZED_TOKEN_DESCRIPTION = 107
MSG_PE_MEXP_UNRECOGNIZED_TOKEN_TB_MESSAGE = 108
MSG_PE_MEXP_MISSING_OPERAND_DESCRIPTION = 109
MSG_PE_MEXP_MISSING_OPERAND_LEFT = 110
MSG_PE_MEXP_MISSING_OPERAND_RIGHT = 111
MSG_PE_MEXP_MISSING_OPERATOR_DESCRIPTION = 112
MSG_PE_MEXP_MISSING_OPERATOR_MUL_BEFORE = 113
MSG_PE_MEXP_FN_UNSUPPORTED_DESCRIPTION = 114
MSG_PE_MEXP_FN_UNSUPPORTED_TB_MESSAGE = 115
MSG_PE_MEXP_NO_CONTENT_DESCRIPTION = 116
MSG_PE_MEXP_NO_CONTENT_PARENTHESIS = 117
MSG_PE_MEXP_NO_CONTENT_ARGUMENT = 118
MSG_PE_MEXP_PARENTHESIS_MISMATCH_DESCRIPTION = 119
MSG_PE_MEXP_PARENTHESIS_MISMATCH_MISSING_LEFT = 120
MSG_PE_MEXP_PARENTHESIS_MISMATCH_MISSING_RIGHT = 121
MSG_PE_MEXP_PARENTHESIS_MISMATCH_INCORRECT = 122
MSG_PE_MEXP_FN_ARGC_MISMATCH_DESCRIPTION = 123
MSG_PE_MEXP_FN_ARGC_MISMATCH_TB_MESSAGE = 124
MSG_PE_MEXP_ILLEGAL_ARG_SEPARATOR_DESCRIPTION = 125
MSG_PE_MEXP_ILLEGAL_ARG_SEPARATOR_TB_MESSAGE = 126
MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_DESCRIPTION = 127
MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_OPERATOR = 128
MSG_PE_MEXP_RPNEV_DIVIDE_ZERO_POW = 129
MSG_PE_MEXP_RPNEV_SQRT_NEG_ARG_DESCRIPTION = 130
MSG_PE_MEXP_RPNEV_SQRT_NEG_ARG_TB_MESSAGE = 131
MSG_PE_EL_UNRECOGNIZED_TOKEN_DESCRIPTION = 500
MSG_PE_EL_UNRECOGNIZED_TOKEN_TB_MESSAGE = 501
MSG_PE_EL_SUB_MEXP_PARENTHESIS_MISMATCH_DESCRIPTION = 502
MSG_PE_EL_SUB_MEXP_PARENTHESIS_MISMATCH_MISSING_RIGHT = 504
MSG_PE_EL_SUB_MEXP_NO_CONTENT_DESCRIPTION = 505
MSG_PE_EL_SUB_MEXP_NO_CONTENT_TB_MESSAGE = 506
MSG_PE_EL_SUB_MEXP_ERROR_TRACE_MESSAGE = 507
MSG_PE_EL_SUB_MEXP_PARENTHESIS_MISMATCH_INCORRECT = 508
MSG_PE_EL_UNRECOGNIZED_FORM_DESCRIPTION = 509
MSG_PE_EL_UNRECOGNIZED_FORM_TB_MESSAGE = 510
MSG_PE_EL_ILLEGAL_TOKEN_DESCRIPTION = 511
MSG_PE_EL_ILLEGAL_TOKEN_REQ_MATH_VALUE = 512
MSG_PE_EL_ILLEGAL_TOKEN_REQ_EL_PROPERTY = 513
MSG_PE_EL_ILLEGAL_COEFFICIENT_DESCRIPTION = 514
MSG_PE_EL_ILLEGAL_COEFFICIENT_EQ_ONE = 515
MSG_PE_EL_ILLEGAL_COEFFICIENT_NEG_OR_ZERO = 516
MSG_PE_ML_UNRECOGNIZED_TOKEN_DESCRIPTION = 600
MSG_PE_ML_UNRECOGNIZED_TOKEN_TB_MESSAGE = 601
MSG_PE_ML_SUB_MEXP_ERROR_TRACE_MESSAGE = 601111
MSG_PE_ML_SUB_EL_ERROR_TRACE_MESSAGE = 602
MSG_PE_ML_NO_CONTENT_DESCRIPTION = 603
MSG_PE_ML_NO_CONTENT_MEXP = 604
MSG_PE_ML_NO_CONTENT_ABBREVIATION = 605
MSG_PE_ML_NO_CONTENT_PARENTHESIS = 606
MSG_PE_ML_NO_CONTENT_EL = 607
MSG_PE_ML_NO_CONTENT_HYDRATE_BEFORE = 608
MSG_PE_ML_NO_CONTENT_HYDRATE_BETWEEN = 609
MSG_PE_ML_EXCESSIVE_LEADING_ZERO_DESCRIPTION = 657
MSG_PE_ML_EXCESSIVE_LEADING_ZERO_TB_MESSAGE = 658
MSG_PE_ML_PARENTHESIS_MISMATCH_DESCRIPTION = 659
MSG_PE_ML_PARENTHESIS_MISMATCH_LEFT = 660
MSG_PE_ML_PARENTHESIS_MISMATCH_RIGHT = 661
MSG_PE_ML_PARENTHESIS_MISMATCH_ABBR_RIGHT = 663
MSG_PE_ML_PARENTHESIS_MISMATCH_EL_RIGHT = 664
MSG_PE_ML_PARENTHESIS_MISMATCH_MEXP_RIGHT = 665
MSG_PE_ML_PARENTHESIS_MISMATCH_INCORRECT = 666
MSG_PE_ML_UNEXPECTED_TOKEN_DESCRIPTION = 667
MSG_PE_ML_UNEXPECTED_TOKEN_TB_MESSAGE = 668
MSG_PE_ML_ABBREVIATION_UNSUPPORTED_DESCRIPTION = 669
MSG_PE_ML_ABBREVIATION_UNSUPPORTED_TB_MESSAGE = 670
MSG_PE_ML_EMPTY_MOLECULE_DESCRIPTION = 671
MSG_PE_ML_EMPTY_MOLECULE_TB_MESSAGE = 672
MSG_PE_ML_ILLEGAL_PREFIX_DESCRIPTION = 673
MSG_PE_ML_ILLEGAL_PREFIX_TB_MESSAGE = 674
MSG_PE_ML_ILLEGAL_SUFFIX_DESCRIPTION = 675
MSG_PE_ML_ILLEGAL_SUFFIX_TB_MESSAGE = 676
MSG_PE_ML_NO_DATA_DESCRIPTION = 677
MSG_PE_ML_NO_DATA_PARENTHESIS = 678
MSG_PE_ML_NO_DATA_ATOM_ELIMINATED = 679
MSG_PE_ML_CONFLICTED_STATUS_DESCRIPTION = 680
MSG_PE_ML_CONFLICTED_STATUS_LAST = 681
MSG_PE_ML_CONFLICTED_STATUS_CURRENT = 682
MSG_PE_CE_PARENTHESIS_MISMATCH_DESCRIPTION = 900
MSG_PE_CE_PARENTHESIS_MISMATCH_LEFT = 901
MSG_PE_CE_PARENTHESIS_MISMATCH_RIGHT = 902
MSG_PE_CE_NO_CONTENT_DESCRIPTION = 923
MSG_PE_CE_NO_CONTENT_OPERATOR_BETWEEN = 924
MSG_PE_CE_NO_CONTENT_OPERATOR_BEFORE = 925
MSG_PE_CE_NO_CONTENT_OPERATOR_AFTER = 926
MSG_PE_CE_MIXED_FORM_DESCRIPTION = 935
MSG_PE_CE_MIXED_FORM_TB_MESSAGE = 936
MSG_PE_CE_DUPLICATED_EQUAL_SIGN_DESCRIPTION = 940
MSG_PE_CE_DUPLICATED_EQUAL_SIGN_PREVIOUS = 941
MSG_PE_CE_DUPLICATED_EQUAL_SIGN_DUPLICATED = 942
MSG_PE_CE_ONLY_ONE_MOLECULE_DESCRIPTION = 950
MSG_PE_CE_ONLY_ONE_MOLECULE_TB_MESSAGE = 951
MSG_PE_CE_NO_EQUAL_SIGN_DESCRIPTION = 960
MSG_PE_CE_NO_EQUAL_SIGN_TB_MESSAGE = 961
MSG_PE_CE_SUB_ML_ERROR_TRACE_MESSAGE = 1000
MSG_LE_COMMON_ERROR_HEADER = 4000
MSG_LE_COMMON_DESCRIPTION_HEADER = 4001
MSG_LE_ARRANGER_MULTI_ANSWER = 4002
MSG_LE_ARRANGER_ZERO_COEFFICIENT = 4003
MSG_LE_WRONG_SIDE = 4004
MSG_LE_SIDE_ELIMINATED_ALL = 4005
MSG_LE_SIDE_ELIMINATED_LEFT = 4006
MSG_LE_SIDE_ELIMINATED_RIGHT = 4007
MSG_LE_CONFLICTED_EQUATIONS = 4008
