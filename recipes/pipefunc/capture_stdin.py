# 03/16/22
# capture_stdin.py
import sys
import io
from contextlib import contextmanager
from .pipefunc import PipeFunc

__all__ = "as_sdtin", "StdinPipe"

Stream = io.BytesIO | io.StringIO
BytesLike = bytes | bytearray
ReplacementStdin = str | Stream | BytesLike | None

@contextmanager
def as_stdin(obj: ReplacementStdin=None, /):
    original_stdin = sys.stdin
    try:
        if isinstance(obj, str) or obj is None:
            sys.stdin = io.StringIO(obj)
        elif isinstance(obj, bytes | bytearray):
            sys.stdin  = io.BytesIO(obj)
        elif isinstance(obj, Stream):
            sys.stdin = obj
        yield sys.stdin
    finally:
        sys.stdin = original_stdin

class StdinPipe(PipeFunc):
    def __call__(self, text, *args, **kwargs):
        with as_stdin(text):
            result = self.func(*args, **kwargs)
        return result
