from __future__ import annotations

from typing import Any, Optional
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from db.protocols.db_protocol import DbProtocol
from db.protocols.cache_protocol import CacheProtocol


db: Optional[DbProtocol] = None
cache: Optional[CacheProtocol] = None
expire: Optional[int] = None


async def _close():
    await db._close()
    await cache._close()


async def get_by_id(url: str | None, id: str, index: str) -> Any | None:
    if url:
        item = await __get_from_cache(url)
        if not item:
            item = await __get_from_db(index, id)
            if not item:
                return None
            await __put_to_cache(url, item)
    else:
        item = await __get_from_db(index, id)
        if not item:
            return None
    return item


async def get_list(self, url: str, page_number, page_size, body=None) -> list[Any] | None:
    items = await self._get_from_cache(url)
    if not items:
        items = await self._get_list_from_elastic(body, page_number, page_size)
        if not items:
            return None
        await self._put_to_cache(url, bytes(str(items), "utf-8"))

    return items

# Private section


async def __put_to_cache(url: str, object: Any):
    await cache._put(
        url, object, expire=expire
    )


async def __get_from_cache(url: str) -> Any | None:
    data = await cache._get(url)
    if not data:
        return None

    return data


async def __get_from_db(index: str, id: str) -> Any | None:
    try:
        doc = await db._get_by_id(index=index, id=id)
    except NotFoundError:
        return None
    return doc


async def __get_list_from_elastic(
    self, body: Any, page_number: int, page_size: int
) -> list[Any] | None:
    try:
        if body is None:
            doc = await self.elastic.search(
                index=self.index, from_=(page_number - 1) * page_size, size=page_size
            )
        else:
            doc = await self.elastic.search(
                index=self.index, body=body, from_=(page_number - 1) * page_size, size=page_size
            )

    except NotFoundError:
        return None
    return doc
