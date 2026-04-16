import asyncio
from app.workers.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.services.ingestion.storage import download_file
from app.services.ingestion.pdf_parser import parse_pdf
from app.services.ingestion.chunker import chunk_pages
from app.services.ingestion.embedder import embed_chunks
from app.repositories.chunk_repo import bulk_insert_chunks
from app.repositories.document_repo import update_document_status


async def _ingest_document(document_id:str, file_path:str):
    async with AsyncSessionLocal() as session:
        try:
            await update_document_status(session=session,document_id=document_id,status="processing")
            await session.commit()
            
            file_data = await download_file(file_path)

            pages = parse_pdf(file_data)

            chunks = chunk_pages(pages)

            chunks_with_embeddings = embed_chunks(chunks)

            total_chunks = await bulk_insert_chunks(
                session,
                document_id,
                chunks_with_embeddings,
            )

            await update_document_status(session, document_id, "completed", total_chunks)
            await session.commit()
        except Exception as e:
                await update_document_status(session, document_id, "failed")
                await session.commit()
                raise e


@celery_app.task( 
    name="ingest_document",
    queue="ingestion_queue",
    max_retries=3,
    default_retry_delay=60)
def ingest_document(document_id:str, file_path:str):
    asyncio.run(_ingest_document(document_id=document_id, file_path=file_path))