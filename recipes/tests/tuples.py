# 03/11/22
# tests.py
import pytest
from .. import *

@pytest.fixture
def point():
    return Tuple(1, a=2, b=3)

def test_multiple_instances(point):
    point1 = Tuple(x=1, y=2)
    assert repr(point) == "(1, a=2, b=3)",  f"'{point!r}' == '{point}' and != '(1, a=2, b=3)'"
    assert repr(point1) == "(x=1, y=2)", f"'{point1!r}' == '{point1}' and != '(x=1, y=2)'"
    assert tuple(point) != tuple(point1)

def test_fields(point):
    assert point._fields == fields(point) == (0, "a", "b")

def test_items(point):
    assert tuple(point._items()) == tuple(items(point)) == ((0, 1), ("a", 2), ("b", 3))

def test_asdict(point):
    assert dict(point._items()) == asdict(point) == point._asdict()

def test_hasattrs(point):
    point2 = Tuple(1, c=2)
    assert hasattr(point, "a") and hasattr(point, "b") and hasattr(point2, "c")\
    and not hasattr(point, "c") and not hasattr(point2, "a") and not hasattr(point2, "b")

def test_get_by_index(point):
    assert point[0] == 1 and point[1] == 2 and point[2] == 3

def test_isinstance_tuple(point):
    assert isinstance(point, tuple)

def test_as_dict_key(point):
    assert dict(point=None), f"Fails as dictionary key"
    assert hash(point), f"hash(point) fails"

def test_match_case_tests(point):
    msg = lambda pattern: f"{pattern} fails pattern match"
    match point:
        case (1, 2, 3): ...
        case _:
            assert False, msg(f"(1, 2, 3)")
    match point:
        case (1, 2, 4): assert False, msg(f"(1, 2, 4)")
        case _:
            ...
    match point:
        case (1, _, 3): ...
        case _:
            assert False, msg(f"(1, _, 3)")
    match point:
        case (_, _, 3): ...
        case _:
            assert False, msg(f"(_, _, 3)")
