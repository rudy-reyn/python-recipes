# Python recipes

## Overview

This package includes various potentially useful miscellaneous functions and classes, including:
  * Anonymous types
  * Function signature guards
  * Static function signatures

## Examples

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
>>> factorial(10, 0)   # raises ValueError

```
### recipes.typed

```python3
>>> from recipes import typed

>>> @typed(int, a=int)
>>> def factorial(n, a=1):
...    if n <= 0:
...        return a
...    return factorial(n - 1, n * a)

>>> factorial(-1.0)       # raises TypeError

>>> @typed(int | float, a=int)
>>> def factorial(n, a=1):
...    if n <= 0:
...        return a
...    return factorial(n - 1, n * a)

>>> factorial(-1.0)       # returns 1
1
```
