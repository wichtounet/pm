#=======================================================================
# Copyright (c) 2014 Baptiste Wicht
# Distributed under the terms of the MIT License.
# (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
#=======================================================================

from __future__ import print_function

color_red = "\033[0;31m"
color_green = "\033[0;32m"
color_cyan = "\033[0;33m"
color_blue = "\033[0;34m"
color_off = "\033[0;3047m"


def green_print(message):
    print(color_green + message + color_off, end="")


def red_print(message):
    print(color_red + message + color_off, end="")


def blue_print(message):
    print(color_blue + message + color_off, end="")


def cyan_print(message):
    print(color_cyan + message + color_off, end="")
