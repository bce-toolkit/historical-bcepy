#!/usr/bin/env python
#
#  This file was copied and modified from SymPy project.
#
#  (C) 2014 The BCE Authors. All rights reserved.
#  (C) SymPy project.
#

#
#  Coding-Style exception:
#    This file follows SymPy's coding style. Don't apply BCE coding style
#    to this file.
#

from sympy import sympify, S, Mul, Integer
# noinspection PyProtectedMember
from sympy.core.function import _coeff_isneg
from sympy.printing.printer import Printer
from sympy.printing.precedence import precedence
import bce.utils.mathml.all as _mathml_comp


# noinspection PyMethodMayBeStatic,PyPep8Naming
class _MathMLPrinter(Printer):
    """Print SymPy expression to MathML."""

    printmethod = "_bce_mathml"
    _default_settings = {
        "order": None,
        "encoding": "utf-8"
    }

    def __init__(self, settings=None, symbol_hdr="X"):
        Printer.__init__(self, settings)
        from xml.dom.minidom import Document
        self.dom = Document()
        self.__protected_symbol_header = symbol_hdr

    def doprint(self, expr):
        return Printer._print(self, expr)

    def _print_Mul(self, expr):
        if _coeff_isneg(expr):
            x = _mathml_comp.RowComponent()
            x.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_MINUS))
            x.append_object(self._print_Mul(-expr))
            return x

        PREC = precedence(expr)

        from sympy.simplify import fraction
        numer, denom = fraction(expr)

        if denom is not S.One:
            return _mathml_comp.FractionComponent(self._print(numer), self._print(denom))

        coeff, terms = expr.as_coeff_mul()
        if coeff is S.One and len(terms) == 1:
            #  Since the negative coefficient has been handled, I don't
            #  thing a coeff of 1 can remain
            if precedence(terms[0]) < PREC:
                #  Return the argument with parentheses around.
                tmp_node = _mathml_comp.RowComponent()
                tmp_node.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_LEFT_PARENTHESIS))
                tmp_node.append_object(self._print(terms[0]))
                tmp_node.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_RIGHT_PARENTHESIS))

                return tmp_node
            else:
                #  Return the argument only.
                return self._print(terms[0])

        if self.order != 'old':
            # noinspection PyProtectedMember
            terms = Mul._from_args(terms).as_ordered_factors()

        #  Build result row element(node).
        x = _mathml_comp.RowComponent()

        if coeff != 1:
            if precedence(coeff) < PREC:
                #  Insert the coefficient number with parentheses around.
                x.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_LEFT_PARENTHESIS))
                x.append_object(self._print(coeff))
                x.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_RIGHT_PARENTHESIS))
            else:
                #  Insert the coefficient number only.
                x.append_object(self._print(coeff))

            #  Insert a multiply operator.
            if not terms[0].is_Symbol:
                x.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_MULTIPLY))

        terms_len = len(terms)
        for term_id in range(0, terms_len):
            cur_term = terms[term_id]
            if precedence(cur_term) < PREC:
                x.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_LEFT_PARENTHESIS))
                x.append_object(self._print(cur_term))
                x.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_RIGHT_PARENTHESIS))
            else:
                x.append_object(self._print(cur_term))
            if term_id + 1 != terms_len and not cur_term.is_Symbol:
                x.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_MULTIPLY))
        return x

    def _print_Add(self, expr, order=None):
        args = self._as_ordered_terms(expr, order=order)
        PREC = precedence(expr)
        dt = _mathml_comp.RowComponent()
        args_len = len(args)

        #  Iterator each part.
        for arg_id in range(0, args_len):
            cur_arg = args[arg_id]
            if cur_arg.is_negative:
                #  Get the negative number.
                neg_arg = -cur_arg

                #  Get the precedence.
                CUR_PREC = precedence(neg_arg)

                #  Add a '-' operator.
                dt.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_MINUS))

                if CUR_PREC < PREC or (_coeff_isneg(neg_arg) and arg_id != 0):
                    #  Insert the argument with parentheses around.
                    dt.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_LEFT_PARENTHESIS))
                    dt.append_object(self._print(neg_arg))
                    dt.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_RIGHT_PARENTHESIS))
                else:
                    #  Insert the argument only.
                    dt.append_object(self._print(neg_arg))
            else:
                #  Add a '+' operator if the argument is not the first one.
                if arg_id != 0:
                    dt.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_PLUS))

                #  Get the precedence.
                CUR_PREC = precedence(cur_arg)

                if CUR_PREC < PREC or (_coeff_isneg(cur_arg) and arg_id != 0):
                    #  Insert the argument with parentheses around.
                    dt.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_LEFT_PARENTHESIS))
                    dt.append_object(self._print(cur_arg))
                    dt.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_RIGHT_PARENTHESIS))
                else:
                    #  Insert the argument only.
                    dt.append_object(self._print(cur_arg))

        return dt

    def _print_Rational(self, e):
        if e.q == 1:
            #  Don't do division if the denominator is 1.
            return _mathml_comp.NumberComponent(str(e.p))

        return _mathml_comp.FractionComponent(_mathml_comp.NumberComponent(str(e.p)),
                                              _mathml_comp.NumberComponent(str(e.q)))

    def _print_Symbol(self, sym):
        if sym.name.startswith(self.__protected_symbol_header):
            return _mathml_comp.SubComponent(_mathml_comp.TextComponent("x"),
                                             _mathml_comp.TextComponent(
                                                 sym.name[len(self.__protected_symbol_header):]))
        else:
            return _mathml_comp.TextComponent(sym.name)

    def _print_Pow(self, e):
        PREC = precedence(e)

        if e.exp.is_Rational and e.exp.p == 1:
            #  If the exponent is like {1/x}, do SQRT operation if x is 2, otherwise, do 
            #  root operation.
            printed_base = self._print(e.base)

            if e.exp.q != 2:
                #  Do root operation.
                root = _mathml_comp.RootComponent(printed_base, _mathml_comp.NumberComponent(str(e.exp.q)))
            else:
                #  Do SQRT operation.
                root = _mathml_comp.SquareRootComponent(printed_base)

            return root

        if e.exp.is_negative:
            if e.exp.is_Integer and e.exp == Integer(-1):
                final_node = _mathml_comp.FractionComponent(_mathml_comp.NumberComponent("1"),
                                                            self._print(e.base))
            else:
                #  frac{1, base ^ |exp|}
                neg_exp = -e.exp

                #  Get node for the base.
                if precedence(e.base) < PREC:
                    base_node = _mathml_comp.RowComponent()
                    base_node.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_LEFT_PARENTHESIS))
                    base_node.append_object(self._print(e.base))
                    base_node.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_RIGHT_PARENTHESIS))
                else:
                    base_node = self._print(e.base)

                #  Get node for the exponent.
                if precedence(neg_exp) < PREC:
                    exp_node = _mathml_comp.RowComponent()
                    exp_node.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_LEFT_PARENTHESIS))
                    exp_node.append_object(self._print(neg_exp))
                    exp_node.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_RIGHT_PARENTHESIS))
                else:
                    exp_node = neg_exp

                final_node = _mathml_comp.FractionComponent(_mathml_comp.NumberComponent("1"),
                                                            _mathml_comp.SuperComponent(base_node, exp_node))

            return final_node

        #  Get node for the base.
        if precedence(e.base) < PREC:
            base_node = _mathml_comp.RowComponent()
            base_node.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_LEFT_PARENTHESIS))
            base_node.append_object(self._print(e.base))
            base_node.append_object(_mathml_comp.OperatorComponent(_mathml_comp.OPERATOR_RIGHT_PARENTHESIS))
        else:
            base_node = self._print(e.base)

        return _mathml_comp.SuperComponent(base_node,
                                           self._print(e.exp))

    def _print_Number(self, e):
        return _mathml_comp.NumberComponent(str(e))

    def _print_int(self, p):
        return _mathml_comp.NumberComponent(str(p))


def decompile_mexp(expr, symbol_hdr="X", **settings):
    # noinspection PyProtectedMember
    return _MathMLPrinter(settings, symbol_hdr)._print(sympify(expr))