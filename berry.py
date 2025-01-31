from decimal import Decimal
from datetime import date
from numbers import Number
from math import floor


class Berry(object):
    """Must implement: name, value, variety, formula, description."""

    __slots__ = (
        "name",
        "variety",
        "description",
        # Maybe value is an @property?
    )

    def __init__(self):
        raise NotImplementedError("Use Vc, V2 or Vf.")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.formula})"

    def __str__(self):
        return self.formula

    def __add__(self, other):
        from .binerry import Binerry

        return Binerry(self, v(other), "+", lambda a, b: a + b)

    def __sub__(self, other):
        from .binerry import Binerry

        return Binerry(self, v(other), "-", lambda a, b: a - b)

    def __mul__(self, other):
        from .binerry import Binerry

        return Binerry(self, v(other), "×", lambda a, b: a * b, scaling=True)

    def __truediv__(self, other):
        from .binerry import Binerry

        return Binerry(self, v(other), "/", lambda a, b: a / b, scaling=True)

    def __floordiv__(self, other):
        from .binerry import Binerry

        return Binerry(self, v(other), "⫽", lambda a, b: a // b, scaling=True)

    def __floor__(self):
        from .unerry import Unerry

        return Unerry("floor", lambda x: floor(x.value), self, variety=self.variety)

    def __round__(self, places=0):
        from .unerry import Unerry

        def r(a):
            if places < 0:
                mul = 10 ** abs(places)
                return (floor(self / mul) * mul).value
            else:
                return round(self.value, places)

        return Unerry(f"round⌊{places}⌋", r, self, variety=self.variety)

    def __eq__(self, other):
        return self.value == v(other).value

    def __ne__(self, other):
        return self.value != v(other).value

    def __lt__(self, other):
        return self.value < v(other).value

    def __le__(self, other):
        return self.value <= v(other).value

    def __gt__(self, other):
        return self.value > v(other).value

    def __ge__(self, other):
        return self.value >= v(other).value

    def __matmul__(self, other: date):
        from .bestbyberry import BestByBerry

        assert isinstance(other, date)
        return BestByBerry(self, other)

    def __rshift__(self, other: "Variety"):
        assert isinstance(other, Variety)
        try:
            return Variety.convert(self, other)
        except Exception as e:
            raise NotImplementedError(f"Can't convert {self} to {other}: {e}")

    def __format__(self, spec):
        variety = self.variety or Unknown
        return variety.format(self)

    @staticmethod
    def of(x, variety: "Variety" = None, name=""):
        from .doppelberry import Doppelberry
        from .seed import Seed

        if isinstance(x, Berry):
            if variety:
                checkVariety(variety, x.variety)
            if name == x.name:
                return x
            return Doppelberry(x, name=name) if name else x
        elif isinstance(x, tuple):
            b, variety = x
            if variety:
                checkVariety(variety, variety)
            return v(v, variety=variety)
        elif isinstance(x, (str, Decimal, Number)):
            return Seed(x, variety=variety, name=name)
        else:
            raise ValueError(f"Can't create V from {repr(x)}")


def v(value, variety=None, name=""):
    return Berry.of(value, variety=variety, name=name)


class Variety(object):
    def __init__(
        self,
        name: str,
        symbol: str = None,
        format=lambda u, v: f"{v.value} {u.name}",
        current_rates: dict = None,
        day_based_rates: dict = None,
    ):
        self.name = name
        self.symbol = symbol
        self._format = format
        self._current_rates = current_rates
        self._day_based_rates = day_based_rates

    def rate(self, value):
        return v(value, variety=self)

    def format(self, value):
        return self._format(self, value)

    def ex(self, original: Berry, day: date):
        if original.name is self.name:
            return self.rate(1)
        if (
            day
            and self._day_based_rates
            and original.name in self._day_based_rates
            and str(day) in self._day_based_rates[original.name]
        ):
            return self.rate(self._day_based_rates[original.name][str(day)])
        if not day and self._current_rates and original.name in self._current_rates:
            return self.rate(self._current_rates[original.name])
        raise NotImplementedError(f"No ex implemented ({original} » {self}" + (f"@{day}" if day else "") + ").")

    def __str__(self):
        return self.symbol or self.name

    @staticmethod
    def convert(src: Berry, dst: "Variety"):
        from .binerry import Binerry
        from .bestbyberry import BestByBerry

        if isinstance(src, BestByBerry):
            day = src.date
        else:
            day = None
        no_unit = v(src.value)
        op = f" {src.variety.name}<{src.variety}{dst}" + (f"@{day}" if day else "") + ">"
        try:
            return Binerry(
                no_unit, dst.ex(src.variety, day), op, lambda a, b: a * b, scaling=True
            )
        except NotImplementedError:
            return Binerry(
                no_unit,
                v(src.variety.ex(dst, day).value, variety=dst),
                op,
                lambda a, b: a / b,
                scaling=True,
            )


def checkVariety(a: Variety, b: Variety, scaling_op=False):
    if scaling_op:
        assert b == a or not b or not a, f"Different varieties: {a} != {b}"
    else:
        assert b == a, f"Different varieties: {b} != {a}"


Unknown = Variety("?", "?", lambda u, v: f"{round(v.value, 2):,}")
