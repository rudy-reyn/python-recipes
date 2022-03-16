from .pipefunc import *
from .capture_stdin import StdinPipe

__all__ = "pipefunc", "StdinPipe", "PipeFunc"

def pipefunc(func=None, /, *, pipe_to_stdin=False):
    """decorator for creating a pipeable function

    returns:
        PipeFunc(func) if func is passed and pipe_to_stdin is False,
        StdinPipe(func) if func is passed and pipe_to_stdin is False,
        StdinPipe if func is None and pipe_to_stdin and is True.
    """
    if callable(func) and pipe_to_stdin is False:
        return PipeFunc(func)
    elif callable(func) and pipe_to_stdin is True:
        return StdinPipe(func)
    elif func is None and pipe_to_stdin is True:
        return StdinPipe
    raise TypeError(f"pipefunc: {pipefunc.__doc__}")
