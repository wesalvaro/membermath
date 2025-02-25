from . import Bushel, Variety, pct
from datetime import date

Blueberry = Variety(
    "BLU", "🫐", current_rates={"SBY": 3}, day_based_rates={"SBY": {"2025-01-31": 2}}
)
Strawberry = Variety("SBY", "🍓")
_ = Bushel()
_.b = 12, Blueberry
_.s = _.b >> Strawberry

print(_.s.formula)
print(_.s.value)
print(_.s.variety)


class Sentinel:
    def __init__(self, name):
        self._name = name

    def __str__(self):
        return self._name


Cat = Sentinel("cat")

_ = Bushel()
_["a"] = 2
_[Cat] = _["a"] * 4

print(_[Cat])
print(_[Cat].value)

_.dog = _[Cat] - 6
print(_.dog)
print(_.dog.value)

これ = Bushel(prefix="あれ")
これ.ペン = 9
これ.です = 4
これ.は = これ.ペン + これ.です

print(これ.は)
print(これ.は.value)

USD = Variety("USD", "$")
JPY = Variety(
    "JPY",
    "¥",
    current_rates={"USD": 150},
    day_based_rates={"USD": {str(date.today()): 160}},
)

taxes = Bushel()
taxes.income = 100, USD
taxes.rate = pct(60)

print(taxes.income)
print(taxes.rate)

taxes.total = taxes.income * taxes.rate
taxes.total_jpy = taxes.total >> JPY

print(taxes.total_jpy)
print(taxes.total_jpy.variety, taxes.total_jpy.value)

fx = Bushel()
fx.usd = taxes.income
fx.jpy = 1_5000, JPY
try:
    fx.total = fx.usd + fx.jpy
except Exception as e:
    assert "Different varieties: $ != ¥" in str(e)
fx.total_jpy = (fx.usd >> JPY) + fx.jpy
fx.total_usd = fx.usd + (fx.jpy >> USD)
fx.total_usd_today = fx.usd + (fx.jpy @ date.today() >> USD)

print(fx.total_jpy)
print(fx.total_jpy.variety, fx.total_jpy.value)
print(fx.total_usd)
print(fx.total_usd.variety, fx.total_usd.value)
print(fx.total_usd_today)
print(fx.total_usd_today.variety, fx.total_usd_today.value)


def cube2(y=2):
    return y**3


def halve(x: Blueberry) -> Strawberry:
    return x / 2


fn = Bushel()
fn.x = 2, Blueberry
fn.foo = lambda x: x**2
assert fn.foo == 4
fn.bar = cube2
assert fn.bar == 8
assert fn.bar.variety == None
fn.y = 3, USD
assert fn.bar == 27
assert fn.bar.variety == USD
fn.baz = halve
try:
    assert fn.baz == 1
except AssertionError as e:
    assert "declared and actual varieties" in str(e)

from rich.console import Console

c = Console()
c.print(fn.x)
