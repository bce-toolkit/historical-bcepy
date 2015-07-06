#!/usr/bin/env python
#
#  Copyright 2014 - 2015 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import locale as _lc
import bce.locale.msg as _msg


def get_system_locale_id():
    """Get the message locale ID matches with the system locale.

    :rtype : int
    :return: The message locale ID.
    """

    #  Get system locale.
    sys_lc = _lc.getdefaultlocale()[0]
    """:type : str"""

    #  Return the message locale ID.
    if sys_lc.startswith("en"):
        return _msg.MSG_LANG_ENGLISH
    elif sys_lc == "zh_CN":
        return _msg.MSG_LANG_CHINESE_SIMPLIFIED
    else:
        return _msg.MSG_LANG_ENGLISH
