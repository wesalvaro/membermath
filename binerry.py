from .berry import Berry, checkVariety
from .bushel import Bushel
from decimal import Decimal


class Binerry(Berry):
    """A value comprised of two other values joined by some operation."""

    __slots__ = (
        "a",
        "b",
        "op",
        "fn",
        "scaling",
    )

    def __init__(self, a, b, op, fn, scaling=False, name=""):
        self.name = name
        self.description = ""
        assert isinstance(a, Berry), f"{name} operand A {a} was not a value"
        assert isinstance(b, Berry), f"{name} operand B {b} was not a value"
        checkVariety(a.variety, b.variety, scaling)
        self.variety = a.variety or b.variety
        self.a = a
        self.b = b
        self.op = op
        self.fn = fn
        self.scaling = scaling

    @property
    def formula(self) -> str:
        v = f"({self.a.formula}{self.op}{self.b.formula})"
        return f"{self.name}={v}" if self.name else v

    @property
    def formula_simple(self) -> str:
        v = f"({self.a.formula_simple}{self.op}{self.b.formula_simple})={self}"
        return f"{self.name}={v}" if self.name else v

    @property
    def formulas(self) -> str:
        if self.name:
            d = {
                self.name: f"{self.a.name} {self.op} {self.b.name}",
            }
        else:
            d = {}
        d.update(self.a.formulas)
        d.update(self.b.formulas)
        return d

    @property
    def value(self) -> Decimal:
        return self.fn(self.a.value, self.b.value)
