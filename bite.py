from .seed import Seed
from decimal import Decimal


def pct(value):
    """Creates a percentage berry."""
    return Bite(value)


class Bite(Seed):
    """A % value where values 0 to 100 (NOT fractions of 1)."""

    def __init__(self, value, name=""):
        super().__init__(Decimal(value) / 100, name=name)

    def __format__(self, spec):
        return f"{self.value * 100}%"
