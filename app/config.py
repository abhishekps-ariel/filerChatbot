from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "filir_db"
    postgres_user: str = "postgres"
    postgres_password: str
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    
    # CORS - can be comma-separated list of URLs
    frontend_url: str = "http://localhost:5173"
    
    @property
    def allowed_origins(self) -> list[str]:
        """Parse frontend_url into list of allowed origins."""
        origins = []
        # Split by comma and strip whitespace
        for url in self.frontend_url.split(","):
            url = url.strip()
            if url:
                origins.append(url)
        # Always include localhost URLs for development
        localhost_urls = ["http://localhost:5173", "http://localhost:3000"]
        for url in localhost_urls:
            if url not in origins:
                origins.append(url)
        return origins
    
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
