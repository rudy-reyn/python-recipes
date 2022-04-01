# 04/01/22
# pipefunc.py
from typing import Any, Callable

class pipefunc:
    """A decorator for creating bash or R style function pipes.

    >>> @pipefunc
    >>> def factorial(n, a=1):
    ...     if n <= 0:
    ...         return a
    ...     return factorial(n - 1, n * a)
    ...
    >>> 5 | factorial
    120
    """

    __slots__ = "_func",

    def __init__(self, func: Callable):
        self.func = func

    def __repr__(self):
        return f"pipefunc(<{self.func.__name__.strip('<>')}>)"

    def __call__(self, *arg, **kwargs) -> Any:
        return self.func(*arg, **kwargs)

    def __ror__(self, arg: Any) -> Any:
        return self(arg)

    @property
    def func(self) -> Callable:
        self.func = self._func # assures self._func wasn't changed at runtime.
        return self._func

    @func.setter
    def func(self, func: Callable):
        if not callable(func):
            raise TypeError("Function must be callable")
        self._func = func
