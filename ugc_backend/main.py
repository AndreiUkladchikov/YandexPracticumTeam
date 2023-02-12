import uvicorn
from fastapi import FastAPI
from src.aggregate_to_kafka import router
from src.config import settings

app = FastAPI(
    title="ugc_backend", docs_url="/api/openapi", openapi_url="/api/openapi.json"
)


app.include_router(router.router, prefix="/views", tags=["views"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.ugc_backend_host,
        port=settings.ugc_backend_port,
    )
