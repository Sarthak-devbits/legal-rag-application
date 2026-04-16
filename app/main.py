from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import health, auth, documents
from app.services.ingestion.storage import ensure_bucket_exists
from app.api.v1 import health, auth, documents, query


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_bucket_exists()
    yield


app = FastAPI(
    title="Legal RAG API",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(health.router)
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(query.router, prefix="/api/v1/query", tags=["query"])