from .berry import Berry, Variety
from .bushel import Bushel
import inspect


class Callerry(Berry):
    """A value from invoking a method with other values.

    Arguments to the method must exist in the provided bushel.
    Parameter and return annotations, if provided, must be Varieties.
    """

    __slots__ = "_sig", "_fn", "_bushel", "name", "description"

    def __init__(self, fn, bushel, name, prefix=""):
        self._sig = inspect.signature(fn)
        self._fn = fn
        self._bushel = bushel
        name = name if fn.__name__ == "<lambda>" else fn.__name__
        self.name = prefix + name
        self.description = fn.__doc__
        assert self.args

    @property
    def args(self):
        aa = []
        for v in self._sig.parameters.values():
            if v.name in self._bushel:
                b = self._bushel[v.name]
                _checkVarietyAnnotations(v.annotation, b.variety)
                aa.append(b)
                continue
            elif v.default != inspect.Parameter.empty:
                b = Berry.of(v.default, variety=_checkVarietyAnnotations(v.annotation))
                aa.append(b)
                continue
            else:
                raise KeyError(f"Missing {v.name}.")
        return aa

    @property
    def formula(self) -> str:
        return f"{self.name}({[a.formula for a in self.args]})={self}"

    @property
    def formula_simple(self) -> str:
        return f"{self.name}({[a.formula_simple for a in self.args]})={self}"

    @property
    def formulas(self) -> str:
        d = {self.name: str(self._sig)}
        for a in self.args:
            d.update(a.formulas)
        return d

    @property
    def value(self):
        v = Berry.of(self._fn(*self.args))
        retanno = self._sig.return_annotation
        if retanno != inspect.Signature.empty:
            assert (
                retanno == v.variety
            ), f"`{self.name}` declared and actual varieties don't match: {retanno} & {v.variety}"
        return v

    @property
    def variety(self):
        return _checkVarietyAnnotations(self._sig.return_annotation, self.value.variety)


def _checkVarietyAnnotations(a, b=None):
    if a == inspect.Signature.empty:
        return b
    elif inspect.isclass(a):
        assert issubclass(a, Variety), f"Annotation {a} was not a Variety."
    else:
        assert isinstance(a, Variety), f"Annotation {a} was not a Variety."
    assert a == b, f"declared and actual varieties don't match: {a} & {b}"
    return a
