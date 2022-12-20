import ast

from aioredis import Redis

from db.protocols.cache_protocol import CacheProtocol


class RedisCache(CacheProtocol):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def _close(self):
        self.redis.close()
        await self.redis.wait_closed()

    async def _get(self, url):
        data = await self.redis.get(url)
        return ast.literal_eval(data.decode("utf-8"))

    async def _put(self, url, object, expire):
        item = bytes(str(object), "utf-8")
        await self.redis.set(
            url, item, expire=expire
        )
