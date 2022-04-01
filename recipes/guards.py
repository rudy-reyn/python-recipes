# 04/01/22
# guards.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Literal, overload, TypeVar, Callable

__all__ = "BaseGuard", "Guard", "PartialGuard", "guard"

T = TypeVar("T")

GuardFunction = Callable[[T], bool]

def valid_classinfo(classinfo: Any):
    try:
        isinstance(..., classinfo)
    except TypeError:
        return False
    return True

class BaseGuard:
    """Abstract base class for creating guards.

    Provides guard property method used to validate given values.
    """

    __slots__ = "_guard"

    def __init__(self, guard: GuardFunction | None=None):
        # done to keep mypy happy, but isn't actually necessary
        if guard is None:
            guard = lambda _: True
        self.guard = guard

    def __repr__(self):
        return f"{self.__class__.__name__}{self.value, self.guard.__name__}"

    @property
    def guard(self) -> GuardFunction:
        self.guard = self._guard # ensures self._guard wasn't changed.
        return self._guard

    @guard.setter
    def guard(self, guard) -> None:
        if guard is None:
            self._guard = lambda value: True
        elif valid_classinfo(guard):
            self._guard = lambda value: isinstance(value, guard)
        elif callable(guard):
            self._guard = guard
        else:
            raise TypeError(
                "Guard must be None, a type, UnionType, tuple of types, or other callable object"
            )

class Guard(BaseGuard):
    __slots__ = "_guard", "_value"

    def __init__(self, value, guard=None):
        self.guard = guard
        self.value = value

    def __repr__(self):
        return f"Guard{self.value, self.guard.__name__}"

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T) -> None:
        if self.guard is not None and not self.guard(value):
            raise ValueError("Value does not pass guard")
        self._value = value

class PartialGuard(BaseGuard):
    "Used to provide a __ror__ method for alternative guard construction."

    __slots__ = "_guard"

    def __call__(self, value: T) -> Guard:
        return Guard(value, self.guard)

    def __ror__(self, value: T) -> Guard:
        return self(value)

@overload
def guard(value: GuardFunction, guard: Literal[None]) -> PartialGuard:
    ...

@overload
def guard(value: T, guard: GuardFunction) -> Guard:
    ...

def guard(value, guard=None) -> PartialGuard | Guard:
    """A generic helper function for creating guards.

    If the value is meant to be a literal callable without a guard,
    then Guard or PartialGuard should be called directly instead."""

    if callable(value) or valid_classinfo(value) and guard is None:
        return PartialGuard(value)
    return Guard(value, guard)
