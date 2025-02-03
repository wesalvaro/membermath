from .berry import Berry
from .bushel import Bushel


class Unerry(Berry):
    """A value of some unary operation on a value."""
    __slots__ = "_value", "_fn"

    def __init__(self, name, fn, value: Berry, variety=None):
        self.name = name
        self._fn = fn
        self._value = value
        self.variety = variety
        self.description = ""

    @property
    def formula(self) -> str:
        return f"{self.name}({self._value.formula})={self}"

    @property
    def formula_simple(self) -> str:
        return f"{self.name}({self._value.formula_simple})={self}"

    @property
    def formulas(self) -> str:
        return {self.formula_simple: {**self._value.formulas}}

    @property
    def value(self):
        return self._fn(self._value)
