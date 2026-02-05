from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class IngestRequest(BaseModel):
    """Request schema for document ingestion."""
    pass  # File will be uploaded as multipart/form-data


class IngestResponse(BaseModel):
    """Response schema for document ingestion."""
    success: bool
    document_name: str
    chunks_created: int
    message: str


class ChatRequest(BaseModel):
    """Request schema for chat."""
    question: str = Field(..., min_length=1, description="User's question")
    document_name: Optional[str] = Field(None, description="Filter by specific document")
    top_k: Optional[int] = Field(5, ge=1, le=10, description="Number of chunks to retrieve")


class SourceChunk(BaseModel):
    """Source chunk used in answer generation."""
    chunk_text: str
    document_name: str
    chunk_index: int
    similarity_score: float


class ChatResponse(BaseModel):
    """Response schema for chat."""
    answer: str
    sources: List[SourceChunk]
    openai_model: str  # Renamed from model_used to avoid conflict


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    database_connected: bool
    openai_configured: bool
