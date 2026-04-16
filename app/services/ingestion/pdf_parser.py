import fitz
from dataclasses import dataclass

@dataclass
class PageContent:
    page_number: int
    text: str
    char_count: int
    
def parse_pdf(file_data:bytes)->list[PageContent]:
    pages=[]
    
    # opens PDF from bytes in memory, no need to save to disk first
    with fitz.open(stream=file_data, filetype="pdf") as doc:
        for page_num, page in enumerate(doc,start=1):
            text = page.get_text().strip()
            if text:
                pages.append(PageContent(
                    page_number=page_num,
                    text=text,
                    char_count=len(text),
                ))
                
    return pages