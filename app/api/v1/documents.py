import hashlib
import uuid
from typing import Annotated, List
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.document import UploadResponse, DocumentStatusResponse
from app.repositories.document_repo import get_document_by_hash, create_document, update_document_status
from app.services.ingestion.storage import upload_file
from pydantic.json_schema import SkipJsonSchema
from app.workers.ingestion_worker import ingest_document
from app.core.exceptions import ValidationError, DuplicateError

router= APIRouter()

@router.post("/upload", response_model=list[UploadResponse])
async def upload_document(files: Annotated[List[UploadFile], File()] , session:AsyncSession=Depends(get_db)):
    if len(files) > 5:
        raise ValidationError("Maximum 5 files allowed at once")

    results=[]
    for file in files:
        if not file.filename.endswith(".pdf"):
            raise ValidationError(f"{file.filename} is not a PDF")

        # read file bytes
        file_data = await file.read()

        # generate hash for deduplication
        sha256_hash = hashlib.sha256(file_data).hexdigest()

        # check for duplicate
        existing = await get_document_by_hash(session, sha256_hash)
        if existing:
            raise DuplicateError(f"{file.filename} already uploaded")

        # upload to MinIO
        file_path = f"{uuid.uuid4()}.pdf"
        await upload_file(file_path, file_data, "application/pdf")

        # create document record in DB
        document = await create_document(
            session,
            user_id=uuid.uuid4(),
            filename=file.filename,
            file_path=file_path,
            sha256_hash=sha256_hash,
        )
        
        ingest_document.delay(
            document_id=str(document.id),
            file_path=file_path,
        )
        
        results.append(UploadResponse(
            document_id=document.id,
            filename=document.filename,
            status=document.status,
            message="Document uploaded successfully, ingestion started",
        ))
        
    return results