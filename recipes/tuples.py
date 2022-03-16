# 03/11/22
# tuples.py

def Tuple(*fields, **named_fields):
    class TupleFactory(tuple):
        def __new__(cls, *args, **kwargs):
            cls._unnamed = args
            cls._named = tuple(kwargs.items())
            cls._fields = tuple(range(len(args))) + tuple(kwargs)
            for attr, value in kwargs.items():
                if attr.startswith("_"):
                    raise AttributeError(f"private fields are not allowed, got: '{name}'")
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

        def __setattr__(self, attr, value):
            if hasattr(self, "_init") and not hasattr(self, attr):
                raise AttributeError(f"type object 'Tuple' has not attribute '{attr}'")
            if hasattr(self, "_init"):
                raise TypeError(f"cannot set '{attr}' attribute of immutable type 'Tuple'")
            object.__setattr__(self, attr, value)

        def __hash__(self):
            return hash(tuple(self._items()))
    return TupleFactory(*fields, **named_fields)

def items(cls):
     return cls._items()

def fields(cls):
    return cls._fields

def asdict(cls):
    return cls._asdict()
