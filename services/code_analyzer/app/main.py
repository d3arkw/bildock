from fastapi import FastAPI

app = FastAPI(
    title="BackDeck Code Analyzer Service",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "code_analyzer"}
