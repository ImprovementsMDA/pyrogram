from attrs import define, field
from pyrogram import types, filters as pyro_f
from typing import Optional

from pyrogram.funnel_tools.utils.attrs_validators import type_validator


__all__ = ["Trigger",
           "PayedTrigger",
           "FunnelMsgTrigger"]


@define(kw_only=True)
class Trigger:
    """
    trigger-phrase
    priority
    """
    phrase: str = field(validator=type_validator)
    case_ignore: bool = field(validator=type_validator, default=True)
    priority: int = field(validator=type_validator, default=0)
    filters: Optional[pyro_f.Filter] = field(validator=type_validator, default=None)

    async def check_msg(self, message: types.Message) -> bool:
        # noinspection PyProtectedMember
        if await self.filters(message._client, message):
            text = message.text if message.text else message.caption
            if text:
                if self.case_ignore:
                    return self.phrase.lower() in text.lower()
                return self.phrase in text
        return False


@define(kw_only=True)
class PayedTrigger(Trigger):
    priority: int = field(init=False, default=10)
    filters: Optional[pyro_f.Filter | None] = field(validator=type_validator, default=(pyro_f.text | pyro_f.caption) & pyro_f.outgoing)


@define(kw_only=True)
class FunnelMsgTrigger(Trigger):
    priority: int = field(init=False, default=5)
    filters: Optional[pyro_f.Filter | None] = field(validator=type_validator, default=(pyro_f.text | pyro_f.caption) & pyro_f.outgoing)

