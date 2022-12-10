from __future__ import annotations

import pickle
import json
from typing import Any
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from pydantic import parse_obj_as

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis


class DbContext:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index: str, expire: int, type: type):
        self.redis = redis
        self.elastic = elastic
        self.index = index
        self.expire = expire
        self.type = type

    async def _put_to_cache(self, url: str, object: Any):
        await self.redis.set(
            url, object, expire=self.expire
        )

    async def _put_list_to_cache(self, url: str, items: list[Any]):
        await self.redis.set(
            url, pickle.dumps([p for p in items]), expire=self.expire
        )

    async def _get_from_cache(self, url: str) -> Any | None:
        data = await self.redis.get(url)
        if not data:
            return None

        return data

    async def _get_from_elastic(self, id: str) -> Any | None:
        try:
            doc = await self.elastic.get(index=self.index, id=id)
        except NotFoundError:
            return None
        return doc

    async def _get_list_from_elastic(
        self, page_number: int, page_size: int
    ) -> list[Any] | None:
        try:
            doc = await self.elastic.search(
                index=self.index, from_=(page_number - 1) * page_size, size=page_size
            )

        except NotFoundError:
            return None
        return doc

    async def _get_list_from_cache(self, url: str) -> list[Any] | None:
        data = await self.redis.get(url)
        if not data:
            return None

        return data

    async def get_by_id(self, url: str, id: str) -> Any | None:
        item = await self._get_from_cache(url)
        if not item:
            item = await self._get_from_elastic(id)
            if not item:
                return None

            # await self._put_to_cache(url, item)

        return item

    async def get_list(self, url: str, page_number, page_size) -> list[Any] | None:
        items = await self._get_list_from_cache(url)
        if not items:
            items = await self._get_list_from_elastic(page_number, page_size)
            if not items:
                return None
            # await self._put_list_to_cache(url, items)

        return items
