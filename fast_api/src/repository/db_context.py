from __future__ import annotations

import ast
from typing import Any
from aioredis import Redis
from loguru import logger
import elasticsearch
from elasticsearch import AsyncElasticsearch
from repository.custom_exceptions import ElasticSearchIsNotAvailable


class DbContext:
    def __init__(
        self, redis: Redis, elastic: AsyncElasticsearch, index: str, expire: int
    ):
        self.redis = redis
        self.elastic = elastic
        self.index = index
        self.expire = expire

    async def _put_to_cache(self, url: str, object: Any):
        try:
            await self.redis.set(url, object, expire=self.expire)
        except (ConnectionRefusedError, AttributeError) as ce:
            logger.error("Enable put data to cache", ce)

    async def _get_from_cache(self, url: str) -> Any | None:
        try:
            data = await self.redis.get(url)
        except (ConnectionRefusedError, AttributeError) as ce:
            logger.error("Enable get data from cache", ce)
            data = None
        if not data:
            return None

        return ast.literal_eval(data.decode("utf-8"))

    async def _get_from_elastic(self, id: str) -> Any | None:
        try:
            doc = await self.elastic.get(index=self.index, id=id)
        except elasticsearch.ConnectionError as ce:
            logger.critical("Enable get data from ElasticSearch", ce)
            raise ElasticSearchIsNotAvailable
        return doc

    async def _get_list_from_elastic(
        self, body: Any, page_number: int, page_size: int
    ) -> list[Any] | None:
        try:
            doc = await self.elastic.search(
                index=self.index,
                body=body,
                from_=(page_number - 1) * page_size,
                size=page_size,
            )
        except elasticsearch.ConnectionError as ce:
            logger.critical("Enable get data from ElasticSearch", ce)
            raise ElasticSearchIsNotAvailable
        return doc

    async def get_by_id(self, url: str | None, id: str) -> Any | None:
        if url:
            item = await self._get_from_cache(url)
            if not item:
                item = await self._get_from_elastic(id)
                if not item:
                    return None
                await self._put_to_cache(url, bytes(str(item), "utf-8"))
        else:
            item = await self._get_from_elastic(id)
            if not item:
                return None
        return item

    async def get_list(
        self, url: str, page_number, page_size, body=None
    ) -> list[Any] | None:
        items = await self._get_from_cache(url)
        if not items:
            items = await self._get_list_from_elastic(body, page_number, page_size)
            if not items:
                return None
            await self._put_to_cache(url, bytes(str(items), "utf-8"))

        return items
