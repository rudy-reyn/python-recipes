# Python recipes

## Overview

This package includes various potentially useful miscellaneous functions and classes, including:
  * Anonymous types
  * Function signature guards
  * Static function signatures
  * Function pipes

## Examples

### recipes.pipefunc
```python3
>>> from recipes import pipefunc

>>> @pipefunc
>>> def factorial(n, a=1):
...     if n <= 0:
...         return a
...     return factorial(n - 1, n * a)

>>> factorial(5)
120

>>> 5 | factorial
120
```

In addition to standard pipes, different operators can be used to unpack arguments.
These are the most useful when piping the output of another function rather than being used
directly.
  * `|`  passes the left value as a single argument as `func(arg)`
  * `>>` unpacks the left value as `func(*args)`
  * `&`  unpacks the left value as `func(**kwargs)`
  * `/`  passes the left value as `func(*args, **kwargs)` if args is an iterable, otherwise as `func(args, **kwargs)`. Note that this includes strings.
  * `//` passes the left value as `func(*args, **kwargs)` regardless of arg type
  * `%`  passes the left value as `func(args, **kwargs)` regardless of arg type

```python3
>>> (5, ) >> factorial
120
>>> {"n": 5, "a": 1} & factorial
120
>>> (5, {"a": 1}) / factorial
120
>>> (5, {"a": 1}) // factorial
TypeError: cannot unpack non-iterable int object
>>> ((5, ), {"a": 1}) // factorial
120
>>> ((5, ), {}) % factorial
TypeError: '<=' not supported between instances of 'tuple' and 'int'
>>> (5, {}) % factorial
120
```

### recipes.tuples
```python3
>>> from recipes import Tuple

>>> ab = Tuple(a=1, b=2)
>>> print(ab)
(a=1, b=2)

>>> print(Tuple(1, 2, c=3))
(1, 2, c=3)

>>> xy = Tuple(x=1, y=2)
>>> print(xy[0], xy[1])
1 2
>>> print(xy.x, xy.y)
1 2
>>> print(*xy)
1 2
```

### recipes.guards

```python3
>>> from recipes import guard

>>> @guard(lambda n: n >= 0, lambda a: a > 0)
>>> def factorial(n, a=1):
...    if n == 0:
...        return a
...    return factorial(n - 1, n * a)

>>> factorial(-1)       # raises ValueError
>>> factorial(10, 0)    # raises ValueError

# Ellipsis can be used as a wildcard
>>> @guard(lambda a: a != 0, ..., lamnda c: c != 0):
>>> def adder(a, b, c):
...     return a + b + c

>>> adder(1, 0, 2)
3


```
### recipes.typed

```python3
>>> from recipes import typed

>>> @typed(int, a=int)
>>> def factorial(n, a=1):
...    if n <= 0:
...        return a
...    return factorial(n - 1, n * a)

>>> factorial(-1.0)        # raises TypeError

>>> @typed(int | float, ..., str)
>>> def display_pair(a, b):
...    print(a, b)

>>> display_pair(1, "2", "3")
1 2 3

>>> display_pair(1, 2, 3) # raises TypeError
```
