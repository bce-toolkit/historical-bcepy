#!/usr/bin/env python
#
#  Copyright 2014-2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.option as _opt
import bce.logic.error as _le
import bce.parser.common.error as _pe
import bce.utils.sys_locale as _sl
import bce.logic.main as _m
import bce.utils.test_utils as _tu

if __name__ == "__main__":
    #  Initialize a new option instance.
    opt = _opt.Option()

    #  Set message language.
    opt.set_message_language(_sl.get_system_locale_id())

    while True:
        #  Input a chemical equation / expression.
        try:
            expr = _tu.input_prompt(">> ").replace(" ", "")
        except EOFError:
            break

        #  Ignore zero-length expressions and comment lines.
        if len(expr) == 0 or expr[0] == "#":
            continue

        #  Balance chemical equation / expression and print it out.
        try:
            print(_m.auto_balance_chemical_equation(expr, opt))
        except _pe.Error as err1:
            print(err1.to_string())
        except _le.LogicError as err2:
            print(err2.to_string())

    #  Print an empty line.
    print("")

    exit(0)