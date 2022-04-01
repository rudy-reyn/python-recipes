# 03/11/22
# tuples.py
from __future__ import annotations
from typing import Iterable, Any

Identifier = str

def anonymous_tuple(*fields, **named_fields) -> "TupleFactory":
    """Anonymous tuple class factory function.

    Used to create Anonymous tuples that retain the functionality of
    builtin python tuples while introducing named attributes.

    Examples:
        >>> Tuple(0, x=1, y=2)
        (0, x=1, y=2)
        >>> tup = Tuple(x=1, y=2, z=3)
        >>> print(tup)
        (x=1, y=2, z=3)
        >>> x, y, z = tup
        >>> print(x, y, z)
        1 2 3
        >>> tup[0], tup[1], tup[3]
        1, 2, 3

    """
    class TupleFactory(tuple):
        def __new__(cls, *args: Any, **kwargs: dict[Identifier, Any]):
            cls._unnamed = args
            cls._named = tuple(kwargs.items())
            cls._fields = tuple(range(len(args))) + tuple(kwargs)
            for attr, value in kwargs.items():
                if attr.startswith("_"):
                    raise AttributeError(f"private fields are not allowed, got: '{attr}'")
                setattr(cls, attr, value)
            cls._init = True
            return tuple.__new__(TupleFactory, args + tuple(kwargs.values()))

        def __repr__(self):
            rep = ", ".join(
                    f"{field}={value}"
                if not
                    isinstance(field, int)
                else
                    str(value)
                for field, value
                    in self._items())
            return f"({rep})"

        def _items(self):
            yield from zip(self._fields, self)

        def _asdict(self):
            return dict(self._items())

        def __setattr__(self, attr: Identifier, value: Any):
            if hasattr(self, "_init") and not hasattr(self, attr):
                raise AttributeError(f"type object 'Tuple' has not attribute '{attr}'")
            if hasattr(self, "_init"):
                raise TypeError(f"cannot set '{attr}' attribute of immutable type 'Tuple'")
            object.__setattr__(self, attr, value)

        def __hash__(self):
            return hash(tuple(self._items()))

    return TupleFactory(*fields, **named_fields)

# Helper class for test compatibility.
class Tuple:
    def __new__(cls, *fields, **named_fields):
        return anonymous_tuple(*fields, **named_fields)

def items(cls):
     return cls._items()

def fields(cls):
    return cls._fields

def asdict(cls):
    return cls._asdict()
