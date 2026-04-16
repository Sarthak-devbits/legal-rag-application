from dataclasses import dataclass
from app.services.ingestion.pdf_parser import PageContent
from langchain_text_splitters import RecursiveCharacterTextSplitter

@dataclass
class Chunk:
    text: str
    page_number: int
    chunk_index: int
    char_count: int

def chunk_pages(pages: list[PageContent], chunk_size:int =500 , overlap: int =50):
    splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
        )
    
    chunk_index=0
    chunks=[]
    
    for page in pages:
        texts= splitter.split_text(page.text)
        for text in texts:
            chunks.append(
                Chunk(
                    text=text,
                    page_number=page.page_number,
                    chunk_index=chunk_index,
                    char_count=len(text),
                )
            )
            chunk_index+=1
    
    return chunks