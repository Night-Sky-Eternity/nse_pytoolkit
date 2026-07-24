# nse_pytoolkit/monadic_errors/decorator.py
import functools
from typing import TYPE_CHECKING, overload

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

    @overload
    def __call__[**P, O, F: BaseException](
        self,
        f: Callable[P, Result[O, F]],
    ) -> Callable[P, Result[O, E | F]]: ...

    @overload
    def __call__[**P, O](
        self,
        f: Callable[P, O],
    ) -> Callable[P, Result[O, E]]: ...

    def __call__[**P, O, F: BaseException](
        self,
        f: Callable[P, O | Result[O, F]],
    ) -> Callable[P, Result[O, E | F]]:
        error_tuple = tuple(self.exceptions)

        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[O, E | F]:
            try:
                result = f(*args, **kwargs)
            except error_tuple as e:
                return Err(e)
            return result if isinstance(result, (Ok, Err)) else Ok(result)

        return wrapper
