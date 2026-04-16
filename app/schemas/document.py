from pydantic import BaseModel
import uuid

class UploadResponse(BaseModel):
    document_id: uuid.UUID
    filename: str
    status: str
    message: str

class DocumentStatusResponse(BaseModel):
    document_id: uuid.UUID
    filename: str
    status: str
    total_chunks: int