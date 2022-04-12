# 04/02/22
# recipes.py
import  inspect
from functools import wraps, partial
from typing import Any, Callable

__all__ = "pipefunc", "curry"

class Function:
    __slots__ = "_func", "_signature"

    def __init__(self, *args, **kwargs):
        name = type(self).__name__
        message = f"{name} cannot be instantiated without defining an __init__ method"
        raise TypeError(message)

    def __repr__(self):
        name = type(self).__name__
        func = self.func.__name__
        if name.endswith("y"):
            name = name[:-1] + "ied"
        return f"<{name} function {func} at {id(self):#x}>"

    def __call__(self, *arg, **kwargs) -> Any:
        return self.func(*arg, **kwargs)

    @staticmethod
    def _require_callable(func: Callable) -> None:
        if not callable(func):
            raise TypeError(f"Function must be callable, got type {type(func)}")

    @property
    def func(self) -> Callable:
        if not hasattr(self, "_func"):
            raise AttributeError("function has not been set")
        self._require_callable(self._func)
        return self._func

    @func.setter
    def func(self, func: Callable):
        self._require_callable(func)
        self._func = func

class pipefunc(Function):
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

    def __ror__(self, arg: Any) -> Any:
        return self(arg)


class curry(Function):
    """A decorator for currying functions.

    >>> @curry
    >>> def add(a, b, c, d=0):
    ...     return a + b + c
    ...
    >>> add20 = add(5, 15)
    <curried function add at 0x{id}>
    >>> add20(100)
    120
    """

    def __init__(self, func, *args, **kwargs):
        self.func = partial(func, *args, **kwargs)
        self._signature = inspect.signature(self.func)
        self.func.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        try:
            bound = self._signature.bind(*args, **kwargs)
        except TypeError as bind_terr:
            try:
                partial_binding = self._signature.bind_partial(*args, **kwargs)
            except TypeError as terr:
                traceback = terr.with_traceback(None)
                message = f"Could not bind function arguments for {self}: {traceback}"
                raise TypeError(message)
            else:
                return type(self)(self.func, *args, **kwargs)
        else:
            return self.func(*args, **kwargs)
