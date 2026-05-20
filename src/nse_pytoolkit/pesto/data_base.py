from typing import TYPE_CHECKING, Any

from .inputs import Input

if TYPE_CHECKING:
    from collections.abc import Hashable

    from . import Trackable
    from .trackers import Tracker


class Database:
    """Reactive state container that drives incremental computation.

    Holds raw `Input` values and a cache of computed `Tracker` results.
    Mutations to inputs propagate invalidations through the dependency graph so
    that the next `compute` call for a stale tracker re-runs only what changed.
    """

    watchers: dict[Trackable, set[Tracker[Any]]]
    inputs: dict[Input[Any], Any]
    cache: dict[Hashable, Any]
    _dirty: set[Hashable]

    __slots__ = ("_dirty", "cache", "inputs", "watchers")

    def __init__(self) -> None:
        self.watchers = {}
        self.inputs = {}
        self.cache = {}
        self._dirty = set()

    def get_input[T](self, i: Input[T]) -> T:
        return self.inputs[i]

    def set_input[T](self, i: Input[T], value: T) -> None:
        """Set an input value and invalidate all trackers that watch it."""
        self.inputs[i] = value
        for dependent in list(self.watchers.get(i, set())):
            self.invalidate(dependent)

    def register(self, tracker: Tracker[Any]) -> None:
        """Subscribe `tracker` as a watcher of each of its declared dependencies."""
        for dep in tracker.dependencies:
            self.watchers.setdefault(dep, set()).add(tracker)

    def recompute(self, tracker: Tracker[Any]) -> None:
        """Unconditionally run `tracker` and update the cache if the value changed."""
        key = tracker.cache_key
        is_new = key not in self.cache
        new_value = tracker.function(self)

        if is_new or tracker.changed(
            self.cache[key],
            new_value,
        ):
            self.cache[key] = new_value
        self._dirty.discard(key)

    def compute[T](self, tracker: Tracker[T]) -> T:
        """Return the current value of `tracker`, recomputing it if stale or unseen."""
        key = tracker.cache_key
        is_new = key not in self.cache
        is_stale = key in self._dirty

        if is_new:
            self.register(tracker)

        if is_new or is_stale:
            self.recompute(tracker)

        return self.cache[key]

    def pin[T](self, tracker: Tracker[T], value: T) -> None:
        """Force `tracker`'s cached value to `value` without running its function.

        Invalidates downstream trackers as if the value had changed normally.
        """
        key = tracker.cache_key
        self.cache[key] = value
        self._dirty.discard(key)
        for dependent in list(self.watchers.get(tracker, set())):
            self.invalidate(dependent)

    def invalidate(self, tracker: Tracker[Any]) -> None:
        """Mark `tracker` as dirty and recursively invalidate its downstream watchers."""
        key = tracker.cache_key
        if key in self._dirty:
            return
        self._dirty.add(key)
        for dependent in list(self.watchers.get(tracker, set())):
            self.invalidate(dependent)

    def get[T](self, key: Trackable[T]) -> T:
        if isinstance(key, Input):
            return self.get_input(key)
        return self.compute(key)
