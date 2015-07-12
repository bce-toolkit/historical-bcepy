#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.option as _opt
import bce.api as _api
import bce.utils.sys_locale as _sl
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
            result = _api.balance_chemical_equation(expr, [_api.DECOMPILER_TEXT], opt)[0]
            print(result)
        except _api.ParserErrorWrapper as err1:
            print(str(err1))
        except _api.LogicErrorWrapper as err2:
            print(str(err2))

    #  Print an empty line.
    print("")

    exit(0)