import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.aggregate_to_kafka import router
from src.config import settings

app = FastAPI(
    title="UGCBackend",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


app.include_router(router.router, prefix="/views", tags=["views"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.ugc_backend_host,
        port=settings.ugc_backend_port,
    )
