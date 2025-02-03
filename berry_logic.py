from .berry import Berry, v


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


def install():
    Berry.__eq__ = __eq__
    Berry.__ne__ = __ne__
    Berry.__lt__ = __lt__
    Berry.__le__ = __le__
    Berry.__gt__ = __gt__
    Berry.__ge__ = __ge__
