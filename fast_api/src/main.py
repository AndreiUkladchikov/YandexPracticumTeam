import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch

from fastapi import FastAPI
from loguru import logger
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core.config import settings
from db import elastic, redis


app = FastAPI(
    title="movies",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    try:
        redis.redis = await aioredis.create_redis_pool(
            f"redis://{settings.redis_host}:{settings.redis_port}",
            minsize=10,
            maxsize=20,
        )
    except ConnectionRefusedError as ce:
        logger.error("Can not connect to cache", ce)

    elastic.es = AsyncElasticsearch(
        hosts=[f"http://{settings.elastic_host}:{settings.elastic_port}"]
    )


@app.on_event("shutdown")
async def shutdown():
    try:
        redis.redis.close()
        await redis.redis.wait_closed()
    except (ConnectionRefusedError, AttributeError) as ce:
        logger.error("Can not connect to cache", ce)
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=str(settings.backend_host),
        port=settings.backend_port,
    )
