import uvicorn
from aggregate_to_kafka import router
from config import settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title="UGCBackend",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    try:
        pass
    except Exception:
        pass


@app.on_event("shutdown")
async def shutdown():
    try:
        pass
    except (ConnectionRefusedError, AttributeError):
        pass


app.include_router(router.router, prefix="/views", tags=["views"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=str(settings.ugc_backend_host),
        port=settings.ugc_backend_port,
    )
