# nse_pytoolkit/monadic_errors
from .checks import is_error, is_okay
from .classes import Err, Ok, Result
from .decorator import AddedCatches, catches, add_catches, catches

__all__ = ("AddedCatches", "catches", "Err", "Ok", "Result", "add_catches", "catches", "is_error", "is_okay")
