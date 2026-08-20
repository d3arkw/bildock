from fastapi import FastAPI

app = FastAPI(
    title="Bildock Analytics Service",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "analytics"}
