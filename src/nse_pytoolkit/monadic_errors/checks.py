# nse_pytoolkit/monadic_errors/checks.py
from typing import TYPE_CHECKING, Any, TypeIs, overload

from .classes import Err, Ok, Result

if TYPE_CHECKING:
    from ..aliases import NotEmptyTuple  # noqa: TID252


@overload
def is_error[O, E: BaseException](
    res: Result[O, Any],
    /,
    *exc: *NotEmptyTuple[type[E]],
) -> TypeIs[Err[E]]: ...


@overload
def is_error[O, E: BaseException](
    res: Result[O, E],
    /,
) -> TypeIs[Err[E]]: ...


def is_error[O, E: BaseException](
    res: Result[O, E],
    /,
    *exc: type[E],
) -> TypeIs[Err[E]]:
    if not exc:
        return isinstance(res, Err)

    return isinstance(res, Err) and isinstance(res.error, exc)


@overload
def is_okay[O, E: BaseException](
    res: Result[Any, E],
    /,
    *val: *NotEmptyTuple[type[O]],
) -> TypeIs[Ok[O]]: ...


@overload
def is_okay[O, E: BaseException](
    res: Result[O, E],
    /,
) -> TypeIs[Ok[O]]: ...


def is_okay[O, E: BaseException](
    res: Result[O, E],
    /,
    *val: type[O],
) -> TypeIs[Ok[O]]:
    if not val:
        return isinstance(res, Ok)

    return isinstance(res, Ok) and isinstance(res.value, val)
