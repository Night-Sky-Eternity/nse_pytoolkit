# nse_pytoolkit/monadic_errors/decorator.py
import functools
from typing import TYPE_CHECKING

from .classes import Err, Ok, Result

if TYPE_CHECKING:
    from collections.abc import Callable


class catches[E: BaseException]:  # noqa: N801
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

    def __or__[F: BaseException](self, other: catches[F] | type[F]) -> catches[E | F]:
        if isinstance(other, catches):
            return catches(*self.exceptions.union(other.exceptions))
        if issubclass(other, BaseException):  # pyright: ignore[reportUnnecessaryIsInstance]
            return catches(*self.exceptions, other)
        return NotImplemented

    __ror__ = __or__
    __ior__ = __or__

    @staticmethod
    def add[F: BaseException](*exc: type[F]) -> AddedCatches[F]:
        return AddedCatches(*exc)


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
        other: catches[F] | type[F],
    ) -> AddedCatches[E | F]:
        if isinstance(other, catches):
            return AddedCatches(*self.exceptions.union(other.exceptions))
        if issubclass(other, BaseException):  # pyright: ignore[reportUnnecessaryIsInstance]
            return AddedCatches(*self.exceptions, other)
        return NotImplemented

    __ror__ = __or__
    __ior__ = __or__
