#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.option as _opt
import bce.api as _api
import bce.base.version as _ver
import bce.locale.msg_id as _msg_id
import bce.utils.sys_locale as _sl
import bce.utils.test_utils as _tu
import argparse as _arg
import signal as _signal
import sys as _sys


# noinspection PyUnusedLocal
def exit_signal_handler(signal, frame):
    """The handler for the exit signal.

    :param signal: The signal.
    :param frame: The calling frame.
    """

    print("")

    exit(0)


def main():
    """Main entry of the BCE console shell."""

    #  Capture SIGINT signal.
    _signal.signal(_signal.SIGINT, exit_signal_handler)

    #  Create an argument parser and do parsing.
    arg_parser = _arg.ArgumentParser(
        description="BCE - Chemical Equation Balancer.",
    )
    arg_parser.add_argument(
        "--output-mathml",
        dest="output_mathml",
        action="store_const",
        const=True,
        default=False,
        help="Show output in MathML format."
    )
    arg_parser.add_argument(
        "--no-banner",
        dest="show_banner",
        action="store_const",
        const=False,
        default=True,
        help="Don't show banner when loaded."
    )
    args = arg_parser.parse_args()

    #  Show the banner.
    if args.show_banner and _sys.stdin.isatty():
        ver_major, ver_minor, ver_revision = _ver.get_version()
        print("BCE V%d.%d.%d" % (ver_major, ver_minor, ver_revision))

    #  Initialize a new option instance.
    opt = _opt.Option()

    #  Set message language.
    opt.set_message_language(_sl.get_system_locale_id())

    #  Disable user abbreviations.
    opt.disable_user_abbreviation_dictionary()

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
            decompiler = [_api.DECOMPILER_TEXT]
            if args.output_mathml:
                decompiler = [_api.DECOMPILER_MATHML]
            result = _api.balance_chemical_equation(expr, decompiler, opt)[0]
            print(result)
        except _api.ParserErrorWrapper as err1:
            print(str(err1))
        except _api.LogicErrorWrapper as err2:
            print(str(err2))
        except _api.InvalidCharacterException:
            print(opt.get_message(_msg_id.MSG_SH_CONSOLE_INVALID_CHARACTER, {}))

    #  Print an empty line.
    print("")

    exit(0)
