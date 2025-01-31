from .berry import Berry
from .doppelberry import Doppelberry
from datetime import date


class BestByBerry(Doppelberry):
    """A date-linked value."""

    __slots__ = ("date",)

    def __init__(self, value: Berry, day: date):
        super().__init__(value, f"{value.name}@{date}")
        self.date = day
