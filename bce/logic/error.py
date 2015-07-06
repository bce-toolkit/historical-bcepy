#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.locale.msg_id as _msg_id

#  Add this for PyCharm auto-hinting.
import bce.option as _opt

LE_WRONG_SIDE = 100
LE_SIDE_ELIMINATED = 101
LE_NO_MOLECULE = 102
LE_ZERO_COEFFICIENT = 103
LE_MULTIPLE_ANSWER = 104
LE_CONFLICT_EQUATIONS = 105


class LogicError(Exception):
    """Logic error class."""

    def __init__(self, error_code, description_id, options, replace_map=None):
        """Initialize the class with specific error code, description and
        detail note.

        :type error_code: int
        :type description_id: int
        :type options: _opt.Option
        :type replace_map: dict
        :param error_code: An integer that contains the error code.
        :param description_id: The message ID of the description.
        :param options: The BCE options.
        :param replace_map: The replace map of the description.
        """

        self.__error_code = error_code
        self.__description = options.get_message(description_id, replace_map)
        self.__opt = options

    def get_error_code(self):
        """Get the error code.

        :rtype : int
        :return: The error code.
        """

        return self.__error_code

    def get_description(self):
        """Get the description.

        :rtype : str
        :return: The description.
        """

        return self.__description

    def to_string(self, left_margin=0, indent=4):
        """Present the error in a human-readable form(string).

        :type left_margin: int
        :type indent: int
        :param left_margin: The left margin value.
        :param indent: The indent value.
        :rtype : str
        :return: The formatted string.
        """

        #  Write header.
        s = " " * left_margin + self.__opt.get_message(_msg_id.MSG_LE_COMMON_ERROR_HEADER,
                                                       {"$1": str(self.__error_code)}) + "\n\n"

        #  Write description.
        s += " " * left_margin + self.__opt.get_message(_msg_id.MSG_LE_COMMON_DESCRIPTION_HEADER) + "\n\n"
        s += " " * (left_margin + indent) + self.__description

        return s