from langchain_openai import OpenAIEmbeddings
from app.core.config import settings
from app.services.ingestion.chunker import Chunk 

embeddings_model = OpenAIEmbeddings(
    api_key=settings.openai_api_key,
    model=settings.openai_embedding_model,
)

def embed_chunks(chunks:list[Chunk])-> list[tuple[Chunk,list[float]]]:
    texts= [chunk.text for chunk in chunks]
    vectors = embeddings_model.embed_documents(texts)
    return list(zip(chunks,vectors))