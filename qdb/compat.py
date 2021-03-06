#
# Copyright 2015 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and


from types import MethodType


__all__ = [
    'Connection',
    'ExitStack',
    'PY2',
    'PY3',
    'StringIO',
    'gevent',
    'gyield',
    'items',
    'keys',
    'range',
    'reduce',
    'zip',
]


try:
    reduce = reduce
    PY2 = True
except NameError:
    from functools import reduce
    PY2 = False

PY3 = not PY2

try:
    import gevent

    def gyield():
        gevent.sleep(0.01)
except ImportError:
    gevent = None

    def gyield():
        pass

if PY2:
    try:
        from io import StringIO
    except ImportError:
        from io import StringIO

    from contextlib2 import ExitStack
    import itertools

    boundmethod = MethodType
    filter = itertools.ifilter
    input = raw_input  # NOQA
    items = dict.iteritems
    keys = dict.iterkeys
    map = itertools.imap
    range = xrange  # NOQA
    zip = itertools.izip

else:
    from contextlib import ExitStack
    from io import StringIO

    def boundmethod(f, instance, owner):
        return MethodType(f, instance)

    filter = filter
    input = input  # NOQA
    items = dict.items
    keys = dict.keys
    map = map
    range = range
    zip = zip

print_ = print


class Connection(object):
    """
    A wrapper for a multiprocessing connection to emulate gipc pipes.
    """
    def __init__(self, conn):
        self.__conn = conn

    def put(self, *args, **kwargs):
        return self.__conn.send(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.__conn.recv(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.__conn, name)


def with_metaclass(metaclass, *bases):
    """
    Adds a new base in the mro for python 2 and 3 compatible
    metaclass syntax.
    """
    return metaclass('SurrogateBase', bases, {})
