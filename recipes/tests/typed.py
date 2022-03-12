# 03/11/22
# tests.py
import pytest
from .. import typed, Typed

def test_return_type():
    @typed(int, a=int, returns=int)
    def fact(n, a=1):
        if n <= 0:
            return ""
        return fact(n - 1, a=n * a)
    with pytest.raises(TypeError) as terr:
        fact(3, a=1)

def test_positional_ellipsis():
    @typed(..., ...)
    def add(n, a):
        return n + a
    add(1, 1)

def test_keyword_ellipsis():
    @typed(int, a=...)
    def add(n, a):
        return n + a
    add(1, a=1)

def test_ellipsis():
    @typed(int, ..., ..., float, e=...)
    def add(a, b, c, d, e=1):
        return a + b + c + d + e
    add(1, 2, 3, 4.0)

def test_invalid_pos_arg():
    @typed(int, a=int, returns=int)
    def fact(n, a=1):
        if n <= 0:
            return a
        return fact(n - 1, a=n * a)
    with pytest.raises(TypeError) as terr:
        fact("", a=1)

def test_multiple_pos_args():
    @typed(int, a=int, returns=int)
    def fact(n, a=1):
        if n <= 0:
            return a
        return fact(n - 1, a=n * a)
    with pytest.raises(TypeError) as terr:
        fact("", "", a=1)

def test_invalid_keyword_arg():
    @typed(int, a=int, returns=int)
    def fact(n, a=1):
        if n <= 0:
            return a
        return fact(n - 1, a=n * a)
    with pytest.raises(TypeError) as terr:
        fact(n=1, a=1)

def test_invalid_keyword_arg_type():
    @typed(int, a=int, returns=int)
    def fact(n, a=1):
        if n <= 0:
            return a
        return fact(n - 1, a=n * a)
    with pytest.raises(TypeError) as terr:
        fact(1, a="")

def test_invalid_signature():
    with pytest.raises(TypeError) as terr:
        @typed(5, a=int, returns=int)
        def fact(n, a=1):
            if n <= 0:
                return a
            return fact(n - 1, a=n * a)

def test_invalid_keyword_signature():
    with pytest.raises(TypeError) as terr:
        @typed(int, a="", returns=int)
        def fact(n, a=1):
            if n <= 0:
                return a
            return fact(n - 1, a=n * a)
