"""
Copyright (c) 2021  Chongqing Parsec Inc.
wax-backend is licensed under the Lesspl Public License(v0.3).
You may obtain a copy of Lesspl Public License(v0.3) at: http://www.lesspl.org
"""
import sys
import time
import random
import inspect


NEW_INSPECT = sys.version_info[:3] >= (3, 8, 0)


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


def make_unique_id() -> int:
    """
    Return global increasing and unique ID
    """
    return int(time.time() * 100000) + random.randint(0, 9999)


def func_arg_spec(fn) -> dict:
    arg_spec = {}  # name: (type_, default, kind)
    for name, param in inspect.signature(fn).parameters.items():
        arg_spec[name] = (
            param.annotation,  # otherwise => inspect.Signature.empty
            param.default,  # otherwise => inspect.Signature.empty
            param.kind  # 0=POSITIONAL_ONLY 1=POSITIONAL_OR_KEYWORD 2=VAR_POSITIONAL 3=KEYWORD_ONLY 4=VAR_KEYWORD
        )
    return arg_spec

