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

    def get_text(self, tag: str | None = None) -> Text:
        # Filter by tags
        texts = [text for text in self.texts if text.tag == tag] if tag is not None else self.texts
        if not texts:
            raise ValueError(f"No texts with current tag: {tag=}")

        if self.dispatching_type == DispatchingTextType.random:
            return random.choice(texts)

        elif self.dispatching_type == DispatchingTextType.equally:
            return min(texts, key=lambda text: text.count)

        raise ValueError(f"Incorrect {self.dispatching_type.value=}")
