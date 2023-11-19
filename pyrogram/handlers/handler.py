#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import inspect
from typing import Callable

import pyrogram
from pyrogram.filters import Filter
from pyrogram.types import Update

from pyrogram.filters.state import State, any_state
from pyrogram.fsm_storage import BaseStorage, FSMContext
from pyrogram.utils.deprecated import warn_deprecated as warn


class Handler:
    def __init__(self,
                 callback: Callable,
                 filters: Filter = None,
                 state: State | None = None
                 ):
        self.callback = callback
        self.filters = filters
        self.state = state
        self._spec = self._get_spec()

    def _get_spec(self):
        func = self.callback
        while hasattr(func, '__wrapped__'):  # Try to resolve decorated callbacks
            func = func.__wrapped__
        return inspect.getfullargspec(func)

    async def check_by_state(self, update: Update, storage: BaseStorage) -> FSMContext | None:
        """FSMContext if can go next code, else will skip current handler"""
        chat_id = None
        user_id = None

        if isinstance(update, pyrogram.types.User):
            user_id = update.id

        elif isinstance(update, (pyrogram.types.ReadHistoryInbox, pyrogram.types.ReadHistoryOutbox)):
            user_id = update.peer.user_id

        else:
            if hasattr(update, 'from_user') and isinstance(update.from_user, pyrogram.types.User):
                user_id = update.from_user.id

            if hasattr(update, 'chat') and isinstance(update.chat, pyrogram.types.Chat):
                chat_id = update.chat.id
                if update.chat.type.value == pyrogram.enums.ChatType.PRIVATE:
                    user_id = chat_id

        if chat_id is None and user_id is None:
            warn(f"{type(update)} in getting state has 2 None values: {chat_id=} {user_id=}.\nFull-info: {update}")
            return None

        if self.state is not None and self.state.state == any_state:
            return FSMContext(storage, chat=chat_id, user=user_id)

        state = await storage.get_state(chat=chat_id, user=user_id)
        if state == (self.state.state if self.state is not None else None):
            return FSMContext(storage, chat=chat_id, user=user_id)

    async def check(self, client: "pyrogram.Client", update: Update):
        if callable(self.filters):
            if inspect.iscoroutinefunction(self.filters.__call__):
                return await self.filters(client, update)
            else:
                return await client.loop.run_in_executor(
                    client.executor,
                    self.filters,
                    client, update
                )

        return True

    def filter_data(self, data: dict):
        if self._spec.varkw:
            return data

        new = {k: v for k, v in data.items() if k in set(self._spec.args + self._spec.kwonlyargs)}
        return new

