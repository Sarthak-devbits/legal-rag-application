from app.models.chunk import Chunk

def build_citations(chunks: list[Chunk]) -> list[dict]:
    return [
        {
            "chunk_index": chunk.chunk_index,
            "page_number": chunk.page_number,
            "content_preview": chunk.content[:100] + "...",
        }
        for chunk in chunks
    ]