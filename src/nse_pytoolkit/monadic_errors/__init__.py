# nse_pytoolkit/monadic_errors
from .checks import is_error, is_okay
from .classes import Err, Ok, Result
from .decorator import AddedCatches, catches

__all__ = ("AddedCatches", "Err", "Ok", "Result", "catches", "catches", "is_error", "is_okay")
