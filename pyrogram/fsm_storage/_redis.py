"""
This module has redis storage for finite-state machine based on `redis <https://pypi.org/project/redis/>`_ driver.
"""

import asyncio
import logging
import typing

from ._base import BaseStorage
from ..utils import json
from ..utils.deprecated import deprecated

if typing.TYPE_CHECKING:
    import aioredis


STATE_KEY = 'state'
STATE_DATA_KEY = 'data'
STATE_BUCKET_KEY = 'bucket'


class RedisStorage2(BaseStorage):
    """
    Busted Redis-base storage for FSM.
    Works with Redis connection pool and customizable keys prefix.

    Usage:

    .. code-block:: python3

        storage = RedisStorage2('localhost', 6379, db=5, pool_size=10, prefix='my_fsm_key')
        dp = Dispatcher(bot, storage=storage)

    And need to close Redis connection when shutdown

    .. code-block:: python3

        await dp.storage.close()

    """

    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: typing.Optional[int] = None,
            password: typing.Optional[str] = None,
            ssl: typing.Optional[bool] = None,
            pool_size: int = 10,
            loop: typing.Optional[asyncio.AbstractEventLoop] = None,
            prefix: str = "fsm",
            state_ttl: typing.Optional[int] = None,
            data_ttl: typing.Optional[int] = None,
            bucket_ttl: typing.Optional[int] = None,
            **kwargs,
    ):
        from redis.asyncio import Redis

        self._redis: typing.Optional[Redis] = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            ssl=ssl,
            max_connections=pool_size,
            decode_responses=True,
            **kwargs,
        )

        self._prefix = (prefix,)
        self._state_ttl = state_ttl
        self._data_ttl = data_ttl
        self._bucket_ttl = bucket_ttl

    @deprecated("This method will be removed in aiogram v3.0. "
                "You should use your own instance of Redis.", stacklevel=3)
    async def redis(self) -> "aioredis.Redis":
        return self._redis

    def generate_key(self, *parts):
        return ':'.join(self._prefix + tuple(map(str, parts)))

    async def close(self):
        await self._redis.close()

    async def wait_closed(self):
        pass

    async def get_state(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                        default: typing.Optional[str] = None) -> typing.Optional[str]:
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, STATE_KEY)
        return await self._redis.get(key) or self.resolve_state(default)

    async def get_data(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                       default: typing.Optional[dict] = None) -> typing.Dict:
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, STATE_DATA_KEY)
        raw_result = await self._redis.get(key)
        if raw_result:
            return json.loads(raw_result)
        return default or {}

    async def set_state(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                        state: typing.Optional[typing.AnyStr] = None):
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, STATE_KEY)
        if state is None:
            await self._redis.delete(key)
        else:
            await self._redis.set(key, self.resolve_state(state), ex=self._state_ttl)

    async def set_data(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                       data: typing.Dict = None):
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, STATE_DATA_KEY)
        if data:
            await self._redis.set(key, json.dumps(data), ex=self._data_ttl)
        else:
            await self._redis.delete(key)

    async def update_data(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                          data: typing.Dict = None, **kwargs):
        if data is None:
            data = {}
        temp_data = await self.get_data(chat=chat, user=user, default={})
        temp_data.update(data, **kwargs)
        await self.set_data(chat=chat, user=user, data=temp_data)

    def has_bucket(self):
        return True

    async def get_bucket(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                         default: typing.Optional[dict] = None) -> typing.Dict:
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, STATE_BUCKET_KEY)
        raw_result = await self._redis.get(key)
        if raw_result:
            return json.loads(raw_result)
        return default or {}

    async def set_bucket(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                         bucket: typing.Dict = None):
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, STATE_BUCKET_KEY)
        if bucket:
            await self._redis.set(key, json.dumps(bucket), ex=self._bucket_ttl)
        else:
            await self._redis.delete(key)

    async def update_bucket(self, *, chat: typing.Union[str, int, None] = None,
                            user: typing.Union[str, int, None] = None,
                            bucket: typing.Dict = None, **kwargs):
        if bucket is None:
            bucket = {}
        temp_bucket = await self.get_bucket(chat=chat, user=user)
        temp_bucket.update(bucket, **kwargs)
        await self.set_bucket(chat=chat, user=user, bucket=temp_bucket)

    async def reset_all(self, full=True):
        """
        Reset states in DB

        :param full: clean DB or clean only states
        :return:
        """
        if full:
            await self._redis.flushdb()
        else:
            keys = await self._redis.keys(self.generate_key('*'))
            await self._redis.delete(*keys)

    async def get_states_list(self) -> typing.List[typing.Tuple[str, str]]:
        """
        Get list of all stored chat's and user's

        :return: list of tuples where first element is chat id and second is user id
        """
        result = []

        keys = await self._redis.keys(self.generate_key('*', '*', STATE_KEY))
        for item in keys:
            *_, chat, user, _ = item.split(':')
            result.append((chat, user))

        return result
