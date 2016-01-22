#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.base.stack as _base_stack
import sympy as _sympy

#  Add this for PyCharm auto-hinting.
import bce.math.matrix as _mat


class _EqSolverStackItem:
    """Item class of the processing stack (Internal use only)."""

    def __init__(self, ofx_row, ofx_col, break_point):
        """Initialize the class with specific row & column offset and break-point.

        :type ofx_row: int
        :type ofx_col: int
        :type break_point: int
        :param ofx_row: The row offset.
        :param ofx_col: The column offset.
        :param break_point: The break-point.
        """

        self.__or = ofx_row
        self.__oc = ofx_col
        self.__bp = break_point

    def get_offset_row(self):
        """Get the row offset.

        :rtype : int
        :return: The row offset.
        """

        return self.__or

    def get_offset_column(self):
        """Get the column offset.

        :rtype : int
        :return: The column offset.
        """

        return self.__oc

    def get_break_point(self):
        """Get the break-point.

        :rtype : int
        :return: The break-point.
        """

        return self.__bp


class SolvedEquation:
    """Class for containing the solution of linear equations."""

    def __init__(self, answer_list, unknown_count):
        """Initialize the class with specific answer list and unknown count.

        :type answer_list: list
        :type unknown_count: int
        :param answer_list: The answer list.
        :param unknown_count: The unknown count.
        """

        self.__a = answer_list
        self.__uc = unknown_count

    def get_answer_list(self):
        """Get the answer list.

        :rtype : list
        :return: The answer list.
        """

        return self.__a

    def get_unknown_count(self):
        """Get the unknown count.

        :rtype : int
        :return: The unknown count.
        """

        return self.__uc


def unknown_id_to_symbol(unknown_id, header="X"):
    """Get the symbol of unknown whose id is |unknown_id|.

    :type unknown_id: int
    :type header: str
    :param unknown_id: The ID of the unknown.
    :param header: The symbol header.
    :rtype : str
    :return: A string that contains the symbol.
    """

    #  If the |unknown_id| is zero, just returns |PROTECT_HEADER|a.
    if unknown_id == 0:
        return header + "a"

    #  Initialize alphabet table.
    ch_table = "abcdefghijklmnopqrstuvwxyz"
    ch_table_len = len(ch_table)

    #  Convert decimal to 26 ary.
    cur_id = unknown_id
    r = ""

    while cur_id != 0:
        r = ch_table[cur_id % ch_table_len] + r
        cur_id = int(cur_id / ch_table_len)

    #  Return the converted symbol.
    return header + r


def solve_equation(matrix, symbol_header="X"):
    """Solve linear equations.

    :type matrix: _mat.Matrix
    :type symbol_header: str
    :param matrix: The matrix that contains the linear equations.
    :param symbol_header: The symbol header of created symbols.
    :rtype : SolvedEquation
    :return: The solutions (presents with SolvedEquation class).
    :raise RuntimeError: When a bug appears.
    """

    #  Get matrix property.
    cur_unknown = 0
    row_c = matrix.get_row_count()
    col_c = matrix.get_column_count()

    #  Initialize
    ans = [None] * (col_c - 1)
    process_stack = _base_stack.Stack()

    #  Push initial matrix onto the stack.
    process_stack.push(_EqSolverStackItem(0, 0, 0))

    while len(process_stack) != 0:
        #  Pop off the process from process stack.
        cur_process = process_stack.pop()

        #  Get the row and column offset.
        #  In comments below, the 'first' column means the column whose offset is |offset_col| and the
        #  first row means the row whose offset is |offset_row|. 'Current matrix' means the sub-matrix
        #  of |matrix| range from [|offset_row|][|offset_column|] to [|row_c|][|col_c|].
        offset_row = cur_process.get_offset_row()
        offset_col = cur_process.get_offset_column()

        #  Get the process status(break point).
        break_point = cur_process.get_break_point()

        if break_point == 0:
            found_nz_row = False

            #  Simplify current column.
            for row_id in range(offset_row, row_c):
                tmp_offset = matrix.get_item_offset(row_id, offset_col)
                tmp_value = matrix.get_item_by_offset(tmp_offset)
                if len(tmp_value.free_symbols) != 0:
                    tmp_value = tmp_value.simplify()
                    matrix.write_item_by_offset(tmp_offset, tmp_value)

            #  Determine the row(in current matrix) whose first item is non-zero and exchange
            #  the row with the first row. If there's no such row, keep variable |found_nz_row|
            #  unchanged.
            for row_id in range(offset_row, row_c):
                if not matrix.get_item_by_position(row_id, offset_col).is_zero:
                    #  Exchange the row with the first row only if it's not the first row.
                    if row_id != offset_row:
                        matrix.exchange_row(row_id, offset_row)

                    #  Mark that we have found such row.
                    found_nz_row = True

                    break

            #  If all items in the first column are zero, set the value of unknown corresponding to
            #  this column to a new created unknown.
            if not found_nz_row:
                #  Set the value of unknown corresponding to the first column.
                ans[offset_col] = _sympy.Symbol(unknown_id_to_symbol(cur_unknown, symbol_header))
                cur_unknown += 1

                #  If there are still some unknown, solve them.
                if offset_col + 2 != col_c:
                    process_stack.push(_EqSolverStackItem(offset_row, offset_col + 1, 0))

                continue

            #  If there's only one unknown in current matrix, get the value of the unknown.
            if offset_col + 2 == col_c:
                tmp_offset = matrix.get_item_offset(offset_row, offset_col)
                ans[offset_col] = matrix.get_item_by_offset(tmp_offset + 1) / matrix.get_item_by_offset(tmp_offset)

                continue

            #  Get the offset of the first row.
            first_row_ofx = matrix.get_row_offset(offset_row)

            if offset_row + 1 == row_c:
                #  Initialize the value of the unknown corresponding to the first column.
                tmp_ans = matrix.get_item_by_offset(first_row_ofx + col_c - 1)

                #  Initialize the offset of coefficients.
                coeff_ofx = first_row_ofx + offset_col + 1

                #  Create new unknowns for the columns other than the first column and
                #  use these unknowns to represent the value of the unknown corresponding to
                #  the first column.
                for col_id in range(offset_col + 1, col_c - 1):
                    #  Set the value of unknown corresponding to this column.
                    new_sym = _sympy.Symbol(unknown_id_to_symbol(cur_unknown, symbol_header))
                    ans[col_id] = new_sym
                    cur_unknown += 1

                    #  Get the coefficient.
                    coeff = matrix.get_item_by_offset(coeff_ofx)
                    coeff_ofx += 1

                    #  Calculate the value.
                    tmp_ans -= coeff * new_sym

                #  Save the calculated value.
                ans[offset_col] = tmp_ans / matrix.get_item_by_offset(first_row_ofx + offset_col)

                continue

            #  Save the value of the first item of the first row and set its value to 1.
            tmp_offset = matrix.get_item_offset(offset_row, offset_col)
            first_value = matrix.get_item_by_offset(tmp_offset)
            matrix.write_item_by_offset(tmp_offset, _sympy.Integer(1))

            #  Move to next item.
            tmp_offset += 1

            #  Let all other items of the first row divide by the first item of the first row.
            for col_id in range(offset_col + 1, col_c):
                #  Get the value at specific position.
                tmp_value = matrix.get_item_by_offset(tmp_offset)

                #  Do division and change the value if it's not zero. (Just an optimization).
                if not tmp_value.is_zero:
                    tmp_value /= first_value
                    matrix.write_item_by_offset(tmp_offset, tmp_value)

                #  Move to next item.
                tmp_offset += 1

            #  Do elimination for rows other than the first row.
            for row_id in range(offset_row + 1, row_c):
                #  Get the value of the first item of the row whose offset is |row_id|.
                tmp_offset = matrix.get_item_offset(row_id, offset_col)
                first_value = matrix.get_item_by_offset(tmp_offset)

                #  Ignore this row if the first value of it is zero.
                if first_value.is_zero:
                    continue

                #  Set the value of the first value to zero.
                matrix.write_item_by_offset(tmp_offset, _sympy.Integer(0))

                #  Move to next item.
                tmp_offset += 1

                #  Do elimination with the first row.
                for col_id in range(offset_col + 1, col_c):
                    #  Get the value at specific position.
                    tmp_value = matrix.get_item_by_offset(tmp_offset)

                    #  Do elimination
                    tmp_value = tmp_value / first_value - matrix.get_item_by_offset(first_row_ofx + col_id)

                    #  Write the value back.
                    matrix.write_item_by_offset(tmp_offset, tmp_value)

                    #  Move to next item.
                    tmp_offset += 1

            #  Save current process. We will do back substitution next time.
            process_stack.push(_EqSolverStackItem(offset_row, offset_col, 1))

            #  Solve the order-reduced matrix.
            process_stack.push(_EqSolverStackItem(offset_row + 1, offset_col + 1, 0))

            continue

        if break_point == 1:
            #  Get the offset of the first row.
            first_row_ofx = matrix.get_row_offset(offset_row)

            #  Initialize the value of the unknown corresponding to the first column.
            tmp_ans = matrix.get_item_by_offset(first_row_ofx + col_c - 1)

            #  Initialize the offset of coefficients.
            coeff_ofx = first_row_ofx + offset_col + 1

            #  Use the calculated values to get the value of the unknown corresponding to the first column.
            for col_id in range(offset_col + 1, col_c - 1):
                #  Get the coefficient.
                coeff = matrix.get_item_by_offset(coeff_ofx)
                coeff_ofx += 1

                #  Calculate the value.
                tmp_ans -= coeff * ans[col_id]

            #  Save the calculated value.
            ans[offset_col] = tmp_ans

            continue

        raise RuntimeError("Invalid break point.")

    return SolvedEquation(ans, cur_unknown)


def check_solved_answer(origin_matrix, answer):
    """Check whether an answer satisfied all equations of an equations group.

    :type origin_matrix: _mat.Matrix
    :type answer: SolvedEquation
    :param origin_matrix: The matrix of the equations group.
    :param answer: The solved answer.
    :rtype : bool
    :return: Return True if satisfied.
    """

    #  Get answer and matrix size.
    answer_list = answer.get_answer_list()
    col_c = origin_matrix.get_column_count()
    row_c = origin_matrix.get_row_count()

    for row_id in range(0, row_c):
        #  Initialize sum.
        s = _sympy.Integer(0)

        #  Get the offset of the first of the row.
        ofx = origin_matrix.get_row_offset(row_id)

        #  Get the sum.
        for col_id in range(0, col_c - 1):
            s += origin_matrix.get_item_by_offset(ofx) * answer_list[col_id]
            ofx += 1

        s = s.simplify()

        #  Check the sum.
        if s != origin_matrix.get_item_by_offset(ofx):
            return False

    return True