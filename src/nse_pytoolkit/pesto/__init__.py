from typing import Any

from .data_base import Database
from .inputs import Input
from .trackers import Tracker, TrackerTemplate, tracks

type Trackable[T = Any] = Tracker[T] | Input[T]

__all__ = ("Database", "Input", "Trackable", "Tracker", "TrackerTemplate", "tracks")
