from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.config import get_settings
from app.database import init_db, get_db, engine
from app.schemas import HealthResponse
from app.routers import ingest, chat
from sqlalchemy import text

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="FILIR ChatBot API",
    description="RAG-based Q&A chatbot for petition",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingest.router)
app.include_router(chat.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")


@app.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    return {
        "message": "FILIR ChatBot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Health check endpoint."""
    # Check database connection
    db_connected = False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_connected = True
    except Exception:
        pass
    
    # Check Gemini configuration
    gemini_configured = bool(settings.gemini_api_key and settings.gemini_api_key != "your-gemini-api-key-here")
    
    return HealthResponse(
        status="healthy" if (db_connected and gemini_configured) else "degraded",
        timestamp=datetime.now(),
        database_connected=db_connected,
        gemini_configured=gemini_configured
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
