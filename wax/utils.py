"""
Copyright (c) 2021  Chongqing Parsec Inc.
wax-backend is licensed under the Lesspl Public License(v0.3).
You may obtain a copy of Lesspl Public License(v0.3) at: http://www.lesspl.org
"""
import time


def eafp(function, default=None):
    """
    Easier to Ask for Forgiveness than Permission.
    return function() if no except is raised, else return default value.

        >>> eafp(lambda [][1], default='error')
        'error'
    """
    try:
        return function()
    except:
        return default


def now_timestamp():
    return int(time.time())
