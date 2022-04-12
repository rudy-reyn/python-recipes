# 04/02/22
# recipes.py
import sys
import re
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
def generic_message():
    return r"Could not bind function arguments for .*:"

@pytest.fixture
def curry_repr():
    return re.compile(r"<curried function <?\w+>? at 0x[a-f0-9]+>")

@pytest.fixture
def curry_helper():
    def helper(func):
        return bool(repr(func)) and isinstance(func, curry)
    return helper

def test_repr(curry_repr):
    func = repr(curry(lambda a, b: (a, b)))

    @repr
    @curry
    def func1(a, b, /):
        return a, b

    @repr
    @curry
    def func2(*, a, b):
        return a, b

    assert curry_repr.match(func), func
    assert curry_repr.match(func1), func1
    assert curry_repr.match(func2), func2

def test_curry(curry_helper):
    @curry
    def add(a, b, c):
        return a + b + c

    with pytest.raises(TypeError):
        curry(None)

    assert curry_helper(add), add
    assert curry_helper(add(1)), add

    assert add(1, 2, 3) == add(1, 2)(3) == add(1)(2, 3) == add(1)(2)(3) == add(a=1, b=2, c=3) == 6

    with pytest.raises(TypeError) as exc_info:
        add(1, 2, 3, 4, 5)

    add1 = add(1)
    assert curry_helper(add1)
    add3 = add1(2)
    assert curry_helper(add3)
    assert add3(c=3) == 6

def test_curry_pos_only(curry_helper, generic_message):
    @curry
    def add(a, b, c, /):
        return a + b + c

    assert curry_helper(add)
    assert curry_helper(add(1))
    assert curry_helper(add(1, 2))
    assert add(1, 2, 3) == 6

    msg = "parameter is positional only, but was passed as a keyword"
    pos_only_message = lambda letter: f"{generic_message} '{letter}' {msg}"

    expected = pos_only_message("c")

    with pytest.raises(TypeError, match=expected) as exc_info:
        add(1, 2, c=3)

    expected = pos_only_message("a")
    with pytest.raises(TypeError, match=expected) as exc_info:
        add(a=1, b=2, c=3)

    add1 = add(1)
    assert curry_helper(add1)
    add3 = add1(2)
    assert curry_helper(add3)
    assert add3(3) == 6

def test_keyword_only(curry_helper, generic_message):
    @curry
    def add(*, a, b, c,):
        return a + b + c

    assert curry_helper(add)
    assert curry_helper(add(a=1))
    assert curry_helper(add(a=1, b=2))
    assert add(a=1, b=2, c=3) == 6

    expected = f"{generic_message} too many positional arguments"

    with pytest.raises(TypeError, match=expected) as exc_info:
        add(1, 2, 3)

    with pytest.raises(TypeError, match=expected) as exc_info:
        add(1, b=2, c=3)

    add1 = add(a=1)
    assert curry_helper(add1)
    add3 = add1(b=2)
    assert curry_helper(add3)
    assert add3(c=3) == 6
