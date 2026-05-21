# nse_pytoolkit/pesto/inputs.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .data_base import Database


class Input[T]:
    """A leaf node in the reactive graph whose value is set externally.

    Mutating an input via `Database.set_input` automatically invalidates all
    trackers that declared it as a dependency.
    """

    __slots__ = ()

    def get(self, db: Database) -> T:
        return db.get_input(self)

    def set(self, db: Database, value: T) -> None:
        db.set_input(self, value)

    def __call__(self, db: Database) -> T:
        return self.get(db)

    def __getitem__(self, key: Database) -> T:
        return self.get(key)

    def __setitem__(self, key: Database, value: T) -> None:
        self.set(key, value)
