from . import BaseMessage


__all__ = ["MessagesList"]


class MessagesList:

    def __init__(self):
        self._messages: list[BaseMessage] = []

    def __len__(self):
        return len(self._messages)

    def __getitem__(self, item: int | slice):
        return self._messages[item]

    def append(self, message: BaseMessage, delay: int | float | None = None) -> "MessagesList":
        if delay is None:
            delay = 0
        message.delay_before_sending = delay
        self._messages.append(message)
        
        return self

    def __str__(self):
        return str(self._messages)

    __repr__ = __str__
