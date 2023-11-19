from typing import Callable

from .handler import Handler
from pyrogram.filters.state import State, any_state


class ReadHistoryInboxHandler(Handler):
    """
    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the handler.

        read_history_inbox (:obj:`~pyrogram.types.ReadHistoryInbox`):
            The received chat member update.
    """

    def __init__(self, callback: Callable, filters=None, state: State | None = any_state):
        super().__init__(callback, filters, state)
