# 03/11/22
# tests.py
import pytest
from .. import guard

def test_signature():
    @guard(lambda n: n >= 0, a=lambda a: a > 0)
    def fact(n, a=1):
        if n <= 0:
            return a
        return fact(n - 1, a=n * a)
    fact(1, a=1)
    with pytest.raises(ValueError) as terr:
        fact(-1, a=1)

def test_positional_ellipsis():
    @guard(..., ...)
    def add(n, a):
        return n, a
    add("", 1)

def test_posiional():
    @guard(lambda n: n == 1)
    def one(n):
        return n
    one(1)
    with pytest.raises(ValueError) as terr:
        one(2)

def test_invalid_num_posiional():
    @guard(lambda a: True, lambda b: True)
    def mul(a, b):
        return a * b
    mul(1, 2)
    with pytest.raises(TypeError) as terr:
        mul(2)

def test_keyword():
    @guard(lambda n: n == 1, a=lambda a: a != 0)
    def minus(n, a=10):
        return n - a
    minus(1, a=10)
    with pytest.raises(ValueError) as terr:
        minus(1, a=0)
