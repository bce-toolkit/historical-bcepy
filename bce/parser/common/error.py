#!/usr/bin/env python
#
#  Copyright 2014 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.locale.msg_id as _msg_id


class TracebackItem:
    def __init__(self, expression, start_pos, end_pos, text):
        self.__expr = expression
        self.__s_pos = start_pos
        self.__e_pos = end_pos
        self.__txt = text

    def get_expression(self):
        return self.__expr

    def get_start_position(self):
        return self.__s_pos

    def get_end_position(self):
        return self.__e_pos

    def get_text(self):
        return self.__txt

    def to_string(self, left_margin=0, underline_char="^"):
        left_margin_str = " " * left_margin
        start_pos_margin_str = " " * self.__s_pos

        return "%s%s\n%s%s%s\n%s%s%s" % (left_margin_str,
                                         self.__expr,
                                         left_margin_str,
                                         start_pos_margin_str,
                                         underline_char * (self.__e_pos - self.__s_pos + 1),
                                         left_margin_str,
                                         start_pos_margin_str,
                                         self.__txt)


class Error(Exception):
    """Parser error class."""

    def __init__(self, error_code, description_msg_id, options):
        """Initialize the class with specific error code and description.

        :type error_code: int
        :type description_msg_id: int
        :param error_code: The error code.
        :param description_msg_id: The message ID of the description.
        """

        self.__err_code = error_code
        self.__description = options.get_message(description_msg_id)
        self.__traceback = []
        self.__opts = options

    def get_error_code(self):
        """Get the error code.

        :rtype : int
        :return: The error code.
        """

        return self.__err_code

    def get_description(self):
        """Get the description.

        :rtype : str
        :return: The description.
        """

        return self.__description

    def get_traceback_count(self):
        """Get the count of traceback items.

        :rtype : int
        :return: The count.
        """

        return len(self.__traceback)

    def push_traceback(self, item):
        """Push a traceback item onto the stack.

        :type item: TracebackItem
        :param item: The traceback item.
        """

        self.__traceback.append(item)

    def push_traceback_ex(self, expression, start_pos, end_pos, msg_id, replace_map=None):
        """Create an instance of TracebackItem class with specified arguments and
        push the item onto the stack.

        :type expression: str
        :type start_pos: int
        :type end_pos: int
        :type msg_id: int
        :type replace_map: dict
        :param expression: The expression.
        :param start_pos: The starting position.
        :param end_pos: The end position.
        :param msg_id: The message ID.
        :param replace_map: The replace map of the message.
        """

        self.__traceback.append(TracebackItem(expression,
                                              start_pos,
                                              end_pos,
                                              self.__opts.get_message(msg_id, replace_map)))

    def pop_traceback(self):
        """Pop off a item from the traceback stack and return it.

        :rtype : TracebackItem
        :return: The top item of the stack.
        """

        return self.__traceback.pop()

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
        s = " " * left_margin + self.__opts.get_message(_msg_id.MSG_PE_COMMON_ERROR_HEADER,
                                                        {"$1": str(self.__err_code)}) + "\n\n"

        #  Write description.
        s += " " * left_margin + self.__opts.get_message(_msg_id.MSG_PE_COMMON_DESCRIPTION_HEADER) + "\n\n"
        s += " " * (left_margin + indent) + self.__description

        #  Write traceback items if have.
        if len(self.__traceback) != 0:
            #  Write traceback header.
            s += "\n\n" + " " * left_margin + self.__opts.get_message(_msg_id.MSG_PE_COMMON_TRACEBACK_HEADER)

            #  Write all traceback items.
            i = len(self.__traceback) - 1
            while i >= 0:
                s += "\n\n" + self.__traceback[i].to_string(left_margin + indent, "^")
                i -= 1

        return s