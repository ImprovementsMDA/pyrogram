from . import BaseMessage


__all__ = ["MessagesList"]


class MessagesList:

    def __init__(self):
        self._messages: list[BaseMessage] = []

    def append(self, message: BaseMessage, delay: int | float | None = None) -> None:
        if delay is None:
            delay = 0
        message.delay_before_sending = delay
        self._messages.append(message)

    def __str__(self):
        return str(self._messages)

    __repr__ = __str__
