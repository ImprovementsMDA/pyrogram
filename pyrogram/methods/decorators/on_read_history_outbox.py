from typing import Callable

import pyrogram
from pyrogram.filters import Filter
from pyrogram.filters.state import State, any_state


class OnReadHistoryOutbox:
    def on_read_history_outbox(
        self=None,
        filters=None,
        group: int = 0,
            state: State | None = any_state
    ) -> Callable:
        """Decorator for handling read history outbox

        This does the same thing as :meth:`~pyrogram.Client.add_handler` using the
        :obj:`~pyrogram.handlers.ReadHistoryOutboxHandler`.

        Parameters:
            filters (:obj:`~pyrogram.filters`, *optional*):
                in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.

            state (:obj:`pyrogram.filters.state.State`, *optional*):
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(pyrogram.handlers.ReadHistoryOutboxHandler(func, filters, state), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.ReadHistoryOutboxHandler(func, self, state),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator