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

GENRE_CACHE_EXPIRE_IN_SECONDS = settings.CACHE_EXPIRE_IN_SECONDS


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "genres"

    async def get_list_genres(self, url: str, page_number, page_size) -> list[Genre] | None:
        print(url)
        genres = await self._list_genres_from_cache(url)
        if not genres:
            genres = await self._get_genres_from_elastic(page_number, page_size)
            if not genres:
                return None
            await self._put_list_genres_to_cache(url, genres)

        return genres

    async def _get_genres_from_elastic(
        self, page_number: int, page_size: int
    ) -> list[Genre] | None:
        try:
            doc = await self.elastic.search(
                index=self.index, from_=(page_number - 1) * page_size, size=page_size
            )

        except NotFoundError:
            return None
        return [Genre(**genre["_source"]) for genre in doc.body["hits"]["hits"]]

    async def _list_genres_from_cache(self, url: str) -> list[Genre] | None:
        data = await self.redis.get(url)
        if not data:
            return None
        persons = parse_obj_as(list[Genre], [json.loads(d) for d in pickle.loads(data)])
        return persons

    async def _put_list_genres_to_cache(self, url: str, genres: list[Genre]):
        await self.redis.set(
            url, pickle.dumps([p.json() for p in genres]), expire=GENRE_CACHE_EXPIRE_IN_SECONDS
        )

    async def get_genre_by_id(self, url: str, genre_id: str) -> Genre | None:
        genre = await self._genre_from_cache(url)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None

            await self._put_genre_to_cache(url, genre)
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.elastic.get(index="genres", id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc["_source"])

    async def _genre_from_cache(self, url: str) -> Genre | None:
        data = await self.redis.get(url)
        if not data:
            return None

        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, url: str, genre: Genre):
        await self.redis.set(
            url, genre.json(), expire=GENRE_CACHE_EXPIRE_IN_SECONDS
        )


def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
