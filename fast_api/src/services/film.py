from __future__ import annotations

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from repository.db_context import DbContext


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.db_context = DbContext(
            redis, elastic, "movies", settings.cache_expire_in_seconds
        )

    async def get_by_id(self, url: str | None, film_id: str) -> Film | None:
        data = await self.db_context.get_by_id(url, film_id)
        if not data:
            return None

        film = Film(**data["_source"])
        return film

    async def get_films_main_page(
        self, url: str, field: str, genre: str, page_number: int, page_size: int
    ) -> (list[Film] | None, int):
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

        doc = await self.db_context.get_list(url, page_number, page_size, body)
        if not doc:
            return None, None

        total_items: int = doc["hits"]["total"]["value"]
        return [Film(**film["_source"]) for film in doc["hits"]["hits"]], total_items

    async def search(
        self, url: str, query: str, page_number: int, page_size: int
    ) -> (list[Film] | None, int):
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

        doc = await self.db_context.get_list(url, page_number, page_size, body)
        if not doc:
            return None

        total_items: int = doc["hits"]["total"]["value"]
        return [Film(**film["_source"]) for film in doc["hits"]["hits"]], total_items

    async def get_films_by_person_id(
        self, url: str, page_number: int, page_size: int, person_id: str
    ):

        filter_by_person_id = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "nested": {
                                "path": "actors",
                                "query": {
                                    "bool": {
                                        "should": [
                                            {"term": {"actors.id": person_id}},
                                        ]
                                    }
                                },
                            }
                        },
                        {
                            "nested": {
                                "path": "writers",
                                "query": {
                                    "bool": {
                                        "should": [
                                            {"term": {"writers.id": person_id}},
                                        ]
                                    }
                                },
                            }
                        },
                        {
                            "nested": {
                                "path": "directors",
                                "query": {
                                    "bool": {
                                        "should": [
                                            {"term": {"directors.id": person_id}},
                                        ]
                                    }
                                },
                            }
                        },
                    ]
                }
            }
        }

        doc = await self.db_context.get_list(
            url, page_number, page_size, filter_by_person_id
        )
        total_items: int = doc["hits"]["total"]["value"]

        return [Film(**film["_source"]) for film in doc["hits"]["hits"]], total_items


def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
