"""
Copyright (c) 2021  Chongqing Parsec Inc.
wax-backend is licensed under the Lesspl Public License(v0.3).
You may obtain a copy of Lesspl Public License(v0.3) at: http://www.lesspl.org
"""
import time
import random


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


def setdefault(this, key, function):
    """
    Insert key with function result if key is not in the dictionary.
    Return the value for key at last.
    """
    if key not in this:
        this[key] = function()
    return this[key]


def timestamp(delta=0) -> int:
    """
    Return the integer seconds since the Epoch,
    and plus delta seconds.
    """
    return int(time.time()) + delta


def left_strip(this: str, word: str) -> str:
    """
    Remove the matching words on the left,
    if this no startswith word, return the original string.
    """
    if this.startswith(word):
        return this[len(word):]
    else:
        return this


def randstr(seq: str, length: int) -> str:
    """
    Return random string
    """
    return ''.join(random.choice(seq) for _ in range(length))