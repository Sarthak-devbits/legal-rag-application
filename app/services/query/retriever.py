from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from pgvector.sqlalchemy import Vector
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings
from app.models.chunk import Chunk

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
    question_vector=await embedding_model.aembed_query(question)

    vector_result= await session.execute(
        select(Chunk)
        .where(Chunk.document_id.in_(document_ids))
        .order_by(Chunk.embedding.cosine_distance(question_vector))
        .limit(top_k)
    )
    chunks= vector_result.scalars().all()
    return chunks