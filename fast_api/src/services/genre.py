from __future__ import annotations

from aioredis import Redis
from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.genre import Genre
from repository.db_context import DbContext


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.db_context = DbContext(
            redis, elastic, "genres", settings.cache_expire_in_seconds
        )

    async def get_list_genres(
        self, url: str, page_number, page_size
    ) -> (list[Genre] | None, int | None):
        doc = await self.db_context.get_list(url, page_number, page_size)
        if not doc:
            return None
        total_items: int = doc["hits"]["total"]["value"]

        return [Genre(**genre["_source"]) for genre in doc["hits"]["hits"]], total_items

    async def get_genre_by_id(self, url: str, genre_id: str) -> Genre | None:
        data = await self.db_context.get_by_id(url, genre_id)
        if not data:
            return None

        genre = Genre(**data["_source"])
        return genre


def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
