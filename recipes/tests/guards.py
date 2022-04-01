# 03/11/22
# tests.py
import pytest
from .. import BaseGuard, Guard, PartialGuard, guard

@pytest.fixture
def is_even():
    return lambda n: n % 2 == 0

def test_init_BaseGuard():
    base = BaseGuard(lambda _: True)
    with pytest.raises(TypeError):
        base._guard = ...
        base.guard
    assert isinstance(base, BaseGuard)

    base._guard = ...
    with pytest.raises(TypeError):
        base.guard

def test_init_PartialGuard():
    with pytest.raises(TypeError):
        PartialGuard(...)
    assert PartialGuard(lambda: True)

def test_PartialGuard(is_even):
    even_partial = PartialGuard(is_even)
    assert isinstance(even_partial(2), Guard)
    assert isinstance(2 | even_partial, Guard)
    with pytest.raises(TypeError):
        even_partial.guard = 10

def test_init_Guard(is_even):
    assert Guard(..., None)
    assert Guard(..., None).value == ...
    assert Guard(..., None).guard(...) is True
    with pytest.raises(TypeError):
        Guard(..., ...)
    with pytest.raises(TypeError):
        Guard(..., Guard(...))
    with pytest.raises(ValueError):
        Guard(1, is_even)

@pytest.fixture
def guard_helper():
    def helper(guarded, *, initial, invalid, new):
        assert isinstance(guarded, Guard)
        assert callable(guarded.guard)
        assert guarded.value == initial
        with pytest.raises(ValueError):
            guarded.value = invalid
        guarded.value = new
        assert guarded.value == new
        return True
    return helper

def test_Guard(is_even, guard_helper):
    assert guard_helper(Guard(0, is_even), initial=0, invalid=1, new=2)

@pytest.fixture
def list_of_types():
    return (int, float, complex), (list, tuple, (set, dict)), str | None

def test_Guard_from_classinfo(guard_helper, list_of_types):
    assert guard_helper(Guard([], list_of_types), initial=[], invalid=..., new={})

def test_guard_helper_function(guard_helper, is_even, list_of_types):
    even_partial = guard(is_even)
    assert isinstance(even_partial, PartialGuard)

    assert guard_helper(0 | even_partial, initial=0, invalid=1, new=2)
    assert guard_helper(guard([], list_of_types), initial=[], invalid=..., new=())
    assert guard_helper(guard([], list_of_types), initial=[], invalid=..., new=None)
