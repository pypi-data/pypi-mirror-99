"""
Enable positional subpattern matching for objects of custom classes.
"""

import inspect


def pos_match(cls=None, /, *, force=False):
    """Decorator to set `__match_args__` attribute to class `cls`.

    `__match_args__` will contain a sequence of names equal to
    parameter names in the signature of `cls.__init__`.

    If `cls` already has the `__match_args__` attribute (inherited or
    defined on its own) it will not be set, unless `force` is set to
    True.
    """
    if cls:
        # decorator used in the form @pos_match
        if not hasattr(cls, '__match_args__'):
            _set_match_args(cls)
        return cls

    if force:
        # decorator used in the form @pos_match(force=True)
        return _set_match_args

    # @pos_match(), @pos_match(force=False) or equivalent usage
    return pos_match


def _set_match_args(cls):
    init_params = inspect.signature(cls.__init__).parameters
    param_names = tuple(init_params.keys())

    # do not include the first parameter (self)
    setattr(cls, '__match_args__', param_names[1:])
    return cls


class PosMatchMeta(type):
    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        if not hasattr(cls, '__match_args__'):
            _set_match_args(cls)
        return cls


class PosMatchMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self.__class__, '__match_args__'):
            _set_match_args(self.__class__)
