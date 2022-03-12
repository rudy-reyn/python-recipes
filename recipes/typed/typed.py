# 03/10/22
# typed.py
from .. import Guard
from types import UnionType
from typing import _UnionGenericAlias as _UnionGenericAlias
from functools import wraps


class ArgTypeGuard:
    def __init__(self, grd):
        Type = type | UnionType | _UnionGenericAlias
        if grd != ... and not isinstance(grd, Type):
            raise TypeError(f"argument guard '{grd}' must be an ellipsis or a type")

        self.type = grd
        self.__name__ = repr(self)

    def __call__(self, arg):
        return self.type == ... or isinstance(arg, self.type)

    def __repr__(self):
        return repr(self.type)

class Typed(Guard):
    def __init__(self, func, *arg_types, returns=object, **kwarg_types):
        sig = dict(enumerate(arg_types)) | kwarg_types

        arg_guards = tuple(ArgTypeGuard(t) for t in arg_types)
        kwarg_guards = {k: ArgTypeGuard(t) for k, t in kwarg_types.items()}
        super(self.__class__, self).__init__(func, *arg_guards, **kwarg_guards)

        self.signature = {k: v for k, v in sig.items() if v != ...}
        self.returns = ArgTypeGuard(returns)

    def __repr__(self):
        return f"<typed function {self.func.__name__} at {id(self)}>"

    def __call__(self, *args, **kwargs):
        result = super(self.__class__, self).__call__(*args, **kwargs)
        if not self.returns(result):
            exp = repr(self.returns)
            got = repr(type(result))
            raise TypeError(f"invalid return type for {self}, expected: {self.returns}, got: {got}")
        return result

    def _func_call_err(self, position, key, grd, arg):
        raise TypeError(f"invalid value for {position} argument {key}, expected type '{grd.type}', got: '{type(arg)}'")

    def _init_guards(self, grds, position):
        pass

def typed(*arg_types, **kwarg_types):
    def wrapper(func):
        return wraps(func)(Typed(func, *arg_types, **kwarg_types))
    return wrapper
