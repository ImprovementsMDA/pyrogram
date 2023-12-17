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

    def __filter_by_tags(self, user_tags: list[str] = None) -> list[Text]:
        # Filter by tags
        _texts_with_tags = [text for text in self.texts if text.tag]
        if _texts_with_tags:
            texts = [text for text in self.texts if text.tag in user_tags]
        else:
            texts = self.texts
        return texts

    def get_text(self, user_tags: list[str] = None) -> Text:
        texts = self.__filter_by_tags(user_tags)

        if not texts:
            raise ValueError(f"No texts found.")

        if self.dispatching_type == DispatchingTextType.random:
            return random.choice(texts)

        elif self.dispatching_type == DispatchingTextType.equally:
            return min(texts, key=lambda text: text.count)

        raise ValueError(f"Incorrect {self.dispatching_type.value=}")
