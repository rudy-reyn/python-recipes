# 03/23/22
# infix.py
from __future__ import annotations
import inspect
from abc import ABC, abstractmethod
from typing import Callable, Literal, overload, TypeVar
from .utils import Nil

__all__ = "Infix", "infix", "BaseInfix"

Operator = Literal['&', '|', '^', '+', '-', '*', '@', '/', '//', '%', '<<', '>>']
NewInfix = TypeVar("NewInfix", bound="BaseInfix")

operators = {
    "&": "and", "|": "or", "^": "xor",
    "+": "add", "-": "sub", "*": "mul",
    "@": "matmul", "/": "tuediv", "//": "floordiv",
    "%": "mod", "<<": "lshift", ">>": "rshift"
}

class BaseInfix(ABC):
    """Infix Base class used to instantiate new Infix subclasses using specified operators.

    The operator and left operator classmethods must be defined and return a valid python
    operator, which includes: '&', '|', '^', '+', '-', '*', '@', '/', '//', '%', '<<', '>>'.

    Short circuited operators are not supported as specific right and left magic methods do not
    exist. These include: '==', '!=', '>', '>=', '>', '<='.

    Examples:
        >>> class Infix(BaseInfix):
        ...     @classmethod
        ...     def operator(cls):
        ...         return "|"
        ...     @classmethod
        ...     def right_operator(cls):
        ...         return "|"
        ...
        >>> @Infix
        >>> def divides(a, b):
        ...     return b % a == 0
        ...
        >>> @Infix
        >>> def tee(content, filename):
        ...     print(content)
        ...     with open(filename, "wb+") as file:
        ...         bytes_written = file.write(content)
        ...     return bytes_written
        ...
        >>> bytes_written = 'Hello, World!' |tee| "filename.txt"
        Hello, World!
    """
    def __init__(self, function: Callable):
        if not callable(function):
            raise TypeError(f"expected a callable, got type '{type(function)}'")
        self.function = function
        self.left_bind = Nil
        self.right_bind = Nil

    def __init_subclass__(cls: NewInfix):
        operator = cls.operator()
        right_operator = cls.right_operator()
        if not operator or not right_operator:
            raise TypeError("subclasses of BaseInfix with abstract methods operator, right_operator "
                    "must be set to valid python operators")
        method = operator_method(cls.operator())
        if cls.right_operator() == cls.operator():
            right_method = method
        else:
            right_method = operator_method(cls.right_operator())

        def left_infix(self, other):
            if self.left_bind is not Nil:
                bind, self.left_bind = self.left_bind, Nil
                self.right_bind = Nil
                raise AttributeError(f"left hand argument is already bound")
            if self.right_bind is Nil:
                self.left_bind = other
                return self
            argument = self.right_bind
            self.right_bind = Nil
            return self(argument, other)

        def right_infix(self, other):
            if self.right_bind is not Nil:
                bind, self.right_bind = self.right_bind, Nil
                self.left_bind = Nil
                raise AttributeError(f"right hand argument is already bound")
            if self.left_bind is Nil:
                self.right_bind = other
                return self
            argument, self.left_bind = self.left_bind, Nil
            return self(argument, other)

        def invoked_invalid_operation(self, value):
            """Ensures that each argument binding is cleared
            in case an unsupported arithmetic operator is performed.

            This is important to handled exceptions do not cause any unwanted side effects.
            """
            # TODO: add additional traceback info
            self.left_bind = Nil
            self.right_bind = Nil
            raise TypeError("unsupported operation")

        # right and left methods are switched due to operator precedence
        for meth in operators.values():
            def func(self, value):
                return invoked_invalid_operation(self, value)
            func.__name__ = f"__{meth}__"
            from functools import wraps
            setattr(cls, f"__{meth}__", wraps(func)(func))
        setattr(cls, f"__r{method}__", left_infix)
        setattr(cls, f"__{right_method}__", right_infix)

        cls.__doc__ = f"""Subclass of BaseInfix used to create infix functions.
        Examples:
            >>> @<infix factory>
            >>> def divides(a, b):
            ...     return b % a == 0
            ...
            >>> 3 {cls.operator()}divides{cls.right_operator()} 9
            True

        Unsupported operators will always raise an exception.
        """
    def __call__(self, x, y):
        return self.function(x, y)

    def __repr__(self):
        name = self.function.__name__
        left = self.operator()
        right = self.right_operator()
        return f"<infix function '{left}{name}{right}'>"

    @classmethod
    @abstractmethod
    def operator(cls) -> Operator:
        pass

    @classmethod
    @abstractmethod
    def right_operator(cls) -> Operator:
        pass

def operator_method(value: str) -> str:
    method = isinstance(value, str) and operators.get(value)
    if not method:
        ops = ", ".join(map(repr, operators))
        msg = f"value is not an operator, expected one of {ops}"
        if value in ("==", "!=", ">", ">=", ">", "<="):
            msg += f"\ncomparison operator {value} is short circuited and thus not supported"
        raise TypeError(msg)
    return method

def new_infix(operator: Operator, right_operator: Operator | None=None) -> NewInfix:
    return type(
        "Infix", (BaseInfix, ), {"operator": classmethod(lambda cls: operator),
        "right_operator": classmethod(lambda cls: right_operator or operator)}
    )

@overload
def infixed(func: Operator, /, operator: None, *,
    right_operator: Operator | None) -> type[NewInfix]: ...

@overload
def infixed(func: None, /, operator: Operator | None, *,
    right_operator: Operator | None) -> type[NewInfix]: ...

@overload
def infixed(func: Callable, /, operator: Operator | None, *,
    right_operator: Operator | None) -> NewInfix: ...

def infixed(func=None, /, operator: Operator | None=None, *, right_operator: Operator | None=None):
    """Helper function for dynamically creating Infixed functions without having to directly
    subclass BaseInfix.

    Can be used as a decorator using '@infixed' or an operator can be specified
    with '@infixed(<operator>)'. It may also be called directly using
    'infixed(<func>, operator=<operator>)'. Returns a new Infix class with
    the operator methods defined.

    Examples:
        >>> @infixed
        >>> def divides(a, b):
        ...     return b % a == 0
        ...
        >>> 10 |divides| 100
        True
        >>> @infixed('+')
        >>> def strcat(x, y):
        ...     return  str(x) + str(y)
        ...
        >>> 1 +strcat+ 2
        '12'
        >>>
        >>> Infix = infixed("|")
        >>>
        >>> @Infix
        >>> def tee(content, filename):
        ...     print(content)
        ...     with open(filename, "wb+") as file:
        ...         bytes_written = file.write(content)
        ...     return bytes_written
        ...
        >>> bytes_written = 'Hello, World!' |tee| "filename.txt"
        Hello, World!
    """
    match func, operator, right_operator:
        case None, None, None:
            return new_infix("|", "|")
        case str(_), None, None:
            return new_infix(func, func)
        case str(_), _, None:
            return new_infix(func, operator)
        case str(_), None, str(_):
            return new_infix(func, right_operator)
        case None, str(_), str(_):
            return new_infix(operator, right_operator)
        case None, str(_), None:
            return new_infix(operator, operator)
        case _, None, None:
            return new_infix("|", "|")(func)
        case _, str(_), _:
            return new_infix(operator, right_operator)(func)
    raise ValueError(f"{type(func)}, {type(operator)}, {type(right_operator)}")

Infix: NewInfix = new_infix("|")
