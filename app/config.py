from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI / Azure OpenAI
    use_azure: bool = False
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # Azure OpenAI specific (only needed if use_azure=True)
    azure_endpoint: str = ""
    azure_api_version: str = "2024-02-15-preview"
    azure_embedding_deployment: str = ""
    azure_chat_deployment: str = ""
    
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "filir_db"
    postgres_user: str = "postgres"
    postgres_password: str
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    
    # CORS
    frontend_url: str = "http://localhost:5173"
    
    # RAG parameters
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def database_url(self) -> str:
        """Build PostgreSQL connection URL."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
