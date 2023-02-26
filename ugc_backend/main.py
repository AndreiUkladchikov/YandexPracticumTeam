import uvicorn
from aiokafka import AIOKafkaProducer, errors
from fastapi import FastAPI
import sentry_sdk
from src.aggregate_to_kafka import dependency, router
from src.config import settings
from src.custom_log import logger


sentry_sdk.init(
    dsn="https://fac7f1bdbad04347bd4f8e12a0f31b3a@o4504746002612224.ingest.sentry.io/4504746011394048",
    traces_sample_rate=0.05,
)

app = FastAPI(
    title="ugc_backend", docs_url="/api/openapi", openapi_url="/api/openapi.json"
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


@app.on_event("shutdown")
async def shutdown_event():
    try:
        await dependency.kafka_producer.stop()
    except errors.KafkaConnectionError as kafka_error:
        logger.critical(kafka_error)
        raise kafka_error


app.include_router(router.router, prefix="/views", tags=["views"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.ugc_backend_host,
        port=settings.ugc_backend_port,
    )
