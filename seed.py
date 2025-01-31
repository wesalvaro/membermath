from .berry import Berry
from decimal import Decimal
from numbers import Number


class Seed(Berry):
    """A static value."""

    def __init__(self, value, variety=None, name=""):
        self._name = name
        self.variety = variety
        self.description = ""
        if isinstance(value, (str, Number)):
            value = Decimal(value)
        assert isinstance(
            value, Decimal
        ), f"{value} ({type(value)}) is not a value for {name}"
        self._value = value

    @property
    def formula(self) -> str:
        return f"{self.name}={self}" if self.name else f"{self}"

    @property
    def formula_simple(self) -> str:
        return f"{self.name}" if self.name else f"{self}"

    @property
    def formulas(self) -> dict:
        if not self.name:
            return {}
        return {self.name: f"{self}"}

    @property
    def name(self):
        return self._name

    @property
    def value(self) -> Decimal:
        return self._value

    def __call__(self, value=None) -> Berry:
        return self
