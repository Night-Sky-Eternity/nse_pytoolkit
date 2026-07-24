# nse_pytoolkit/monadic_errors

from .classes import Err, Ok, Result
from .decorator import catches
from .functions import collect, is_error, is_okay

__all__ = ("Err", "Ok", "Result", "catches", "collect", "is_error", "is_okay")
