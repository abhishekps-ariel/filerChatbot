from pypdf import PdfReader
from docx import Document
from typing import List, Tuple
import io


class SimpleTextSplitter:
    """Simple text splitter without external dependencies."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap."""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence or word boundary
            if end < text_length:
                # Look for sentence end
                last_period = chunk.rfind('. ')
                if last_period > self.chunk_size // 2:
                    end = start + last_period + 2
                    chunk = text[start:end]
                else:
                    # Look for word boundary
                    last_space = chunk.rfind(' ')
                    if last_space > self.chunk_size // 2:
                        end = start + last_space
                        chunk = text[start:end]
            
            chunks.append(chunk.strip())
            start = end - self.chunk_overlap
        
        return [c for c in chunks if c]  # Remove empty chunks


class DocumentProcessor:
    """Process PDF documents and split them into chunks."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = SimpleTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file."""
        try:
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)
            
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_text_from_docx(self, file_content: bytes) -> str:
        """Extract text from Word (DOCX) file."""
        try:
            docx_file = io.BytesIO(file_content)
            doc = Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # Also extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += cell.text + " "
                    text += "\n"
            
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to extract text from DOCX: {str(e)}")
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        if not text:
            raise ValueError("Text is empty")
        
        chunks = self.text_splitter.split_text(text)
        return chunks
    
    def process_document(self, file_content: bytes, filename: str) -> Tuple[List[str], dict]:
        """
        Process document file (PDF or DOCX): extract text and chunk it.
        
        Returns:
            Tuple of (chunks, metadata)
        """
        # Determine file type and extract text
        if filename.lower().endswith('.pdf'):
            text = self.extract_text_from_pdf(file_content)
            file_type = "PDF"
        elif filename.lower().endswith('.docx'):
            text = self.extract_text_from_docx(file_content)
            file_type = "DOCX"
        else:
            raise ValueError(f"Unsupported file type. Only PDF and DOCX are supported.")
        
        # Create chunks
        chunks = self.chunk_text(text)
        
        # Create metadata
        metadata = {
            "filename": filename,
            "file_type": file_type,
            "total_chunks": len(chunks),
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "total_characters": len(text)
        }
        
        return chunks, metadata
