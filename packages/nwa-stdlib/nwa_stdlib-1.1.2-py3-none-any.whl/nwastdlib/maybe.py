#  Copyright 2019 SURF.
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from functools import reduce
from typing import Any, Callable, ClassVar, Generic, Iterable, Optional, Type, TypeVar

from .f import const, identity

α = TypeVar("α")
β = TypeVar("β")


class Maybe(Generic[α], metaclass=ABCMeta):
    """The Maybe data type to represent an optional value."""

    Nothing: ClassVar[Type[Maybe]]
    Some: ClassVar[Type[Maybe]]
    unit: ClassVar[Type[Maybe]]

    @staticmethod
    def of(optional: Optional[α]) -> Maybe[α]:
        """
        Maybe type constructor from Optional value.

        >>> Maybe.of(1)
        Some 1

        >>> Maybe.of(None)
        Nothing
        """
        return Maybe.Nothing() if optional is None else Maybe.Some(optional)

    @abstractmethod
    def __init__(self, value: Optional[α] = None) -> None:
        """
        Enforce using specific data type constructors.

        >>> Maybe()
        Traceback (most recent call last):
            ...
        TypeError: Can't instantiate abstract class Maybe with abstract methods ...

        >>> Maybe('value')
        Traceback (most recent call last):
            ...
        TypeError: Can't instantiate abstract class Maybe with abstract methods ...
        """
        raise AssertionError("Maybe is an abstract type; use a specific type constructor")

    def map(self, f: Callable[[α], β]) -> Maybe[β]:
        """
        Map Variable over Callable.

        >>> inc = lambda n: n + 1

        >>> Maybe.Some(1).map(inc)
        Some 2

        >>> Maybe.Nothing().map(inc)
        Nothing
        """
        return self.flatmap(lambda a: Maybe.Some(f(a)))

    @abstractmethod
    def flatmap(self, f: Callable[[α], Maybe[β]]) -> Maybe[β]:
        """
        Flatmap Variable over Callable returning Maybe.

        >>> Maybe.Some(1).flatmap(lambda _: Maybe.Some(2))
        Some 2

        >>> Maybe.Some(1).flatmap(lambda _: Maybe.Nothing())
        Nothing

        >>> Maybe.Nothing().flatmap(lambda _: Maybe.Some(1))
        Nothing

        >>> Maybe.Some(1).flatmap(const('invalid type'))
        Traceback (most recent call last):
            ...
        TypeError: f must return a Maybe type
        """
        raise NotImplementedError("Abstract function `flatmap` must be implemented by the type constructor")

    @abstractmethod
    def maybe(self, b: β, f: Callable[[α], β]) -> β:
        """
        Extract some value through `f` or get the default value `a`.

        >>> Maybe.Some(1).maybe(0, identity)
        1

        >>> Maybe.Nothing().maybe(0, identity)
        0
        """
        raise NotImplementedError("Abstract function `maybe` must be implemented by the type constructor")

    def isNothing(self) -> bool:
        """
        Return True iff self is Nothing.

        >>> Maybe.Some(1).isNothing()
        False

        >>> Maybe.Nothing().isNothing()
        True
        """
        return self.maybe(True, const(False))

    def isSome(self) -> bool:
        """
        Return True iff self is Some.

        >>> Maybe.Some(1).isSome()
        True

        >>> Maybe.Nothing().isSome()
        False
        """

        return self.maybe(False, const(True))

    def orElse(self, a: α) -> α:
        """
        Return a if self is Some.

        >>> Maybe.Some(1).orElse(2)
        1

        >>> Maybe.Nothing().orElse(1)
        1

        >>> Maybe.Nothing().orElse(None)
        """
        return self.maybe(a, identity)

    def or_else_throw(self, error):
        """
        Extract element of a Some and throws the error if Nothing.

        >>> Maybe.of(None).or_else_throw(ValueError("Expected some"))
        Traceback (most recent call last):
            ...
        ValueError: Expected some

        >>> Maybe.of(1).or_else_throw(ValueError("Expected some"))
        1
        """
        if self.isNothing():
            raise error
        return self.getSome()

    @abstractmethod
    def getSome(self) -> α:
        """
        Extract element of a Some and throws a ValueError if Nothing.

        >>> Maybe.Some(1).getSome()
        1

        >>> Maybe.Nothing().getSome()
        Traceback (most recent call last):
            ...
        ValueError: Cannot extract Some value from Nothing
        """
        raise NotImplementedError("Abstract function `getSome` must be implemented by the type constructor")

    def filter(self, p: Callable[[α], bool]) -> Maybe[β]:
        """
        Filter to a Maybe of the element that satisfies the predicate.

        >>> Maybe.Some(1).filter(lambda x: x == 1)
        Some 1

        >>> Maybe.Some(1).filter(lambda x: x > 1)
        Nothing
        """
        return self.flatmap(lambda x: Maybe.Some(x) if p(x) else Maybe.Nothing())

    @abstractmethod
    def __iter__(self):
        """
        Get an iterator over this Maybe.

        >>> [x for x in Maybe.Some(1)]
        [1]

        >>> [x for x in Maybe.Nothing()]
        []
        """
        raise NotImplementedError("Abstract function `__iter__` must be implemented by the type constructor")

    def __eq__(self, other: Any) -> bool:
        """
        Test two instances for value equality.

        >>> Maybe.Some(1) == Maybe.Some(1)
        True

        >>> Maybe.Some(1) == Maybe.Some(2)
        False

        >>> Maybe.Some(1) == Maybe.Nothing()
        False

        >>> Maybe.Nothing() == Maybe.Nothing()
        True
        """
        if isinstance(other, Maybe):
            return self.maybe(other.isNothing(), lambda x: other.maybe(False, x.__eq__))
        else:
            return False

    def __repr__(self) -> str:
        """
        Show the instance.

        >>> repr(Maybe.Some('value'))
        "Some 'value'"

        >>> repr(Maybe.Nothing())
        'Nothing'
        """
        return self.maybe("Nothing", lambda a: "Some {!r}".format(a))

    @staticmethod
    def sequence(xs: Iterable[Maybe[α]]) -> Maybe[Iterable[α]]:
        """
        Fold an iterable of Maybe to a Maybe of iterable.

        The iterable's class must have constructor that returns an empty instance
        given no arguments, and a non-empty instance given a singleton tuple.

        >>> Maybe.sequence([Maybe.Some(1), Maybe.Some(2)])
        Some [1, 2]

        >>> Maybe.sequence((Maybe.Some(2), Maybe.Some(3)))
        Some (2, 3)

        >>> Maybe.sequence((Maybe.Some(3), Maybe.Nothing()))
        Nothing
        """
        unit = xs.__class__
        empty = unit()  # type: ignore

        def iter(acc, e):
            return acc.flatmap(lambda rs: e.map(lambda x: rs + unit((x,))))

        return reduce(iter, xs, Maybe.Some(empty))


class __Nothing(Maybe):
    def __init__(self) -> None:
        """
        Nothing data constructor.

        >>> Maybe.Nothing()
        Nothing
        """
        pass

    def flatmap(self, f):
        return self

    def maybe(self, b, f):
        return b

    def getSome(self) -> α:
        raise ValueError("Cannot extract Some value from Nothing")

    def __iter__(self):
        return ().__iter__()


class __Some(Maybe):
    def __init__(self, a: α) -> None:
        """
        Initialise Some object.

        >>> Maybe.Some('value')
        Some 'value'

        >>> Maybe.Some(False)
        Some False

        >>> Maybe.Some(None)
        Traceback (most recent call last):
            ...
        AssertionError: Some must contain a value
        """
        assert a is not None, "Some must contain a value"
        self.value = a

    def flatmap(self, f):
        x = f(self.value)
        if not isinstance(x, Maybe):
            raise TypeError("f must return a Maybe type")
        return x

    def maybe(self, b, f):
        return f(self.value)

    def getSome(self) -> α:
        return self.value

    def __iter__(self):
        return (self.value,).__iter__()


Maybe.Nothing = const(__Nothing())  # type: ignore
Maybe.Some = __Some
Maybe.unit = __Some
