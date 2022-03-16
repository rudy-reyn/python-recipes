# 03/16/22
# pipefunc.py
from typing import Any, Iterable

class PipeFunc:
    """A decorator for creating bash or R style function pipes.

    >>> @PipeFunc
    >>> def factorial(n, a=1):
    ...     if n <= 0:
    ...         return a
    ...     return factorial(n - 1, n * a)
    ...
    >>> 5 | factorial
    120
    """

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __ror__(self, arg):
        """`|` passes the left value as a single argument as `func(arg)`

        >>> 2 | factorial
        4
        """
        return self(arg)

    def __rrshift__(self, args):
        """`>>` unpacks the left value as `func(*args)`

        >>> (5, ) >> factorial
        120
        """
        return self(*args)

    def __rand__(self, kwargs):
        """`&` unpacks the left value as `func(**kwargs)`

        >>> {'n'=5} & factorial
        120
        """
        return self(**kwargs)


    "For the following, the left value is a 2-tuple of arguments and keyword arguments `(args, kwargs)`"

    ArgKwargs = tuple[Any, dict[str, Any]]

    def __rtruediv__(self, args_kwargs: ArgKwargs):
        """`/` passes the left value as `func(*args, **kwargs)`
        if args is an iterable, otherwise as `func(args, **kwargs)`

        Note: This will also treat strings as iterables

        >>> (5, {'a'=1}) / factorial
        120
        """
        args, kwargs = args_kwargs
        if isinstance(args, Iterable):
            return self(*args, **kwargs)
        return self(args, **kwargs)

    def __rfloordiv__(self, args_kwargs: ArgKwargs):
        """`//` always unpacks args regardless of type

        >>> ((5, ), {}) // factorial
        120
        """
        args, kwargs = args_kwargs
        return self(*args, **kwargs)

    def __rmod__(self, args_kwargs: ArgKwargs):
        """`%` never unpacks args regardless of type

        >>> ((5, ), {}) % factorial
        TypeError: '<=' not supported between instances of 'tuple' and 'int'
        >>> (5, {}) % factorial
        120
        """
        args, kwargs = args_kwargs
        return self(args, **kwargs)
