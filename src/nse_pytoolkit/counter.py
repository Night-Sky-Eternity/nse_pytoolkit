import threading
from collections.abc import Iterator, Sized
from typing import Self

__all__ = ("ContextCounter",)


class ContextCounter(Iterator[int], Sized):
    """Return an independent thread-safe counter. Call next() on it to get sequential IDs."""

    __slots__ = ("_count", "_lock")

    def __init__(self) -> None:
        self._count = 0
        self._lock = threading.Lock()

    def __iter__(self) -> Self:
        return self

    def __len__(self) -> int:
        with self._lock:
            return self._count

    def __next__(self) -> int:
        with self._lock:
            self._count += 1
            return self._count
