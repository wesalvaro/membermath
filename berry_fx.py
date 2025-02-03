from datetime import date
from .berry import Berry, Unknown, Variety
from .bestbyberry import BestByBerry


def __matmul__(self, other: date):
    assert isinstance(other, date)
    return BestByBerry(self, other)


def __rshift__(self, other: Variety):
    assert self.variety is not None
    assert isinstance(other, Variety)
    try:
        return Variety.convert(self, other)
    except Exception as e:
        raise NotImplementedError(f"Can't convert {self} to {other}: {e}")


def install():
    Berry.__matmul__ = __matmul__
    Berry.__rshift__ = __rshift__
