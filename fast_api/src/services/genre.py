from __future__ import annotations

import json
import pickle
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from pydantic import parse_obj_as

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from repository.db_context import DbContext

GENRE_CACHE_EXPIRE_IN_SECONDS = settings.cache_expire_in_seconds


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.db_context = DbContext(redis, elastic, "genres", settings.cache_expire_in_seconds, type(Genre))

    async def get_list_genres(self, url: str, page_number, page_size) -> list[Genre] | None:
        doc = await self.db_context.get_list(url, page_number, page_size)
        return [Genre(**genre["_source"]) for genre in doc.body["hits"]["hits"]]

    async def get_genre_by_id(self, url: str, genre_id: str) -> Genre | None:
        data = await self.db_context.get_by_id(url, genre_id)
        genre = Genre(**data["_source"])
        return genre


def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
