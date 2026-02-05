import google.generativeai as genai
from typing import List
from app.config import get_settings

settings = get_settings()
genai.configure(api_key=settings.gemini_api_key)


class EmbeddingService:
    """Service for creating embeddings using Google Gemini."""
    
    def __init__(self):
        self.model = settings.gemini_embedding_model
    
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a single text."""
        try:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            raise ValueError(f"Failed to create embedding: {str(e)}")
    
    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts."""
        try:
            embeddings = []
            for text in texts:
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            return embeddings
        except Exception as e:
            raise ValueError(f"Failed to create embeddings: {str(e)}")
