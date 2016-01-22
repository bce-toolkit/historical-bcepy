#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.locale.english.msg_table as _msg_t_english
import bce.locale.chinese_simplified.msg_table as _msg_t_chn_simp

MSG_LANG_ENGLISH = 0
MSG_LANG_CHINESE_SIMPLIFIED = 1


class Message:
    """Message class."""

    def __init__(self, msg_lang):
        """Initialize the class with specific message language.

        :type msg_lang: int
        :param msg_lang: One of 'MSG_LANG_*' in this module.
        """

        self.__msg_lang = msg_lang

    def get_language(self):
        """Get current message language.

        :rtype : int
        :return: One of 'MSG_LANG_*' in this module.
        """

        return self.__msg_lang

    def set_language(self, msg_lang):
        """Set message language.

        :type msg_lang: int
        :param msg_lang: One of 'MSG_LANG_*' in this module.
        """

        self.__msg_lang = msg_lang

    def get_message(self, msg_id, replace_map=None):
        """Get a message with specific message ID.

        :type msg_id: int
        :type replace_map: dict
        :param msg_id: The message ID.
        :param replace_map: The replace map.
        :rtype : str
        :return: The message.
        """

        #  Get the message table.
        if self.__msg_lang == MSG_LANG_ENGLISH:
            msg_table = _msg_t_english.MESSAGES
        else:
            msg_table = _msg_t_chn_simp.MESSAGES

        #  Get origin message. If the message is not in the table of specific language, load
        #  English message instead.
        if msg_id in msg_table:
            msg = msg_table[msg_id]
        else:
            msg = _msg_t_english.MESSAGES[msg_id]

        #  Replace each |keyword| in the message with the mapped value of |keyword| in the replace map.
        if replace_map is not None:
            for keyword in replace_map:
                msg = msg.replace(keyword, replace_map[keyword])

        return msg