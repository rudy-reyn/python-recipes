#!/usr/bin/env python3
# 03/23/22
# infix.py
# rudy@infix
from functools import partial
from typing import Iterable, Callable

__all__ = "Infix", "infix"

class Infix:
    """base Infix class with a default `|` operator already implemented

    examples:
        >>> xor = Infix(lambda x, y: bool(x) ^ bool(y))
        >>> 1 |xor| 2
        False
        >>> mul = Infix(lambda x, y: x * y)
        >>> 3 |mul| 2
        4
        >>> ext = Infix(lambda x, y: x + list(y) if isinstance(y, Iterable) else x + [y])
        >>> [1, 2, 3] |ext| 4
        [1, 2, 3, 4]
        >>> [1, 2, 3] |ext| [4, 5]
        [1, 2, 3, 4, 5]

    Infixes are not atomic and can therefore be used as partial functions
        >>> add = Infix(lambda x, y: x + y)
        >>> add2 = 2 | add
        >>> add2 | 3
        5
        >>> add2 | 4
        6
    """
    def __init__(self, function):
        self.function = function

    def __call__(self, x, y):
        return self.function(x, y)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.function})"

    def left_infix(self, other):
        return self.function(other)

    def right_infix(self, other):
        return self.__class__(lambda x: self.function(other, x))

    # `|` can be used as a default infix operator
    def __or__(self, other):
        return  self.left_infix(other)

    def __ror__(self, other):
        return self.right_infix(other)

def infix(cls=None, /, *, left=None, right=None) -> Callable:
    """decorator for easily subclassing Infix and overriding other Python operators
    can be used as decorator or called directly

    examples:
        >>> import builtins
        >>>
        >>> mulfix = infix("mulfix", left="__mul__", right="__rmul__")
        >>> zip = mulfix(lambda A, B: builtins.zip(A, B))
        >>> [1, 2] *zip* ['a', 'b']
        [(1, 'a'), (2, 'b')]
        >>>
        >>> @infix
        ... class andmul:
        ...     left = "__and__"
        ...     right = "__rmatmul__"
        ...
        >>> class mod_fix:
        ...     pass
        ...
        >>> mod_fix = infix(mod_fix, "__mod__", "__rmod__")
        >>>
        >>> @infix(left="__truediv__", right="__rtruediv__")
        >>> class div_fix:
        ...     pass
        ...
    """
    if isinstance(left, str) and isinstance(right, str):
        if isinstance(cls, str):
            cls = type(cls, (Infix, ), {left: Infix.left_infix, right: Infix.right_infix})
        elif callable(cls):
            setattr(cls, left, Infix.left_infix)
            setattr(cls, right, Infix.right_infix)
        elif cls is None:
            # presumably called with @infix(left=...) decorator syntax
            cls = partial(infix, left=left, right=right)
    elif callable(cls):
        # otherwise assume that the class has a `left` and `right` attribute defined
        cls = type(cls, (Infix, ), {cls.left: Infix.left_infix, cls.right: Infix.right_infix})
    return cls

del Callable
del Iterable
del partial
