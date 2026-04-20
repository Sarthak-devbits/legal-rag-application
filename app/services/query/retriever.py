from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from pgvector.sqlalchemy import Vector
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings
from app.models.chunk import Chunk
from app.core.exceptions import ValidationError, NotFoundError

embedding_model= OpenAIEmbeddings(
    api_key=settings.openai_api_key,
    model=settings.openai_embedding_model
)

async def retrieve_chunks(
    session:AsyncSession,
    question:str,
    document_ids: list[str],
    top_k:int =20
)->list[Chunk]:
    if not question or not question.strip():
        raise ValidationError("Question cannot be empty")

    try:
        question_vector=await embedding_model.aembed_query(question)
    except Exception as e:
        raise ValidationError(f"Failed to generate embedding: {e}")

    vector_result= await session.execute(
        select(Chunk)
        .where(Chunk.document_id.in_(document_ids))
        .order_by(Chunk.embedding.cosine_distance(question_vector))
        .limit(top_k)
    )
    chunks= vector_result.scalars().all()

    if not chunks:
        raise NotFoundError("No relevant chunks found for the given documents")

    return chunks