from attrs import define, field


__all__ = ["SetAttrs"]


class _Undefined:
    ...


@define(kw_only=True)
class SetAttrs:
    tags: str | list[str] = field(default=_Undefined)
    status: str = field(default=_Undefined)

    def __attrs_post_init__(self):
        if isinstance(self.tags, str):
            self.tags = [self.tags]

    async def set(self, user):
        if not isinstance(self.tags, _Undefined):
            for tag in self.tags:
                user.tags.append(tag)

        if not isinstance(self.status, _Undefined):
            await user.awaitable_attrs.data
            user.data.status = self.status
