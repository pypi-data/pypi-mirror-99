# -*- coding: utf-8 -*-

# Copyright (C) 2019 Spiralworks Technologies Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#  _     _       _             _  _ _
# | |   (_)  _  (_)           | |(_) |
# | |  _ _ _| |_ _  ____ _____| | _| |__   ____ _____  ____ _   _
# | |_/ ) (_   _) |/ ___|____ | || |  _ \ / ___|____ |/ ___) | | |
# |  _ (| | | |_| ( (___/ ___ | || | |_) ) |   / ___ | |   | |_| |
# |_| \_)_|  \__)_|\____)_____|\_)_|____/|_|   \_____|_|    \__  |
#                                                          (____/
# kitica DevicePool API
# Created by    : Joshua Kim Rivera
# Date          : February 18 2020 12:15 UTC-8
# Company       : Spiralworks Technologies Inc.
#


class DevicePoolException(Exception):
    """Base class for other exceptions
    """
    pass


class DeviceBorrowError(DevicePoolException):
    """Device is either ACTIVE
    and forced is not set to True or
    device is UNPLUGGED.
    """
    def __init__(self, message):
        self.message = message
