import cohere
from app.core.config import settings
from app.models.chunk import Chunk

cohere_client= cohere.AsyncClient(api_key=settings.cohere_api_key)

async def rerank_chunks(question:str, chunks:list[Chunk], top_n:int=5)->list[Chunk]:
    if not chunks:
        return []
    
    documents = [chunk.content for chunk in chunks]

    response = await cohere_client.rerank(
        model="rerank-english-v3.0",
        query=question,
        documents=documents,
        top_n=top_n,
    )

    reranked = [chunks[result.index] for result in response.results]
    return reranked