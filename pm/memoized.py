#=======================================================================
# Copyright (c) 2014 Baptiste Wicht
# Distributed under the terms of the MIT License.
# (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
#=======================================================================

import functools
import weakref


class memoized(object):
    caches = weakref.WeakSet()

    def __init__(self, func):
        self.func = func
        self.cache = {}
        memoized.caches.add(self)

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)

    @staticmethod
    def reset():
        for memo in memoized.caches:
            memo.cache = {}
