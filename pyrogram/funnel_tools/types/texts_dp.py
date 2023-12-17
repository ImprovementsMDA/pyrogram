import random

from attrs import define
from enum import Enum

from . import Text


__all__ = ["DispatchingTextType", "TextsDP"]


class DispatchingTextType(Enum):
    random = "RANDOM"
    equally = "EQUALLY"


@define
class TextsDP:
    texts: list[Text]
    dispatching_type: DispatchingTextType

    def get_text(self) -> Text:
        if self.dispatching_type == DispatchingTextType.random:
            return random.choice(self.texts)

        elif self.dispatching_type == DispatchingTextType.equally:
            return min(self.texts, key=lambda text: text.count)

        raise ValueError(f"Incorrect {self.dispatching_type.value=}")
