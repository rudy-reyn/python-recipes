# 03/16/22
# pipefunc.py
import sys
import pytest
from .. import *

@pytest.fixture
def factorial():
    @pipefunc
    def inner(n, a=1):
        if n <= 0:
            return a
        return inner(n -1, n * a)
    return inner

def test_pipefunc_decorator(factorial):
    @pipefunc(pipe_to_stdin=True)
    def test():
        return

    assert isinstance(factorial, PipeFunc)
    assert isinstance(test, PipeFunc)
    assert isinstance(test, StdinPipe)
    assert isinstance(pipefunc(factorial, pipe_to_stdin=True), StdinPipe)

    with pytest.raises(TypeError):
        @pipefunc(pipe_to_stdin=None)
        def _():
            return

    with pytest.raises(TypeError):
        pipefunc(None)

def test_direct_call(factorial):
    assert factorial(5) == 120
    assert factorial(5, 1) == 120
    assert factorial(5, a=1) == 120
    assert factorial(n=5, a=1) == 120

def test_ror(factorial):
    "`|` passes the left value as a single argument as `func(arg)`"
    assert 5 | factorial == 120

def test_rrshift(factorial):
    "`>>` unpacks the left value as `func(*args)`"
    assert (5, ) >> factorial == 120
    assert (5, 1) >> factorial == 120

    with pytest.raises(TypeError):
        assert 5 >> factorial == 120

def test_rand(factorial):
    "`&` unpacks the left value as `func(**kwargs)`"
    assert {'n': 5} & factorial == 120
    assert {'n': 5, 'a': 1} & factorial == 120

def test_rtruediv(factorial):
    """`/` passes the left value as `func(*args, **kwargs)`
    if args is an iterable, otherwise as `func(args, **kwargs)`"""
    assert (5, {}) / factorial == 120
    assert ((5, ), {}) / factorial == 120

def test_rfloordiv(factorial):
    "`//` always unpacks args regardless of type"
    assert ((5, ), {'a': 1}) // factorial == 120

    with pytest.raises(TypeError):
        assert 5 // factorial == 120

def test_rmod(factorial):
    "`%` is passed a 2-tuple, and never unpacks args regardless of type"
    assert (5, {}) % factorial == 120

    with pytest.raises(TypeError):
        assert (5, {}) // factorial == 120

    with pytest.raises(TypeError):
        assert (5, {}) // factorial == 120

@pytest.fixture
def zen():
    import io
    from contextlib import redirect_stdout
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        import this
    return buffer.getvalue()

@pytest.fixture
def enumerated_zen(zen):
    enumerated = ""
    for i, line in enumerate(zen.splitlines()):
        enumerated += f"{i} {line}\n"
    return enumerated

@pytest.fixture
def enumerate_lines():
    @pipefunc(pipe_to_stdin=True)
    def inner():
        enumerated = ""
        for i, line in enumerate(sys.stdin):
            enumerated += f"{i} {line}"
        return enumerated
    return inner

def test_stdin(zen, enumerate_lines, enumerated_zen):
    assert zen | enumerate_lines == enumerated_zen
