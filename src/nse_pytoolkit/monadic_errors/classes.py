# nse_pytoolkit/monadic_errors/classes.py
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Concatenate, Never, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable


class Result[O, E: BaseException](Protocol):
    def bind[U, F: BaseException, **P](
        self,
        f: Callable[Concatenate[O, P], Result[U, F]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[U, E | F]: ...  # rust: and_then

    def bind_err[U, F: BaseException, **P](
        self,
        f: Callable[Concatenate[E, P], Result[U, F]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[U | O, F]: ...  # rust: or_else

    def map[U, **P](
        self,
        f: Callable[Concatenate[O, P], U],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[U, E]: ...

    def map_or[U, **P](
        self,
        default: U,
        f: Callable[Concatenate[O, P], U],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> U: ...

    def map_or_else[U, **P](
        self,
        default_f: Callable[[E], U],
        f: Callable[Concatenate[O, P], U],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> U: ...

    def map_err[F: BaseException, **P](
        self,
        f: Callable[Concatenate[E, P], F],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[O, F]: ...

    def map_err_or[F, **P](
        self,
        default: F,
        f: Callable[Concatenate[E, P], F],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> F: ...

    def map_err_or_else[F, **P](
        self,
        default_f: Callable[[O], F],
        f: Callable[Concatenate[E, P], F],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> F: ...

    def unwrap(self, *, msg: str | None = None) -> O: ...

    def unwrap_err(self, *, msg: str | None = None) -> E: ...

    def unwrap_or[D](self, default: D) -> O | D: ...

    def unwrap_err_or[D](self, default: D) -> D | E: ...

    def unwrap_or_else[D, **P](
        self,
        default_factory: Callable[Concatenate[E, P], D],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> O | D: ...

    def unwrap_err_or_else[D, **P](
        self,
        default_factory: Callable[Concatenate[O, P], D],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> D | E: ...

    def inspect[**P](
        self,
        f: Callable[Concatenate[O, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[O, E]: ...

    def inspect_err[**P](
        self,
        f: Callable[Concatenate[E, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[O, E]: ...

    def __eq__(self, value: object) -> bool: ...

    def __hash__(self) -> int: ...


class Ok[O](Result[O, Never]):
    value: O

    __slots__ = ("value",)

    def __init__(self, value: O) -> None:
        self.value = value

    def bind[U, F: BaseException, **P](
        self,
        f: Callable[Concatenate[O, P], Result[U, F]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[U, F]:
        return f(self.value, *args, **kwargs)

    def bind_err[U, F: BaseException, **P](
        self,
        f: Callable[Concatenate[Never, P], Result[U, F]],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Ok[O]:
        return self

    def map[U, **P](
        self,
        f: Callable[Concatenate[O, P], U],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Ok[U]:
        return Ok(f(self.value, *args, **kwargs))

    def map_or[U, **P](
        self,
        default: Never,  # noqa: ARG002
        f: Callable[Concatenate[O, P], U],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> U:
        return f(self.value, *args, **kwargs)

    def map_or_else[U, **P](
        self,
        default_f: Callable[[Never], U],  # noqa: ARG002
        f: Callable[Concatenate[O, P], U],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> U:
        return f(self.value, *args, **kwargs)

    def map_err[F: BaseException, **P](
        self,
        f: Callable[Concatenate[Never, P], F],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Ok[O]:
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
        default_f: Callable[[O], F],
        f: Callable[Concatenate[Never, P], F],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> F:
        return default_f(self.value)

    def unwrap(self, *, msg: str | None = None) -> O:  # noqa: ARG002
        return self.value

    def unwrap_err(self, *, msg: str | None = None) -> Never:
        raise UnwrapError(msg or "called unwrap_err() on Ok") from None

    def unwrap_or(self, default: object) -> O:  # noqa: ARG002
        return self.value

    def unwrap_err_or[D](self, default: D) -> D:
        return default

    def unwrap_or_else[D, **P](
        self,
        default_factory: Callable[Concatenate[Never, P], Any],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> O:
        return self.value

    def unwrap_err_or_else[D, **P](
        self,
        default_factory: Callable[Concatenate[O, P], D],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> D:
        return default_factory(self.value, *args, **kwargs)

    def inspect[**P](
        self,
        f: Callable[Concatenate[O, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Ok[O]:
        f(self.value, *args, **kwargs)
        return self

    def inspect_err[**P](
        self,
        f: Callable[Concatenate[Never, P], Any],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Ok[O]:
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ok):
            ok: Ok[Any] = other
            return self.value == ok.value
        return NotImplemented

    def __hash__(self) -> int:
        return hash((type(Ok), self.value))


class Err[E: BaseException](Result[Never, E]):
    error: E

    __slots__ = ("error",)

    def __init__(self, error: E) -> None:
        self.error = error

    def bind[U, F: BaseException, **P](
        self,
        f: Callable[Concatenate[Never, P], Result[U, F]],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Err[E]:
        return self

    def bind_err[U, F: BaseException, **P](
        self,
        f: Callable[Concatenate[E, P], Result[U, F]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[U, F]:
        return f(self.error, *args, **kwargs)

    def map[U, **P](
        self,
        f: Callable[Concatenate[Never, P], U],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Err[E]:
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
        default_f: Callable[[E], U],
        f: Callable[Concatenate[Never, P], U],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> U:
        return default_f(self.error)

    def map_err[F: BaseException, **P](
        self,
        f: Callable[Concatenate[E, P], F],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Err[F]:
        return Err(f(self.error, *args, **kwargs))

    def map_err_or[F, **P](
        self,
        default: Never,  # noqa: ARG002
        f: Callable[Concatenate[E, P], F],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> F:
        return f(self.error, *args, **kwargs)

    def map_err_or_else[F, **P](
        self,
        default_f: Callable[[Never], F],  # noqa: ARG002
        f: Callable[Concatenate[E, P], F],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> F:
        return f(self.error, *args, **kwargs)

    def unwrap(self, *, msg: str | None = None) -> Never:
        raise UnwrapError(msg or "called unwrap() on Err") from self.error

    def unwrap_err(self, *, msg: str | None = None) -> E:  # noqa: ARG002
        return self.error

    def unwrap_or[D](self, default: D) -> D:
        return default

    def unwrap_err_or(self, default: object) -> E:  # noqa: ARG002
        return self.error

    def unwrap_or_else[D, **P](
        self,
        default_factory: Callable[Concatenate[E, P], D],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> D:
        return default_factory(self.error, *args, **kwargs)

    def unwrap_err_or_else[D, **P](
        self,
        default_factory: Callable[Concatenate[Never, P], Any],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> E:
        return self.error

    def inspect[**P](
        self,
        f: Callable[Concatenate[Never, P], Any],  # noqa: ARG002
        *args: P.args,  # noqa: ARG002
        **kwargs: P.kwargs,  # noqa: ARG002
    ) -> Err[E]:
        return self

    def inspect_err[**P](
        self,
        f: Callable[Concatenate[E, P], Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Err[E]:
        f(self.error, *args, **kwargs)
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Err):
            err: Err[Any] = other
            return self.error == err.error
        return NotImplemented

    def __hash__(self) -> int:
        return hash((type(Err), self.error))


class UnwrapError(Exception):
    pass
