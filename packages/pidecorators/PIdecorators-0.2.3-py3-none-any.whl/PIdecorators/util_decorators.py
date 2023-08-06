def copy_docstring_of(original):
    def wrapper(target):
        target.__doc__ = original.__doc__
        return target
    return wrapper
