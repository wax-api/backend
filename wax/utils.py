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
