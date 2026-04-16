from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chunk import Chunk

async def bulk_insert_chunks(session:AsyncSession, document_id: str, chunks_with_embeddings: list[tuple]):
    chunk_object=[]
    
    for chunk, embedding in chunks_with_embeddings:
        chunk_object.append(
            Chunk(
                document_id=document_id,
                page_number=chunk.page_number,
                chunk_index=chunk.chunk_index,
                content=chunk.text,
                embedding=embedding,
            )
        )
    session.add_all(chunk_object)
    await session.flush()
    return len(chunk_object)
    