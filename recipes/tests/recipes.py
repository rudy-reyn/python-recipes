# 04/02/22
# recipes.py
import sys
import pytest
from .. import pipefunc, curry

@pytest.fixture
def factorial():
    @pipefunc
    def factorial(n, a=1):
        if n <= 0:
            return a
        return factorial(n - 1, n * a)
    return factorial

@pytest.fixture
def add():
    @curry
    def add(a, b, c=0):
        return a + b + c
    return add

@pytest.fixture
def add_positional():
    @curry
    def add(a, b, c, /):
        return a + b + c
    return add

def test_pipefunc(factorial):
    assert repr(factorial)
    assert isinstance(factorial, pipefunc)

    with pytest.raises(TypeError):
        pipefunc(None)

    assert factorial(5) == 120
    assert factorial(5, 1) == 120
    assert factorial(5, a=1) == 120
    assert factorial(n=5, a=1) == 120

    # `|` passes the left value as a single argument as `func(arg)`
    assert (5 | factorial) == 120

@pytest.fixture
def curry_helper():
    def helper(function):
        assert repr(function)
        assert isinstance(function, curry)
    return helper

def test_curry(add, add_positional, curry_helper):
    with pytest.raises(TypeError):
        curry(None)
    assert curry_helper(add)
    assert curry_helper(add(1))
    assert add(1)(2)(3) == 6

def test_curry_pos_only(add_positional, curry_helper):
    assert curry_helper(add_positional)
    assert curry_helper(add_positional(1))
    assert curry_helper(add_positional(1, 2))
    assert add_positional(1, 2, 3) == 6

    with pytest.raises(TypeError):
        add_positional(1, 2, c=3)

    with pytest.raises(TypeError):
        add_positional(a=1, b=2, c=3)

    add1 = add_positional(1)
    assert curry_helper(add1)
    add3 = add1(2)
    assert curry_helper(add3)
    assert add3(3) == 6
