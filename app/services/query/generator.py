from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage
from app.core.config import settings
from app.models.chunk import Chunk

chat_model= ChatOpenAI(
    api_key= settings.openai_api_key,
    model=settings.openai_chat_model,
    streaming=True,
    temperature=0
)


async def generate_answer(
    question: str,
    chunks: list[Chunk],
):
    context = "\n\n".join([
        f"[Page {chunk.page_number}, Chunk {chunk.chunk_index}]\n{chunk.content}"
        for chunk in chunks
    ])
 
    messages = [
        SystemMessage(content="""You are a legal document assistant. 
        Answer questions based only on the provided context.
        Always cite the page number when referencing information.
        If the answer is not in the context, say 'I cannot find this information in the provided documents.'"""),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {question}"),
    ]
    
    async for token in chat_model.astream(messages):
        yield token.content
        