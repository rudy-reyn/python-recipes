# 03/10/22
# guards.py
from functools import wraps

class Guard:
    def __init__(self, func, *guards, **kw_guards):
        self.func = func
        self.name = func.__name__
        self.req = len(guards)
        self.req_kw = len(kw_guards)

        self._init_guards(guards, "Positional")
        self._init_guards(kw_guards.values(), "Keyword")
        self.guards = guards
        self.kw_guards = kw_guards

    def __repr__(self):
        return f"<guarded {self.func.__name__}>"

    def __call__(self, *args, **kwargs):
        self._require_valid_num_args(*args, **kwargs)
        self._valid_func_call(zip(range(self.req), self.guards, args), "positional")
        self._valid_func_call(((k, self.kw_guards[k], kwargs[k]) for k in kwargs), "keyword")
        return self.func(*args, **kwargs)

    def _init_guards(self, grds, position):
        for grd in grds:
            if grd != ... and not callable(grd):
                raise TypeError(f"{position} argument guard {grd} must be an ellipsis or a function")

    def _require_valid_num_args(self, *args, **kwargs):
        if len(args) != self.req:
            raise TypeError(self._arg_len_err(self.req, len(args), "positional"))
        if kwargs.keys() - self.kw_guards.keys():
            raise TypeError(self._arg_len_err(self.req_kw, len(kwargs), "keyword"))

    def _arg_len_err(self, req, passed, position):
        s = "" if req != 1 else "s"
        were = "were" if passed != 1 else "was"
        return f"{self!r} takes {req} {position} argument{s} but {passed} {were} given"

    def _valid_func_call(self, passed_args, position):
        for i, grd, arg in passed_args:
            if grd != ...:
                if not grd(arg):
                    raise self._func_call_err(position, i, grd, arg)

    def _func_call_err(self, position, key, grd, arg):
        return ValueError(f"Invalid value for {position} argument {key} with guard {grd.__name__}: {arg}")

def guard(*guards, **kw_guards):
    def wrapper(func):
        return wraps(func)(Guard(func, *guards, **kw_guards))
    return wrapper
