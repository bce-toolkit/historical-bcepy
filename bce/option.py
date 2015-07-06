#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.locale.msg as _msg


class Option:
    """Class for containing BCE options."""

    def __init__(self):
        """Initialize the class with suggested options."""

        #  Enable auto-correct function by default.
        self.__fn_ac = True

        #  Disable user-abbreviation-dictionary by default.
        self.__fn_user_abbr = False

        #  Set user abbreviation dictionary to an empty dictionary.
        self.__user_abbr = {}

        #  Set default language to English.
        self.__msg_container = _msg.Message(_msg.MSG_LANG_ENGLISH)

        #  Set default protected math symbol header.
        self.__math_protected_symbol_hdr = "X"

    def is_auto_correct_enabled(self):
        """Get whether the auto-correct function is enabled.

        :rtype : bool
        :return: Return True if it is enabled.
        """

        return self.__fn_ac

    def is_user_abbreviation_dictionary_enabled(self):
        """Get whether the user abbreviation dictionary is enabled.

        :rtype : bool
        :return: Return True if it is enabled.
        """

        return self.__fn_user_abbr

    def enable_auto_correct(self):
        """Enable the auto-correct function."""

        self.__fn_ac = True

    def disable_auto_correct(self):
        """Disable the auto-correct function."""

        self.__fn_ac = False

    def enable_user_abbreviation_dictionary(self):
        """Enable user abbreviation dictionary."""

        self.__fn_user_abbr = True

    def disable_user_abbreviation_dictionary(self):
        """Disable user abbreviation dictionary."""

        self.__fn_user_abbr = False

    def set_user_abbreviation_dictionary(self, data):
        """Set the user abbreviation dictionary.

        :type data: dict
        :param data: The new dictionary.
        """

        self.__user_abbr = data

    def get_user_abbreviation_dictionary(self):
        """Get the user abbreviation dictionary.

        :rtype : dict
        :return: The dictionary.
        """

        return self.__user_abbr

    def get_message_language(self):
        """Get the language of messages.

        :rtype : int
        :return: One of 'MSG_LANG_*' in bce.locale.msg package.
        """

        return self.__msg_container.get_language()

    def set_message_language(self, msg_lang):
        """Set the language of messages.

        :type msg_lang: int
        :param msg_lang: One of 'MSG_LANG_*' in bce.locale.msg package.
        """

        self.__msg_container.set_language(msg_lang)

    def get_message(self, msg_id, replace_map=None):
        """Get a message.

        :type msg_id: int
        :param msg_id: The message ID.
        :param replace_map: Replace map.
        :rtype : str
        :return: The message.
        """

        return self.__msg_container.get_message(msg_id, replace_map)

    def set_protected_math_symbol_header(self, new_header):
        """Set the protected math symbol header.

        :type new_header: str
        :param new_header: The header.
        """

        if len(new_header) == 0:
            raise ValueError("Header length shouldn't be zero.")

        self.__math_protected_symbol_hdr = new_header

    def get_protected_math_symbol_header(self):
        """Get the protected math symbol header.

        :rtype : str
        :return: The header.
        """

        return self.__math_protected_symbol_hdr