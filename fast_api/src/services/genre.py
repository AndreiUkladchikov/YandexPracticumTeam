from __future__ import annotations

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from core.config import settings

GENRE_CACHE_EXPIRE_IN_SECONDS = settings.CACHE_EXPIRE_IN_SECONDS


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "genres"

    async def get_list_genres(self, page_number, page_size) -> list[Genre] | None:
        genres = await self._get_genres_from_elastic(page_number, page_size)
        if not genres:
            return None
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

    async def get_genre_by_id(self, genre_id: str) -> Genre | None:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None

            await self._put_genre_to_cache(genre)
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.elastic.get(index="genres", id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc["_source"])

    async def _genre_from_cache(self, genre_id: str) -> Genre | None:
        data = await self.redis.get(genre_id)
        if not data:
            return None

        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(
            genre.id, genre.json(), expire=GENRE_CACHE_EXPIRE_IN_SECONDS
        )


def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
