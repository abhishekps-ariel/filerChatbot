from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChatRequest, ChatResponse, SourceChunk
from app.services.retrieval import RetrievalService
from app.services.chat import ChatService
from app.config import get_settings

router = APIRouter(prefix="/chat", tags=["chat"])
settings = get_settings()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Answer a question using RAG (Retrieval Augmented Generation).
    
    This endpoint:
    1. Creates an embedding for the user's question
    2. Searches for similar chunks in the database
    3. Uses GPT-4o-mini to generate an answer based on retrieved chunks
    """
    try:
        # Retrieve relevant chunks
        retrieval_service = RetrievalService()
        chunks_with_scores = retrieval_service.similarity_search(
            db=db,
            query=request.question,
            top_k=request.top_k or settings.top_k_results,
            document_name=request.document_name
        )
        
        if not chunks_with_scores:
            raise HTTPException(
                status_code=404,
                detail="No relevant documents found. Please upload petition documents first."
            )
        
        # Generate answer
        chat_service = ChatService()
        answer = chat_service.generate_answer(request.question, chunks_with_scores)
        
        # Format sources
        sources = [
            SourceChunk(
                chunk_text=chunk.chunk_text[:200] + "..." if len(chunk.chunk_text) > 200 else chunk.chunk_text,
                document_name=chunk.document_name,
                chunk_index=chunk.chunk_index,
                similarity_score=round(score, 4)
            )
            for chunk, score in chunks_with_scores
        ]
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            gemini_model=settings.gemini_model
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")
