from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    document_ids: list[str]

class Citation(BaseModel):
    chunk_index: int
    page_number: int
    content_preview: str

class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]