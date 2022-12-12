from __future__ import annotations

import pickle
import json
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from pydantic import parse_obj_as

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = settings.cache_expire_in_seconds


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "movies"

    async def get_by_id(self, film_id: str) -> Film | None:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Film | None:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def _film_from_cache(self, film_id: str) -> Film | None:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def get_films_main_page(
        self, url: str, field: str, genre: str, page_number: int, page_size: int
    ) -> list[Film] | None:
        films_ = await self._films_from_cache(url)
        if not films_:
            order = "desc" if field[0] == "-" else "asc"
            field = field.lstrip("-")
            body = {"sort": [{field: {"order": order}}]}
            if genre:
                filter_by_genre = {
                    "query": {
                        "bool": {
                            "filter": {
                                "nested": {
                                    "path": "genres",
                                    "query": {"term": {"genres.id": genre}},
                                }
                            }
                        }
                    }
                }
                body.update(filter_by_genre)

            try:
                films = await self.elastic.search(
                    index=self.index,
                    body=body,
                    from_=(page_number - 1) * page_size,
                    size=page_size,
                )
            except NotFoundError:
                return None
            films_ = [Film(**film["_source"]) for film in films["hits"]["hits"]]
            if not films_:
                return None
            await self._put_films_to_cache(url, films_)
        return films_

    async def search(self, url: str,  query: str, page_number: int, page_size: int) -> list[Film] | None:
        films_ = await self._films_from_cache(url)
        if not films_:
            body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            "title^6",
                            "description^5",
                            "genre^4",
                            "actors_names^3",
                            "writers_names^2",
                            "director",
                        ],
                    }
                }
            }
            films = await self.elastic.search(
                index=self.index,
                body=body,
                from_=(page_number - 1) * page_size,
                size=page_size,
            )
            films_ = [Film(**film["_source"]) for film in films["hits"]["hits"]]
            if not films_:
                return None
            await self._put_films_to_cache(url, films_)
        return films_

    async def _films_from_cache(self, url: str) -> list[Film] | None:

        data = await self.redis.get(url)

        if not data:
            return None
        persons = parse_obj_as(list[Film], [json.loads(d) for d in pickle.loads(data)])
        return persons

    async def _put_films_to_cache(self, url: str, films: list[Film]):
        await self.redis.set(
            url, pickle.dumps([p.json() for p in films]), expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )


def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
