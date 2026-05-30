from fastapi import FastAPI
from app.ingestion import router as ingestion_router

app = FastAPI(
    title="Store Intelligence API",
    description="Purplle Tech Challenge 2026",
    version="1.0.0"
)

app.include_router(ingestion_router)


@app.get("/")
def root():
    return {"message": "Store Intelligence API Running"}


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }