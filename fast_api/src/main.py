import logging

import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core.config import settings
from core.logger import LOGGING
from db.elastic import ElasticDb
from db.redis import RedisCache
from repository import db_context


app = FastAPI(
    title="movies",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    db_context.db = ElasticDb(
        AsyncElasticsearch(hosts=[f"http://{settings.elastic_host}:{settings.elastic_port}"])
    )
    db_context.cache = RedisCache(
        await aioredis.create_redis_pool(
            f"redis://{settings.redis_host}:{settings.redis_port}", minsize=10, maxsize=20
        )
    )


@app.on_event("shutdown")
async def shutdown():
    await db_context._close()


# Подключаем роутер к серверу, указав префикс /v1/films
# Теги указываем для удобства навигации по документации
app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=str(settings.backend_host),
        port=settings.backend_port,
    )
