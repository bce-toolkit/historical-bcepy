#!/usr/bin/env python
#
#  Copyright 2014 - 2016 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

_MAJOR = 1
_MINOR = 5
_REVISION = 1081


def get_version():
    """Get BCE version.

    :rtype : (int, int, int)
    :return: A tuple (Major, Minor, Revision).
    """

    return _MAJOR, _MINOR, _REVISION
