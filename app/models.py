from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class DocumentChunk(Base):
    """Model for storing document chunks with embeddings."""
    
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String(255), nullable=False, index=True)
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    embedding = Column(JSON)  # Stored as JSONB array (no pgvector needed)
    doc_metadata = Column("metadata", JSON)  # Renamed to avoid conflict with SQLAlchemy
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, document={self.document_name}, chunk={self.chunk_index})>"
