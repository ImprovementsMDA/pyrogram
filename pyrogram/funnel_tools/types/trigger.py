from attrs import define, field
from pyrogram import types, filters as pyro_f

from typing import Optional
from enum import Enum, auto

from pyrogram.funnel_tools.utils.attrs_validators import type_validator


__all__ = ["TriggerType",
           "BaseTrigger",
           "PayedTrigger",
           "ExpectTrigger",
           "FunnelMsgTrigger"]


class TriggerType(Enum):
    PAYED = auto()
    EXPECT = auto()
    CANCEL_FUNNEL_MSG = auto()


@define(kw_only=True)
class BaseTrigger:
    """
    trigger-phrase
    priority
    """
    type: Optional[TriggerType] = field(default="")
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
class PayedTrigger(BaseTrigger):

    type: TriggerType = field(init=False, default=TriggerType.PAYED)
    priority: int = field(init=False, default=10)
    filters: Optional[pyro_f.Filter] = field(validator=type_validator, default=(pyro_f.text | pyro_f.caption) & pyro_f.outgoing)


@define(kw_only=True)
class ExpectTrigger(PayedTrigger):

    type: TriggerType = field(init=False, default=TriggerType.EXPECT)


@define(kw_only=True)
class FunnelMsgTrigger(BaseTrigger):
    type: TriggerType = field(default=TriggerType.CANCEL_FUNNEL_MSG)
    priority: int = field(init=False, default=5)
    filters: Optional[pyro_f.Filter] = field(validator=type_validator, default=(pyro_f.text | pyro_f.caption) & pyro_f.outgoing)
