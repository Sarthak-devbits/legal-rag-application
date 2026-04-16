from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.query import QueryRequest
from app.services.query.retriever import retrieve_chunks
from app.services.query.reranker import rerank_chunks
from app.services.query.generator import generate_answer
from app.services.query.citation_builder import build_citations

router = APIRouter()

import json

@router.post("/")
async def query_documents(
    request: QueryRequest,
    session: AsyncSession = Depends(get_db),
):
    chunks = await retrieve_chunks(
        session=session,
        question=request.question,
        document_ids=request.document_ids,
    )
    print(chunks)

    reranked_chunks = await rerank_chunks(
        question=request.question,
        chunks=chunks,
    )

    citations = build_citations(reranked_chunks)

    return StreamingResponse(
        generate_answer(request.question, reranked_chunks),
        media_type="text/event-stream",
        headers={"X-Citations": json.dumps(citations)},
    )