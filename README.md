# Python recipes

## Overview

This package includes various potentially useful miscellaneous functions and classes, including:
  * Anonymous types
  * Variable guards
  * Infix operators
  * Function pipes

## Examples

## infix
Includes `infixed` function factory for creating infixed functions.
These can be used to create pseudo binary operators.

```python3
>>> @infixed
>>> def divides(a, b):
...     return b % a == 0
...
>>> 10 |divides| 100
True
>>> @infixed('+')
>>> def strcat(x, y):
...     return  str(x) + str(y)
...
>>> 1 +strcat+ 2
'12'
>>>
>>> Infix = infixed("|")
>>>
>>> @Infix
>>> def tee(content, filename):
...     print(content)
...     with open(filename, "wb+") as file:
...         bytes_written = file.write(content)
...     return bytes_written
...
>>> bytes_written = 'Hello, World!' |tee| "filename.txt"
Hello, World!
```

### guards
```python3
>>> from recipes import guard
>>>
>>> natural_num = guard(1, lambda n: n > 0)
>>> natural_num.value
1
>>> zero.value = -1
ValueError("Value does not pass guard")
```

Guards can also accept types

```python3
>>> n = guard(0, (int, float, complex))
>>> n.value
0
>>> n.value = "0"
ValueError("Value does not pass guard")
```

### pipefunc
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

### tuples
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
