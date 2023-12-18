import asyncio

from attrs import define, field

from pyrogram import Client
from pyrogram.enums import ParseMode, MessageMediaType

from pathlib import Path
from typing import Optional, List

from . import Text, TextsDP, BaseTrigger
from pyrogram.funnel_tools.utils.attrs_validators import *


__all__ = ["BaseMessage",
           "SimpleMessage",
           "MediaMessage"]


@define(kw_only=True)
class BaseMessage:
    parse_mode: Optional[ParseMode] = field(validator=type_validator, default=None)
    triggers: List[BaseTrigger] = field(validator=type_validator, factory=list)
    delay_before_sending: int = field(init=False, default=0)

    @staticmethod
    def get_text(text_attr: Text | TextsDP, user_tags: list[str] = None):
        if isinstance(text_attr, TextsDP):
            return text_attr.get_text(user_tags)
        return text_attr


@define()
class SimpleMessage(BaseMessage):
    _text: Optional[Text | TextsDP | str] = field(validator=type_validator, default=None)

    def __attrs_post_init__(self):
        if isinstance(self._text, str) or self._text is None:
            self._text = Text(self._text)

    # noinspection PyMethodOverriding
    def get_text(self, user_tags: list[str]):
        return super().get_text(self._text, user_tags)

    async def send(self, client: Client, user_id: int, user_tags: list[str]):
        await asyncio.sleep(self.delay_before_sending)

        text = self.get_text(user_tags)
        await client.send_message(user_id, text=str(text), parse_mode=self.parse_mode)


@define()
class MediaMessage(BaseMessage):
    media_type: MessageMediaType = field(validator=type_validator)
    media_path: Path = field(validator=[type_validator, check_path_exists])
    caption: Optional[Text | str] = field(validator=type_validator, default=None)

    # noinspection PyMethodOverriding
    def get_text(self):
        return super().get_text(self.caption)

    def __attrs_post_init__(self):
        if isinstance(self.caption, str) or self.caption is None:
            self.caption = Text(self.caption)

    async def send(self, client: Client, user_id: int):
        await asyncio.sleep(self.delay_before_sending)

        _type = MessageMediaType

        default_args = (user_id, self.media_path)
        default_kwargs = {'parse_mode': self.parse_mode}
        text = self.get_text()

        if self.media_type == _type.AUDIO:
            await client.send_audio(*default_args, caption=str(text), **default_kwargs)
        elif self.media_type == _type.DOCUMENT:
            await client.send_document(*default_args, caption=str(text), **default_kwargs)
        elif self.media_type == _type.VIDEO:
            await client.send_video(*default_args, caption=str(text), **default_kwargs)
        elif self.media_type == _type.VIDEO_NOTE:
            await client.send_video_note(*default_args)
        else:
            raise NotImplementedError(f"For {self.media_type} didn't make function")
