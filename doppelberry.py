from .berry import Berry
from decimal import Decimal


class Doppelberry(Berry):
    __slots__ = ("_value",)

    def __init__(self, value: Berry, name: str):
        assert name, "Alias not needed without a name."
        assert name != value.name, "Alias not needed for the same name."
        self.name = name
        self.variety = value.variety
        self.description = ""
        assert isinstance(value, Berry), "{name}'s real {value} was not a value"
        self._value = value

    @property
    def value(self) -> Decimal:
        return self._value.value

    @property
    def formula(self) -> str:
        return f"{self.name}={self._value.formula}"

    @property
    def formula_simple(self) -> str:
        return f"{self.name}"

    @property
    def formulas(self) -> dict:
        d = {self.name: self._value.formula_simple}
        d.update(self._value.formulas)
        return d
