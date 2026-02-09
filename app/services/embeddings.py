from openai import OpenAI
from typing import List
from app.config import get_settings

settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)


class EmbeddingService:
    """Service for creating embeddings using OpenAI."""
    
    def __init__(self):
        self.model = settings.openai_embedding_model
    
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a single text."""
        try:
            response = client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise ValueError(f"Failed to create embedding: {str(e)}")
    
    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts."""
        try:
            response = client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            raise ValueError(f"Failed to create embeddings: {str(e)}")
