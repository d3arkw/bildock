from app.routers import router
from bildock_lib.exceptions import register_exception_handlers
from fastapi import FastAPI

app = FastAPI(
    title="Bildock Auth Service",
    version="0.1.0",
)

register_exception_handlers(app)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "auth"}


app.include_router(router, prefix="/api/v1")
