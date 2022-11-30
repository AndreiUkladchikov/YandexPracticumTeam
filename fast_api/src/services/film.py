from __future__ import annotations

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from core.config import Settings

FILM_CACHE_EXPIRE_IN_SECONDS = Settings().CACHE_EXPIRE_IN_SECONDS


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = "movies"

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, film_id: str) -> Film | None:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        film = await self._film_from_cache(film_id)
        if not film:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            film = await self._get_film_from_elastic(film_id)
            if not film:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None
            # Сохраняем фильм  в кеш
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Film | None:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def _film_from_cache(self, film_id: str) -> Film | None:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(film_id)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        # Сохраняем данные о фильме, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set
        # pydantic позволяет сериализовать модель в json
        await self.redis.set(film.id, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def get_films_main_page(self, field: str, genre: str, page_number: int, page_size: int) -> list[Film] | None:
        order = "desc" if field[0] == '-' else "asc"
        field = field.lstrip('-')
        body = {
            "sort": [{
                field: {
                    "order": order
                }
            }]
        }
        if genre:
            filter_by_genre = {
                "query": {
                    "bool": {
                        "filter": {
                            "nested": {
                                "path": "genres",
                                "query": {
                                    "term": {
                                        "genres.id": genre
                                    }
                                }
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
                size=page_size
            )
        except NotFoundError:
            return None
        return [Film(**film["_source"]) for film in films["hits"]["hits"]]

    async def search(self, query: str, page_number: int, page_size: int) -> list[Film]:
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "title^6", "description^5", "genre^4", "actors_names^3", "writers_names^2", "director"
                    ]
                }
            }
        }
        films = await self.elastic.search(
            index=self.index,
            body=body,
            from_=(page_number - 1) * page_size,
            size=page_size
        )
        return [Film(**film["_source"]) for film in films["hits"]["hits"]]


def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
