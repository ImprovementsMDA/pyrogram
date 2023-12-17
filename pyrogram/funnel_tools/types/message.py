from attrs import define, field
from pathlib import Path
from pyrogram.enums import ParseMode, MessageMediaType
from typing import Optional, List

from . import Text, TextsDP, Trigger
from pyrogram.funnel_tools.utils.attrs_validators import *


__all__ = ["BaseMessage",
           "SimpleMessage",
           "MediaMessage"]


@define(kw_only=True)
class BaseMessage:
    parse_mode: Optional[ParseMode] = field(validator=type_validator, default=None)
    triggers: List[Trigger] = field(validator=type_validator, factory=list)
    delay_before_sending: int = field(init=False, default=0)

    @staticmethod
    def get_text(text_attr: Text | None | TextsDP):
        if isinstance(text_attr, TextsDP):
            return text_attr.get_text()
        return text_attr


@define
class SimpleMessage(BaseMessage):
    _text: Optional[Text | TextsDP | str] = field(validator=type_validator, default=None)

    def __attrs_post_init__(self):
        if isinstance(self._text, str) or self._text is None:
            self._text = Text(self._text)

    def get_text(self):
        return super().get_text(self._text)


@define
class MediaMessage(BaseMessage):
    media_type: MessageMediaType = field(validator=type_validator)
    media_path: Path = field(validator=[type_validator, check_path_exists])
    _caption: Optional[Text] = field(validator=type_validator, default=None)

    def get_text(self):
        return super().get_text(self._caption)
