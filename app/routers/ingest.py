from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.schemas import IngestResponse
from app.models import DocumentChunk
from app.services.document_processor import DocumentProcessor
from app.services.embeddings import EmbeddingService
from app.config import get_settings

router = APIRouter(prefix="/ingest", tags=["ingest"])
settings = get_settings()


@router.post("/", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process a document (PDF or DOCX).
    
    This endpoint:
    1. Extracts text from the document
    2. Splits text into chunks
    3. Creates embeddings for each chunk
    4. Stores chunks and embeddings in the database
    """
    # Validate file type
    if not (file.filename.lower().endswith('.pdf') or file.filename.lower().endswith('.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Process document
        processor = DocumentProcessor(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        chunks, metadata = processor.process_document(file_content, file.filename)
        
        # Create embeddings
        embedding_service = EmbeddingService()
        embeddings = embedding_service.create_embeddings_batch(chunks)
        
        # Delete existing chunks for this document (if re-uploading)
        db.query(DocumentChunk).filter(
            DocumentChunk.document_name == file.filename
        ).delete()
        
        # Store chunks in database
        for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
            chunk = DocumentChunk(
                document_name=file.filename,
                chunk_text=chunk_text,
                chunk_index=i,
                embedding=embedding,
                doc_metadata=metadata
            )
            db.add(chunk)
        
        db.commit()
        
        return IngestResponse(
            success=True,
            document_name=file.filename,
            chunks_created=len(chunks),
            message=f"Successfully processed {file.filename} into {len(chunks)} chunks"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")


@router.delete("/{document_name}")
async def delete_document(
    document_name: str,
    db: Session = Depends(get_db)
):
    """Delete all chunks for a specific document."""
    deleted = db.query(DocumentChunk).filter(
        DocumentChunk.document_name == document_name
    ).delete()
    
    db.commit()
    
    if deleted == 0:
        raise HTTPException(status_code=404, detail=f"Document '{document_name}' not found")
    
    return {
        "success": True,
        "document_name": document_name,
        "chunks_deleted": deleted,
        "message": f"Successfully deleted {deleted} chunks"
    }


@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    """List all documents in the database."""
    result = db.query(
        DocumentChunk.document_name,
        func.count(DocumentChunk.id).label('chunk_count'),
        func.max(DocumentChunk.created_at).label('last_updated')
    ).group_by(DocumentChunk.document_name).all()
    
    documents = [
        {
            "document_name": row.document_name,
            "chunk_count": row.chunk_count,
            "last_updated": row.last_updated.isoformat() if row.last_updated else None
        }
        for row in result
    ]
    
    return {"documents": documents, "total": len(documents)}
