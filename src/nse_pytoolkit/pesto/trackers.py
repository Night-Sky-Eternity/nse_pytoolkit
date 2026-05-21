# nse_pytoolkit/pesto/trackers.py
import functools
import inspect
from typing import TYPE_CHECKING, Any, Concatenate, Final

if TYPE_CHECKING:
    from collections.abc import Callable, Hashable, Iterable

    from ..aliases import NotEmptyTuple  # noqa: TID252
    from . import Trackable
    from .data_base import Database


class Tracker[T]:
    """A derived value cached per `cache_key` and recomputed when its dependencies change.

    `dependencies` is fixed at construction — the dependency set is static and never
    re-derived at call time. Override `changed` to control when a freshly computed
    value counts as a real change and propagates further invalidations.
    """

    dependencies: Final[set[Trackable]]
    function: Final[Callable[[Database], T]]
    cache_key: Final[Hashable]

    __slots__ = ("cache_key", "dependencies", "function")

    def __init__(
        self,
        function: Callable[[Database], T],
        dependencies: Iterable[Trackable],
        cache_key: Hashable | None = None,
    ) -> None:
        self.function = function
        self.dependencies = set(dependencies)
        self.cache_key = cache_key or self

    def get(self, db: Database) -> T:
        return db.compute(self)

    def __call__(self, db: Database) -> T:
        return self.get(db)

    def __getitem__(self, key: Database) -> T:
        return self.get(key)

    @classmethod
    def changed(cls, old: T, new: T) -> bool:
        """Return whether recomputing produced a meaningful change.

        Override in a subclass to suppress downstream invalidation for values
        that are semantically equivalent but not equal (e.g. same-length lists).
        """
        return old != new


class tracks:  # noqa: N801
    """Decorator that binds a set of dependencies to a tracker function.

    Two usage forms:

    - ``tracks(dep_a, dep_b).make(fn)`` — zero-argument tracker; wraps ``fn``
      directly into a ``Tracker``.
    - ``@tracks(dep_a, dep_b)`` on a function with extra parameters — returns a
      ``TrackerTemplate`` whose instances each occupy a separate cache slot.
    """

    def __init__(
        self,
        *dependencies: *NotEmptyTuple[Trackable],
        tracker: type[Tracker[Any]] = Tracker,
    ) -> None:
        self.dependencies = dependencies
        self.tracker = tracker

    def make[R](self, fn: Callable[[Database], R]) -> Tracker[R]:
        """Wrap `fn` directly into a `Tracker` with no additional arguments."""
        return self.tracker(fn, self.dependencies)

    def __call__[**P, R](
        self,
        fn: Callable[Concatenate[Database, P], R],
    ) -> TrackerTemplate[P, R]:
        return TrackerTemplate(self.dependencies, fn, tracker=self.tracker)


class TrackerTemplate[**P, R]:
    """Produces `Tracker` instances bound to specific call arguments.

    Each unique argument combination gets its own cache slot in the database,
    identified by a key derived from the bound signature (defaults included).
    """

    def __init__(
        self,
        dependencies: Iterable[Trackable],
        fn: Callable[Concatenate[Database, P], R],
        *,
        tracker: type[Tracker[Any]] = Tracker,
    ) -> None:
        self.dependencies = dependencies
        self.fn = fn
        self.tracker = tracker

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Tracker[R]:
        @functools.wraps(self.fn)
        def inner(db: Database) -> R:
            return self.fn(db, *args, **kwargs)

        return self.tracker(inner, self.dependencies, self.cache_key(*args, **kwargs))

    def cache_key(self, *args: P.args, **kwargs: P.kwargs) -> Hashable:
        """Compute the cache key for a given set of arguments.

        Applies defaults so that ``f(x=1)`` and ``f(1)`` map to the same slot.
        """
        bound = inspect.signature(self.fn).bind(None, *args, **kwargs)
        bound.apply_defaults()
        return self, *bound.args[1:], *bound.kwargs.items()
