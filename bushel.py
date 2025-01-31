from .berry import Berry, Variety


class Bushel(object):
    """A collection of unique, final values.

    Works very similarly to a dict.

    f = Bushel({"a":3}, {"b":5}, x=1, y=2)
    f.z = f.x + f.y
    f.c = f.a * f.b
    f.result = f.z + f.c
    assert f.result == 18
    """

    __slots__ = (
        "_values",
        "_prefix",
    )

    def __init__(self, *args, prefix: str = None, **kwargs):
        self._values = dict()
        self._prefix = f"{prefix}_" if prefix else ""
        for a in args:
            self.update(a)
        self.update(kwargs)

    def update(self, other):
        if isinstance(other, dict):
            d = other
        elif isinstance(other, Bushel):
            d = other._values
        else:
            raise ValueError(f"Unrecognized collection. {type(other)}")
        overlapping = self._values.keys() & d.keys()
        assert not overlapping, f"Overlapping keys: {overlapping}"
        for k, v in d.items():
            self.__setattr__(k, v)

    def __iter__(self):
        return self._values.__iter__()

    def __len__(self):
        return len(self._values)

    def __delitem__(self, key):
        raise NotImplementedError("Values cannot be changed.")

    def __getitem__(self, key):
        if key not in self._values:
            raise KeyError(f"{key} is not set: {" ".join(sorted(self._values.keys()))}")
        return self._values[key]

    def __setitem__(self, name, value):
        if name in {"_values", "_prefix"}:
            super().__setattr__(name, value)
            return
        if name in self._values:
            raise KeyError(
                f"{name} already set: {self._values[name]}\nCannot set to {value}"
            )
        nice_name = self._prefix + str(name)
        if isinstance(value, tuple):
            self._values[name] = _tupleBerry(value, name=nice_name)
        else:
            self._values[name] = Berry.of(value, name=nice_name)

    def __getattr__(self, name) -> Berry:
        if name == "keys":
            return self._values.keys
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __str__(self):
        s = []
        for k, v in self._values.items():
            if v.name == k:
                s.append(v.formula)
            else:
                s.append(f"{k}: {v.formula}")
            if v.description:
                s.append("  " + v.description)
        return "\n".join(s)


def freeze(fn: Bushel) -> Bushel:
    return _FreezeDriedBushel(fn)


class _FreezeDriedBushel(Bushel):
    def __init__(self, fn):
        super().__init__(fn._values)

    def __setitem__(self, name, value):
        raise NotImplementedError("Frozen!")

    def __setattr__(self, name, value):
        raise NotImplementedError("Frozen!")


def _tupleBerry(berry, name):
    assert len(berry) == 2, f"Unsupported tuple size: {berry}"
    v, variety_desc = berry
    if isinstance(variety_desc, Variety):
        variety = variety_desc
        desc = ""
    else:
        variety = None
        desc = variety_desc
    v = Berry.of(v, variety=variety, name=name)
    v.description = desc
    return v
