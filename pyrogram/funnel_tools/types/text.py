from attrs import define, field


__all__ = ["Text"]


@define
class Text:
    value: str | None
    count: int = field(init=False, default=0)

    def success_sent(self):
        self.count += 1
