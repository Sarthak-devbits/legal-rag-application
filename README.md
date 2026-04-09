# Legal RAG API

A production-ready **Retrieval-Augmented Generation (RAG)** backend for legal document intelligence. Built with FastAPI, it ingests legal PDFs, chunks and embeds them, stores vectors, and answers natural-language queries with cited, source-grounded responses.

---

## Architecture Overview

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│  Client App │───▶│  FastAPI API │───▶│  Celery Workers │
└─────────────┘    └──────┬───────┘    └────────┬────────┘
                          │                      │
              ┌───────────▼──────────┐           │
              │  PostgreSQL + pgvector◀──────────┘
              └──────────────────────┘
                          │
              ┌───────────▼──────────┐
              │  Redis (cache/queue) │
              └──────────────────────┘
```

### Ingestion Pipeline

```
PDF Upload ──▶ PDF Parser ──▶ Chunker ──▶ Deduplicator ──▶ Embedder ──▶ Vector Store
```

### Query Pipeline

```
User Query ──▶ Query Expander ──▶ Retriever ──▶ Reranker ──▶ Generator ──▶ Citation Builder ──▶ Response
```

---

## Project Structure

```
legal-rag-api/
├── app/
│   ├── api/v1/
│   │   ├── auth.py              # JWT authentication endpoints
│   │   ├── documents.py         # Document upload & management
│   │   ├── query.py             # RAG query endpoint
│   │   └── health.py            # Health check
│   ├── core/
│   │   ├── config.py            # Settings (env-based)
│   │   ├── security.py          # JWT / password hashing
│   │   ├── rate_limit.py        # Request rate limiting
│   │   ├── exceptions.py        # Custom exception handlers
│   │   ├── logging.py           # Structured logging
│   │   └── tracing.py           # OpenTelemetry tracing
│   ├── middleware/
│   │   ├── auth_middleware.py   # Token validation middleware
│   │   ├── correlation.py       # Correlation ID injection
│   │   └── timing.py            # Request timing
│   ├── models/
│   │   ├── user.py              # User ORM model
│   │   ├── document.py          # Document ORM model
│   │   ├── chunk.py             # Chunk + embedding ORM model
│   │   └── job.py               # Async job ORM model
│   ├── schemas/
│   │   ├── auth.py              # Auth request/response schemas
│   │   ├── document.py          # Document schemas
│   │   ├── query.py             # Query/response schemas
│   │   └── job.py               # Job status schemas
│   ├── repositories/
│   │   ├── user_repo.py         # User DB operations
│   │   ├── document_repo.py     # Document DB operations
│   │   ├── chunk_repo.py        # Chunk/vector DB operations
│   │   └── job_repo.py          # Job DB operations
│   ├── services/
│   │   ├── auth_service.py      # Auth business logic
│   │   ├── ingestion/
│   │   │   ├── pdf_parser.py    # PDF text extraction
│   │   │   ├── chunker.py       # Text chunking strategies
│   │   │   ├── deduplicator.py  # Chunk deduplication
│   │   │   ├── embedder.py      # Embedding model client
│   │   │   └── storage.py       # Object storage (S3/local)
│   │   └── query/
│   │       ├── expander.py          # Query expansion / rewriting
│   │       ├── retriever.py         # Vector + keyword retrieval
│   │       ├── reranker.py          # Cross-encoder reranking
│   │       ├── generator.py         # LLM answer generation
│   │       ├── citation_builder.py  # Source citation assembly
│   │       └── cache.py             # Semantic query caching
│   ├── workers/
│   │   ├── celery_app.py        # Celery configuration
│   │   ├── ingestion_worker.py  # Async ingestion tasks
│   │   ├── query_worker.py      # Async query tasks
│   │   └── dead_letter.py       # Failed task handling
│   └── db/
│       ├── session.py           # SQLAlchemy session factory
│       ├── base.py              # Declarative base
│       └── migrations/          # Alembic migrations
├── scripts/
│   ├── seed_db.py               # Database seeding
│   ├── check_health.py          # Health verification script
│   └── benchmark.py             # Performance benchmarking
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
└── pyproject.toml
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI (Python 3.13) |
| Database | PostgreSQL + pgvector |
| Task Queue | Celery + Redis |
| Cache | Redis |
| Embeddings | Configurable (OpenAI / local model) |
| LLM | Configurable (OpenAI / Anthropic) |
| Migrations | Alembic |
| Auth | JWT (Bearer tokens) |
| Tracing | OpenTelemetry |
| Containerization | Docker / Docker Compose |

---

## Getting Started

### Prerequisites

- Python 3.13+
- Docker & Docker Compose
- `uv` (recommended) or `pip`

### 1. Clone & Configure

```bash
git clone <repo-url>
cd legal-rag-api
cp .env.example .env
# Edit .env with your credentials
```

### 2. Start Infrastructure

```bash
docker compose up -d
```

This starts PostgreSQL (with pgvector extension) and Redis.

### 3. Install Dependencies

```bash
uv sync
# or: pip install -e .
```

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

### 6. Start Celery Worker

```bash
celery -A app.workers.celery_app worker --loglevel=info
```

API available at `http://localhost:8000` — Interactive docs at `http://localhost:8000/docs`

---

## API Endpoints

### Auth

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register a new user |
| `POST` | `/api/v1/auth/login` | Obtain JWT token |
| `POST` | `/api/v1/auth/refresh` | Refresh access token |

### Documents

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/documents` | Upload a legal PDF |
| `GET` | `/api/v1/documents` | List all documents |
| `GET` | `/api/v1/documents/{id}` | Get document details |
| `DELETE` | `/api/v1/documents/{id}` | Delete a document |
| `GET` | `/api/v1/documents/{id}/status` | Ingestion job status |

### Query

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/query` | Ask a question over ingested documents |

### Health

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/health` | Service health check |

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/legal_rag

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Embeddings
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=sk-...

# LLM
LLM_MODEL=gpt-4o
LLM_PROVIDER=openai   # or: anthropic

# Storage
STORAGE_BACKEND=local  # or: s3
S3_BUCKET=legal-docs
AWS_REGION=us-east-1
```

---

## Development

```bash
# Seed the database with test data
python scripts/seed_db.py

# Run the benchmark suite
python scripts/benchmark.py

# Verify all services are healthy
python scripts/check_health.py

# Run tests
pytest
```

---

## Key Features

- **Async-first** — Non-blocking I/O throughout; long ingestion jobs run in Celery workers.
- **Deduplication** — Chunks are deduplicated before embedding to avoid redundant vector entries.
- **Query expansion** — Queries are rewritten/expanded before retrieval to improve recall.
- **Reranking** — Retrieved chunks are reranked with a cross-encoder before LLM generation.
- **Citations** — Every answer includes source citations with document name, page, and chunk reference.
- **Semantic caching** — Repeated or semantically similar queries are served from cache.
- **Rate limiting** — Per-user rate limits enforced at the middleware layer.
- **Observability** — Structured logging, correlation IDs, request timing, and OpenTelemetry tracing.
- **Dead-letter handling** — Failed Celery tasks are captured and stored for inspection.

---

## Status

> **This project is currently in active scaffolding / early development.**
> The architecture and directory structure are fully defined. Implementation is in progress.

---

## License

MIT
# legal-rag-application
