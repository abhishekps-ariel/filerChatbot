"""
Script to clear all documents from the database.
Run this before ingesting new documents.
"""
from sqlalchemy import text
from app.database import engine

def clear_all_documents():
    """Delete all document chunks from database."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("DELETE FROM document_chunks"))
            conn.commit()
            print(f"✅ Cleared {result.rowcount} document chunks from database")
            print("You can now add new documents using ingest_documents.py")
    except Exception as e:
        print(f"❌ Error clearing documents: {e}")

if __name__ == "__main__":
    print("⚠️  This will delete ALL documents from the database!")
    confirm = input("Are you sure? (yes/no): ")
    
    if confirm.lower() == 'yes':
        clear_all_documents()
    else:
        print("Cancelled")
