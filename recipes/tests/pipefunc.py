# 03/16/22
# pipefunc.py
import sys
import pytest
from .. import pipefunc

@pytest.fixture
def factorial():
    @pipefunc
    def factorial(n, a=1):
        if n <= 0:
            return a
        return factorial(n - 1, n * a)
    return factorial

def test_repr(factorial):
    assert repr(factorial)

def test_instance(factorial):
    assert isinstance(factorial, pipefunc)

    with pytest.raises(TypeError):
        pipefunc(None)

def test_direct_call(factorial):
    assert factorial(5) == 120
    assert factorial(5, 1) == 120
    assert factorial(5, a=1) == 120
    assert factorial(n=5, a=1) == 120

def test_ror(factorial):
    "`|` passes the left value as a single argument as `func(arg)`"
    assert (5 | factorial) == 120
