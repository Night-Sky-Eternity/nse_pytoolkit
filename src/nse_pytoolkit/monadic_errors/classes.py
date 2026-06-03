# nse_pytoolkit/monadic_errors/classes.py
from collections.abc import Callable
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    Generic,
    Never,
    Self,
    TypeVar,
)

if TYPE_CHECKING:
    from collections.abc import Callable

O_co = TypeVar("O_co", covariant=True)
E_co = TypeVar("E_co", bound=BaseException, covariant=True)

class Ok(Generic[O_co]):  # noqa: UP046
    value: O_co

    __slots__ = ("value",)

    def __init__(self, value: O_co) -> None:
        self.value = value

    def flatten[R: Result[Any, Any]](self: Ok[R]) -> R:
        return self.value

    def then[R: Result[Any, Any]](self, other: R) -> R:
        return other

    def otherwise(self, other: Result[Any, Any]) -> Self:  # noqa: ARG002
        return self

    def ok(self) -> Self:
        return self

    def err(self) -> None:
        return None

    def bind[R: Result[Any, Any], **P](
        self,
        f: Callable[Concatenate[O_co, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        return f(self.value, *args, **kwargs)

    def bind_err[R: Result[Any, Any], **P](
        self,
        f: Callable[Concatenate[Never, P], R],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Self:
        return self

    def map[U, **P](
        self,
        f: Callable[Concatenate[O_co, P], U],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Ok[U]:
        return Ok(f(self.value, *args, **kwargs))

    def map_or[U, **P](
        self,
        default: Never,  # noqa: ARG002
        f: Callable[Concatenate[O_co, P], U],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> U:
        return f(self.value, *args, **kwargs)

    def map_or_else[U, **P](
        self,
        default_f: Callable[[Never], U],  # noqa: ARG002
        f: Callable[Concatenate[O_co, P], U],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> U:
        return f(self.value, *args, **kwargs)

    def map_err[F: BaseException, **P](
        self,
        f: Callable[Concatenate[Never, P], F],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Self:
        return self

    def map_err_or[F, **P](
        self,
        default: F,
        f: Callable[Concatenate[Never, P], F],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> F:
        return default

    def map_err_or_else[F, **P](
        self,
        default_f: Callable[[O_co], F],
        f: Callable[Concatenate[Never, P], F],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> F:
        return default_f(self.value)

    def unwrap(self, *, msg: str | None = None) -> O_co:  # noqa: ARG002
        return self.value

    def unwrap_err(self, *, msg: str | None = None) -> Never:
        raise UnwrapError(msg or "called unwrap_err() on Ok") from None

    def unwrap_or(self, default: object) -> O_co:  # noqa: ARG002
        return self.value

    def unwrap_err_or[D](self, default: D) -> D:
        return default

    def unwrap_or_else[D, **P](
        self,
        default_factory: Callable[Concatenate[Never, P], Any],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> O_co:
        return self.value

    def unwrap_err_or_else[D, **P](
        self,
        default_factory: Callable[Concatenate[O_co, P], D],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> D:
        return default_factory(self.value, *args, **kwargs)

    def inspect[**P](
        self,
        f: Callable[Concatenate[O_co, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Self:
        f(self.value, *args, **kwargs)
        return self

    def inspect_err[**P](
        self,
        f: Callable[Concatenate[Never, P], Any],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Self:
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ok):
            ok: Ok[Any] = other
            return self.value == ok.value
        return NotImplemented

    def __hash__(self) -> int:
        return hash((type(Ok), self.value))

class Err(Generic[E_co]):  # noqa: UP046
    error: E_co

    __slots__ = ("error",)

    def __init__(self, error: E_co) -> None:
        self.error = error

    def flatten(self) -> Self:
        return self

    def then(self, other: Result[Any, Any]) -> Self:  # noqa: ARG002
        return self

    def otherwise[R: Result[Any, Any]](self, other: R) -> R:
        return other

    def ok(self) -> None:
        return None

    def err(self) -> Self:
        return self

    def bind[R: Result[Any, Any], **P](
        self,
        f: Callable[Concatenate[Never, P], R],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Self:
        return self

    def bind_err[R: Result[Any, Any], **P](
        self,
        f: Callable[Concatenate[E_co, P], R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        return f(self.error, *args, **kwargs)

    def map[U, **P](
        self,
        f: Callable[Concatenate[Never, P], U],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Self:
        return self

    def map_or[U, **P](
        self,
        default: U,
        f: Callable[Concatenate[Never, P], U],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> U:
        return default

    def map_or_else[U, **P](
        self,
        default_f: Callable[[E_co], U],
        f: Callable[Concatenate[Never, P], U],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> U:
        return default_f(self.error)

    def map_err[F: BaseException, **P](
        self,
        f: Callable[Concatenate[E_co, P], F],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Err[F]:
        return Err(f(self.error, *args, **kwargs))

    def map_err_or[F, **P](
        self,
        default: Never,  # noqa: ARG002
        f: Callable[Concatenate[E_co, P], F],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> F:
        return f(self.error, *args, **kwargs)

    def map_err_or_else[F, **P](
        self,
        default_f: Callable[[Never], F],  # noqa: ARG002
        f: Callable[Concatenate[E_co, P], F],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> F:
        return f(self.error, *args, **kwargs)

    def unwrap(self, *, msg: str | None = None) -> Never:
        raise UnwrapError(msg or "called unwrap() on Err") from self.error

    def unwrap_err(self, *, msg: str | None = None) -> E_co:  # noqa: ARG002
        return self.error

    def unwrap_or[D](self, default: D) -> D:
        return default

    def unwrap_err_or(self, default: object) -> E_co:  # noqa: ARG002
        return self.error

    def unwrap_or_else[D, **P](
        self,
        default_factory: Callable[Concatenate[E_co, P], D],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> D:
        return default_factory(self.error, *args, **kwargs)

    def unwrap_err_or_else[D, **P](
        self,
        default_factory: Callable[Concatenate[Never, P], Any],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> E_co:
        return self.error

    def inspect[**P](
        self,
        f: Callable[Concatenate[Never, P], Any],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Self:
        return self

    def inspect_err[**P](
        self,
        f: Callable[Concatenate[E_co, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Self:
        f(self.error, *args, **kwargs)
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Err):
            err: Err[Any] = other
            return self.error == err.error
        return NotImplemented

    def __hash__(self) -> int:
        return hash((type(Err), self.error))

type Result[O, E: BaseException] = Ok[O] | Err[E]

class UnwrapError(Exception):
    pass
