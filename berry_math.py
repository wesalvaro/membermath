from .berry import v, Berry
from .binerry import Binerry
from .unerry import Unerry
from math import floor


def __add__(self, other):
    return Binerry(self, v(other), "+", lambda a, b: a + b)


def __sub__(self, other):
    return Binerry(self, v(other), "-", lambda a, b: a - b)


def __mul__(self, other):
    return Binerry(self, v(other), "×", lambda a, b: a * b, scaling=True)


def __truediv__(self, other):
    return Binerry(self, v(other), "/", lambda a, b: a / b, scaling=True)


def __floordiv__(self, other):
    return Binerry(self, v(other), "⫽", lambda a, b: a // b, scaling=True)


def __pow__(self, exp):
    return Binerry(self, v(exp), "**", lambda a, b: a**b, scaling=True)


def __floor__(self):
    return Unerry("floor", lambda x: floor(x.value), self, variety=self.variety)


def __round__(self, places=0):
    def r(a):
        if places < 0:
            mul = 10 ** abs(places)
            return (floor(self / mul) * mul).value
        else:
            return round(self.value, places)

    return Unerry(f"round⌊{places}⌋", r, self, variety=self.variety)


def install():
    Berry.__add__ = __add__
    Berry.__sub__ = __sub__
    Berry.__mul__ = __mul__
    Berry.__pow__ = __pow__
    Berry.__truediv__ = __truediv__
    Berry.__floordiv__ = __floordiv__
    Berry.__floor__ = __floor__
    Berry.__round__ = __round__
