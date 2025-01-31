# Member Math

> 'Member how you computed that value?  
> I 'member!

A simple, write-once, read-many data structure that remembers exactly how you computed each value in it.

`Bushel` and `Variety` are the only types you need.  
From there, all your `Berry`s will grow healthily on the vine by assignment.

A `Bushel` works like a dictionary.  
Or an object with all the properties you want.  
Properties make the syntax more digestable.

```python
_ = Bushel()
_.fizz = 1
_.buzz = 2
_.fizzbuzz = _.fizz + _.buzz
print(_.fizzbuzz)
```

`Bushel`s can be given a prefix to use for all its values since values can be
used across multiple `Bushel` instances. Names are based on the prefix and the
property name or the stringified version of the key instance.

Underneath, all the values in the Bushels are implemented as `Berry`s.  
`Berry` implements all the dunder methods you can think of and returns berries
from them. Keeping all the berries in the bushel isn't a requirement but it's
recommended since it will help you create and keep track of all your berries.

## Exchanging your `Berry`s

A `Berry` can have a `Variety`. This `Variety` has a name, a symbol, an optional
format string and optional dictionaries to convert between other `Variety`s.

```python
Blueberry = Variety("BLU", "🫐", current_rates={"SBY": 3})
Strawberry = Variety("SBY", "🍓")
_ = Bushel()
_.b = 12, Blueberry
_.s = _.b >> Strawberry
```

You can also slap a `date` on your `Berry`s to keep the exchange fresh.

```python
from datetime import date
Blueberry = Variety("BLU", "🫐", day_based_rates={"SBY": {"2025-01-31": 2}})
Strawberry = Variety("SBY", "🍓")
_ = Bushel()
_.b = 12, Blueberry
_.s = _.b @ date.today() >> Strawberry
```

## Berry picking

Once you have all your inputs added and calculations defined,  
you can access the `formula`, `value`, and `variety` of your `Berry`s:

```bash
s=(12.00 BLU<🫐🍓>3 SBY)
4
🍓
```

## Why `Berry`s and `Bushel`s?

It's cute. I liked the word play of the reference and math.
