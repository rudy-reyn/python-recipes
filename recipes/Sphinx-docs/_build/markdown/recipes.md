# recipes package

## Subpackages


* [recipes.tests package](recipes.tests.md)


    * [Submodules](recipes.tests.md#submodules)


    * [recipes.tests.guards module](recipes.tests.md#module-recipes.tests.guards)


    * [recipes.tests.infix module](recipes.tests.md#module-recipes.tests.infix)


    * [recipes.tests.recipes module](recipes.tests.md#module-recipes.tests.recipes)


    * [recipes.tests.tuples module](recipes.tests.md#module-recipes.tests.tuples)


    * [Module contents](recipes.tests.md#module-recipes.tests)


## Submodules

## recipes.guards module


### _class_ recipes.guards.BaseGuard(guard=None)
Bases: `object`

Abstract base class for creating guards.

Provides guard property method used to validate given values.


#### \__init__(guard=None)

#### _property_ guard(_: Callable[[recipes.guards.T], bool_ )

* **Return type**

    `Callable`[[`TypeVar`(`T`)], `bool`]



### _class_ recipes.guards.Guard(value, guard=None)
Bases: `recipes.guards.BaseGuard`


#### \__init__(value, guard=None)

#### _property_ value(_: recipes.guards._ )

* **Return type**

    `TypeVar`(`T`)



### _class_ recipes.guards.PartialGuard(guard=None)
Bases: `recipes.guards.BaseGuard`

Used to provide a __ror__ method for alternative guard construction.


### recipes.guards.guard(value: Callable[[recipes.guards.T], bool], guard: Literal[None])

### recipes.guards.guard(value: recipes.guards.T, guard: Callable[[recipes.guards.T], bool])
A generic helper function for creating guards.

If the value is meant to be a literal callable without a guard,
then Guard or PartialGuard should be called directly instead.


* **Return type**

    `UnionType`[`PartialGuard`, `Guard`]


## recipes.infix module


### _class_ recipes.infix.BaseInfix(function)
Bases: `abc.ABC`

Infix Base class used to instantiate new Infix subclasses using specified operators.

The operator and left operator classmethods must be defined and return a valid python
operator, which includes: ‘&’, ‘|’, ‘^’, ‘+’, ‘-’, ‘\*’, ‘@’, ‘/’, ‘//’, ‘%’, ‘<<’, ‘>>’.

Short circuited operators are not supported as specific right and left magic methods do not
exist. These include: ‘==’, ‘!=’, ‘>’, ‘>=’, ‘>’, ‘<=’.

Examples:

    ```python
    >>> class Infix(BaseInfix):
    ...     @classmethod
    ...     def operator(cls):
    ...         return "|"
    ...     @classmethod
    ...     def right_operator(cls):
    ...         return "|"
    ...
    >>> @Infix
    >>> def divides(a, b):
    ...     return b % a == 0
    ...
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


#### \__init__(function)

#### _abstract classmethod_ operator()

* **Return type**

    `Literal`[’&’, ‘|’, ‘^’, ‘+’, ‘-’, ‘\*’, ‘@’, ‘/’, ‘//’, ‘%’, ‘<<’, ‘>>’]



#### _abstract classmethod_ right_operator()

* **Return type**

    `Literal`[’&’, ‘|’, ‘^’, ‘+’, ‘-’, ‘\*’, ‘@’, ‘/’, ‘//’, ‘%’, ‘<<’, ‘>>’]



### _class_ recipes.infix.Infix(function)
Bases: `recipes.infix.BaseInfix`

Subclass of BaseInfix used to create infix functions.
Examples:

```python
>>> @<infix factory>
>>> def divides(a, b):
...     return b % a == 0
...
>>> 3 |divides| 9
True
```

Unsupported operators will always raise an exception.


#### _classmethod_ operator()

#### _classmethod_ right_operator()
## recipes.recipes module


### _class_ recipes.recipes.curry(func, \*args, \*\*kwargs)
Bases: `recipes.recipes.Function`

A decorator for currying functions.

```python
>>> @curry
>>> def add(a, b, c, d=0):
...     return a + b + c
...
>>> add(5, 15)
<curried function add at 0x{id}>
>>> add(100)
120
```


#### \__init__(func, \*args, \*\*kwargs)

### _class_ recipes.recipes.pipefunc(func)
Bases: `recipes.recipes.Function`

A decorator for creating bash or R style function pipes.

```python
>>> @pipefunc
>>> def factorial(n, a=1):
...     if n <= 0:
...         return a
...     return factorial(n - 1, n * a)
...
>>> 5 | factorial
120
```


#### \__init__(func)
## recipes.tuples module


### _class_ recipes.tuples.Tuple(\*fields, \*\*named_fields)
Bases: `object`


### recipes.tuples.anonymous_tuple(\*fields, \*\*named_fields)
Anonymous tuple class factory function.

Used to create Anonymous tuples that retain the functionality of
builtin python tuples while introducing named attributes.

Examples:

    ```python
    >>> Tuple(0, x=1, y=2)
    (0, x=1, y=2)
    >>> tup = Tuple(x=1, y=2, z=3)
    >>> print(tup)
    (x=1, y=2, z=3)
    >>> x, y, z = tup
    >>> print(x, y, z)
    1 2 3
    >>> tup[0], tup[1], tup[3]
    1, 2, 3
    ```


* **Return type**

    TupleFactory



### recipes.tuples.asdict(cls)

### recipes.tuples.fields(cls)

### recipes.tuples.items(cls)
## recipes.utils module


### recipes.utils.require(predicate, error=Exception())

### recipes.utils.singleton(cls)
## Module contents
