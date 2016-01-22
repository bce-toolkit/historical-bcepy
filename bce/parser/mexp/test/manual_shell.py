#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.option as _opt
import bce.parser.mexp.evaluate as _mexp_ev
import bce.decompiler.mexp.to_bce as _mexp_rp
import bce.parser.common.error as _pe
import bce.utils.test_utils as _tu
import bce.utils.sys_locale as _sl


def run_shell():
    """Run the shell.

    :rtype : int
    :return: The exit code.
    """

    #  Generate a new option instance.
    opt = _opt.Option()
    opt.set_message_language(_sl.get_system_locale_id())

    while True:
        #  Input an expression.
        try:
            expr = _tu.input_prompt(">> ").replace(" ", "")
        except EOFError:
            break

        #  Ignore zero length lines and comment lines.
        if len(expr) == 0 or expr[0] == "#":
            continue

        #  Evaluate the expression and print it out.
        try:
            print(_mexp_rp.decompile_mexp(_mexp_ev.evaluate_math_expression(expr, opt)))
        except _pe.Error as err:
            print(err.to_string())

    #  Print an empty line.
    print("")

    return 0