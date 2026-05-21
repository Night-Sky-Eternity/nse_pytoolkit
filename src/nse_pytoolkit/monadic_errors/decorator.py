# nse_pytoolkit/monadic_errors/decorator.py
import functools
from typing import TYPE_CHECKING

from .classes import Err, Ok, Result

if TYPE_CHECKING:
    from collections.abc import Callable


class Catches[E: BaseException]:
    exceptions: set[type[E]]

    __slots__ = ("exceptions",)

    def __init__(self, *exc: type[E]) -> None:
        self.exceptions = set(exc)

    def run[**P, O](
        self,
        f: Callable[P, O],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[O, E]:
        error_tuple = tuple(self.exceptions)
        try:
            return Ok(f(*args, **kwargs))
        except error_tuple as e:
            return Err(e)

    def __call__[**P, O](self, f: Callable[P, O]) -> Callable[P, Result[O, E]]:
        error_tuple = tuple(self.exceptions)

        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[O, E]:
            try:
                return Ok(f(*args, **kwargs))
            except error_tuple as e:
                return Err(e)

        return wrapper

    def __or__[F: BaseException](self, other: Catches[F] | type[F]) -> Catches[E | F]:
        if isinstance(other, Catches):
            return Catches(*self.exceptions.union(other.exceptions))
        if issubclass(other, BaseException):  # pyright: ignore[reportUnnecessaryIsInstance]
            return Catches(*self.exceptions, other)
        return NotImplemented

    __ror__ = __or__
    __ior__ = __or__

    @staticmethod
    def add[F: BaseException](*exc: type[F]) -> AddedCatches[F]:
        return AddedCatches(*exc)


def catches[E: BaseException](*exc: type[E]) -> Catches[E]:
    return Catches(*exc)


class AddedCatches[E: BaseException]:
    exceptions: set[type[E]]

    __slots__ = ("exceptions",)

    def __init__(self, *exc: type[E]) -> None:
        self.exceptions = set(exc)

    def run[**P, O, F: BaseException](
        self,
        f: Callable[P, Result[O, F]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[O, E | F]:
        error_tuple = tuple(self.exceptions)
        try:
            return f(*args, **kwargs)
        except error_tuple as e:
            return Err(e)

    def __call__[**P, O, F: BaseException](
        self,
        f: Callable[P, Result[O, F]],
    ) -> Callable[P, Result[O, E | F]]:
        error_tuple = tuple(self.exceptions)

        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[O, E | F]:
            try:
                return f(*args, **kwargs)
            except error_tuple as e:
                return Err(e)

        return wrapper

    def __or__[F: BaseException](
        self,
        other: Catches[F] | type[F],
    ) -> AddedCatches[E | F]:
        if isinstance(other, Catches):
            return AddedCatches(*self.exceptions.union(other.exceptions))
        if issubclass(other, BaseException):  # pyright: ignore[reportUnnecessaryIsInstance]
            return AddedCatches(*self.exceptions, other)
        return NotImplemented

    __ror__ = __or__
    __ior__ = __or__


def add_catches[E: BaseException](*exc: type[E]) -> AddedCatches[E]:
    return AddedCatches(*exc)
