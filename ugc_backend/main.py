import uvicorn
from aggregate_to_kafka import dependency, router
from aiokafka import AIOKafkaProducer, errors
from api.v1 import likes, reviews
from core.config import settings
from core.custom_log import logger
from db import mongo
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(
    title="UGC Backend", docs_url="/api/openapi", openapi_url="/api/openapi.json"
)


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
    try:
        await dependency.kafka_producer.stop()
    except errors.KafkaConnectionError as kafka_error:
        logger.critical(kafka_error)


app.include_router(router.router, prefix="/views", tags=["views"])

app.include_router(likes.router, prefix="/api/v1/likes", tags=["likes"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
# app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.ugc_backend_host,
        port=settings.ugc_backend_port,
    )
