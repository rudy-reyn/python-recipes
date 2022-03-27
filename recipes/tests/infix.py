#!/usr/bin/env python3
# 03/27/22
# tests/infix.py
# rudy@recipes
from typing import Iterable
from abc import ABC
import pytest
from .. import infixed, BaseInfix, operator_method, new_infix, Nil

@pytest.fixture
def operators():
    return {
        "&": "and", "|": "or", "^": "xor",
        "+": "add", "-": "sub", "*": "mul",
        "@": "matmul", "/": "tuediv", "//": "floordiv",
        "%": "mod", "<<": "lshift", ">>": "rshift"
    }


def test_invalid_subclass():
    with pytest.raises(TypeError):
        class Infix(BaseInfix):
            pass

def test_operator_method(operators):
    for op in operators:
        assert operator_method(op) == operators[op]

def test_operator_method_comp_ops():
    comp_ops = ("==", "!=", ">", ">=", ">", "<=")
    for op in comp_ops:
        try:
            operator_method(op)
        except TypeError as terr:
            assert len(terr.args) == 1
            assert f"comparison operator {op}" in terr.args[0]
        else:
            assert False, f"TypeError expected for comparison operator{op}"

def tets_invalid_operator():
    for op in (None, 3, ["&", "|"], "!", "@@"):
        with pytest.raises(TypeError):
            operator_method(op)

def test_new_infix():
    Infix = new_infix("|", "-")
    assert Infix.operator() == "|"
    assert Infix.right_operator() == "-"
    assert hasattr(Infix, "__ror__")
    assert hasattr(Infix, "__sub__")
    assert Infix.mro() == [Infix, BaseInfix, ABC, object]

def test_infix_no_args():
    @infixed
    def concat(x, y):
        return f"{x}{y}"

    assert 1 |concat| 2 == "12"

def test_infix_single_operator_kwarg():
    import builtins

    @infixed("*")
    def zip(A, B):
        return list(builtins.zip(A, B))

    assert [1, 2] *zip* ["a", "b"] == [(1, "a"), (2, "b")]

def test_infix_operator_args():
    @infixed("+", "+")
    def ext(xs, x):
        if isinstance(x, Iterable):
            return list(xs) + list(x)
        return list(xs) + [x]

    assert [1, 2, 3] +ext+ [4, 5] == [1, 2, 3, 4, 5]
    assert ext.left_bind is Nil
    assert ext.right_bind is Nil
    assert [1, 2, 3] +ext+ 4 == [1, 2, 3, 4]
    assert ext.left_bind is Nil
    assert ext.right_bind is Nil

def test_argument_bindings():
    @infixed("+", "-")
    def ext(xs, x):
        if isinstance(x, Iterable):
            return list(xs) + list(x)
        return list(xs) + [x]

    with pytest.raises(TypeError):
        assert [1, 2, 3] +ext+ [4, 5] == [1, 2, 3, 4, 5]

    assert ext.left_bind is Nil
    assert ext.right_bind is Nil

    assert [1, 2, 3] +ext- [4, 5] == [1, 2, 3, 4, 5]
    assert [1, 2, 3] +ext- 4 == [1, 2, 3, 4]

def test_infix_single_kwarg():
    @infixed(operator="%")
    def divides(x, y):
        return y % x == 0
    assert 10 %divides% 20
    assert not 11 %divides% 20

def test_infix_operators_kwargs():
    @infixed(operator="&", right_operator="|")
    def xor(x, y):
        return bool(x) ^ bool(y)

    assert 1 &xor| 0
    assert not 1 &xor| 1

def test_infix_operators_kwargs():
    @infixed(operator="&", right_operator="|")
    def xor(x, y):
        return bool(x) ^ bool(y)

    assert 1 &xor| 0
    assert not 1 &xor| 1

def test_infix():
    @infixed("<<", right_operator=">>")
    def O(a, b):
        return min(a, b), max(a, b)

    cartesian_product = lambda A, B: ((a, b) for a in A for b in B)
    prod = infixed(cartesian_product, "*")
