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


class Handler:
    def __init__(self, callback: Callable, filters: Filter = None):
        self.callback = callback
        self.filters = filters
        self._spec = self._get_spec()

    def _get_spec(self):
        func = self.callback
        while hasattr(func, '__wrapped__'):  # Try to resolve decorated callbacks
            func = func.__wrapped__
        return inspect.getfullargspec(func)

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

