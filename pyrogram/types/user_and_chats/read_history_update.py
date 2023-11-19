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


import pyrogram
from pyrogram import raw
from pyrogram.types import Object, Update


class ReadHistoryInbox(Object, Update):

    def __init__(self,
                 *,
                 client: 'pyrogram.Client',
                 peer: raw.base.Peer,
                 max_id: int,
                 still_unread_count: int,
                 folder_id: int | None = None):
        super().__init__(client)

        self.peer = peer
        self.max_id = max_id,
        self.still_unread_count = still_unread_count
        self.folder_id = folder_id

    @staticmethod
    def _parse(client: 'pyrogram.Client', update: raw.types.UpdateReadHistoryInbox) -> 'ReadHistoryInbox':
        return ReadHistoryInbox(
            client=client,
            peer=update.peer,
            max_id=update.max_id,
            still_unread_count=update.still_unread_count,
            folder_id=getattr(update, 'folder_id', None)
        )


class ReadHistoryOutbox(Object, Update):

    def __init__(self,
                 *,
                 client: 'pyrogram.Client',
                 peer: raw.base.Peer,
                 max_id: int):
        super().__init__(client)

        self.peer = peer
        self.max_id = max_id,

    @staticmethod
    def _parse(client: 'pyrogram.Client', update: raw.types.UpdateReadHistoryOutbox) -> 'ReadHistoryOutbox':
        return ReadHistoryOutbox(
            client=client,
            peer=update.peer,
            max_id=update.max_id
        )
