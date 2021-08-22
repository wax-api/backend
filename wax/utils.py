"""
Copyright (c) 2021  Chongqing Parsec Inc.
wax-backend is licensed under the Lesspl Public License(v0.2).
You may obtain a copy of Lesspl Public License(v0.2) at: http://www.lesspl.org
"""


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
