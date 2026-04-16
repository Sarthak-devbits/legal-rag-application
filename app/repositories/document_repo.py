from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.document import Document

async def get_document_by_hash(session:AsyncSession, sha256_hash:str) -> Document | None:
    result = await session.execute(select(Document).where(Document.sha256_hash==sha256_hash))
    return result.scalar_one_or_none()


async def create_document(session:AsyncSession,  user_id: str,filename: str, file_path: str, sha256_hash: str,) -> Document:
    document = Document(
        user_id=user_id,
        filename=filename,
        file_path=file_path,
        sha256_hash=sha256_hash,
    )
    session.add(document)
    await session.flush()
    
    return document


async def update_document_status(session:AsyncSession,document_id: str, status:str, total_chunks:int = None ):
    result = await session.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()
    
    if document:
        document.status= status
        if total_chunks is not None:
            document.total_chunks=total_chunks
        await session.flush()
    
    return document