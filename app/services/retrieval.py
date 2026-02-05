from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
import numpy as np
from app.models import DocumentChunk
from app.services.embeddings import EmbeddingService


class RetrievalService:
    """Service for retrieving relevant chunks using cosine similarity (no pgvector)."""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        a = np.array(vec1)
        b = np.array(vec2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    
    def similarity_search(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
        document_name: Optional[str] = None
    ) -> List[Tuple[DocumentChunk, float]]:
        """
        Search for similar chunks using cosine similarity.
        
        Args:
            db: Database session
            query: User's question
            top_k: Number of results to return
            document_name: Optional filter by document name
            
        Returns:
            List of (DocumentChunk, similarity_score) tuples
        """
        # Create embedding for the query
        query_embedding = self.embedding_service.create_embedding(query)
        
        # Get all chunks (with optional filter)
        if document_name:
            chunks = db.query(DocumentChunk).filter(
                DocumentChunk.document_name == document_name
            ).all()
        else:
            chunks = db.query(DocumentChunk).all()
        
        if not chunks:
            return []
        
        # Calculate similarity for each chunk
        similarities = []
        for chunk in chunks:
            if chunk.embedding:
                # embedding is stored as JSON array
                chunk_embedding = chunk.embedding if isinstance(chunk.embedding, list) else chunk.embedding
                similarity = self.cosine_similarity(query_embedding, chunk_embedding)
                similarities.append((chunk, similarity))
        
        # Sort by similarity (highest first) and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
