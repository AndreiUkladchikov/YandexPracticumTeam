import uvicorn
import sentry_sdk
from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.routing import Match
from aiokafka import AIOKafkaProducer, errors

from aggregate_to_kafka import dependency, router
from api.v1 import likes, reviews, user_bookmarks
from core.config import settings
from core.custom_log import logger
from db import mongo


sentry_sdk.init(
    dsn=settings.sentry_url,
    traces_sample_rate=settings.sentry_traces_sample_rate,
)

app = FastAPI(
    title="UGC Backend", docs_url="/api/openapi", openapi_url="/api/openapi.json"
)


@app.middleware("http")
async def log_middle(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    routes = request.app.router.routes
    logger.debug("Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")

    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup_event():
    try:
        dependency.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}"
        )
        await dependency.kafka_producer.start()

    except errors.KafkaConnectionError as kafka_error:
        logger.critical(kafka_error)
        # raise kafka_error

    mongo.mongo_client = AsyncIOMotorClient(settings.mongo)


@app.on_event("shutdown")
async def shutdown_event():
    mongo.mongo_client.close()
    try:
        await dependency.kafka_producer.stop()
    except errors.KafkaConnectionError as kafka_error:
        logger.critical(kafka_error)


app.include_router(router.router, prefix="/views", tags=["views"])

app.include_router(likes.router, prefix="/api/v1/likes", tags=["likes"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
app.include_router(
    user_bookmarks.router, prefix="/api/v1/bookmarks", tags=["bookmarks"]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.ugc_backend_host,
        port=settings.ugc_backend_port,
    )
