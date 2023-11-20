from attrs import Attribute
from pathlib import Path


__all__ = ["type_validator", "check_path_exists"]


def type_validator(instance, attribute: Attribute, value):  # TODO: better
    obj = type(instance)
    d: dict[str, type] = dict()
    while obj != object:
        d.update(obj.__annotations__)
        obj = obj.__bases__[0]

    type_ = dict(d)[attribute.name]
    try:
        try:
            check = type_.__instancecheck__(value)
        except TypeError:
            check = isinstance(value, type_)
    except TypeError:
        ...
    else:
        if not check:
            raise TypeError(f'{type(instance).__name__}.{attribute.name} has incorrect type = {type(value)}. Should have {type_}')


def check_path_exists(*_, value: Path):
    if not value.exists():
        raise FileNotFoundError(f'{value}')
