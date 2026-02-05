from openai import OpenAI, AzureOpenAI
from typing import List
from app.config import get_settings

settings = get_settings()


class EmbeddingService:
    """Service for creating embeddings using OpenAI or Azure OpenAI."""
    
    def __init__(self):
        if settings.use_azure:
            self.client = AzureOpenAI(
                api_key=settings.openai_api_key,
                azure_endpoint=settings.azure_endpoint,
                api_version=settings.azure_api_version
            )
            self.model = settings.azure_embedding_deployment
        else:
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_embedding_model
    
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a single text."""
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            raise ValueError(f"Failed to create embedding: {str(e)}")
    
    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts."""
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            raise ValueError(f"Failed to create embeddings: {str(e)}")
