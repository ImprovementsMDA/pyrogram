from attrs import define, field

from . import SetAttrs


__all__ = ["Text"]


@define
class Text:
    value: str | None
    count: int = field(init=False, default=0)
    tag: str = field(default=None)
    set_attrs: SetAttrs = field(default=None)

    def success_sent(self, user):
        self.count += 1
        if self.set_attrs is not None:
            self.set_attrs.set(user)

    def __str__(self):
        if self.value is None:
            return ''
        return self.value

    __repr__ = __str__
