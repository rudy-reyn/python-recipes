# 03/23/22
# infix.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Literal, overload, TypeVar
from .utils import Nil

__all__ = "Infix", "infix"

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
                raise AttributeError(f"left hand argument is already bound")
            if self.right_bind is Nil:
                self.left_bind = other
                return self
            argument, self.right_bind = self.right_bind, Nil
            return self(argument, other)

        def right_infix(self, other):
            if self.right_bind is not Nil:
                raise AttributeError(f"right hand argument is already bound")
            if self.left_bind is Nil:
                self.right_bind = other
                return self
            argument, self.left_bind = self.left_bind, Nil
            return self(argument, other)

        # right and left methods are switched due to operator precedence
        setattr(cls, f"__r{method}__", left_infix)
        setattr(cls, f"__{right_method}__", right_infix)

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
def infix(func: Operator, /, op: None, *, rop: Operator | None) -> type[NewInfix]: ...

@overload
def infix(func: None, /, op: Operator | None, *, rop: Operator | None) -> type[NewInfix]: ...

@overload
def infix(func: Callable, /, op: Operator | None, *, rop: Operator | None) -> NewInfix: ...

def infix(func=None, /, operator: Operator | None=None, *, right_operator: Operator | None=None):
    """Helper function for dynamically creating Infixed functions without having to directly
    subclass BaseInfix.

    Can be used as a decorator using '@infix' or an operator can be specified
    with '@infix(<operator>)'. It may also be called directly using
    'infix(<func>, operator=<operator>, r)'. Returns a new Infix class with
    the operator methods defined.

    Examples:
        >>> @infix
        >>> def divides(a, b):
        ...     return b % a == 0
        ...
        >>> 10 |divides| 100
        True
        >>> @infix('+')
        >>> def strcat(x, y):
        ...     return  str(x) + str(y)
        ...
        >>> 1 +strcat+ 2
        '12'
        >>>
        >>> Infix = infix("|")
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
        case _, None, None:
            return new_infix("|", "|")(func)
        case _, str(_), str(_):
            return new_infix(operator, right_operator)(func)
    raise ValueError(infix.__doc__)

Infix = new_infix("|")
