"""
Bulk ingest all PDF documents from the documents/ folder.
This script is for admins to upload petition documents to the chatbot system.
Users will only ask questions, not upload files.
"""

import os
import sys
import requests
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8001"
DOCUMENTS_FOLDER = "documents"

def ingest_document(file_path: Path):
    """Upload a single document to the chatbot."""
    print(f"📄 Processing: {file_path.name}...")
    
    try:
        # Determine content type based on file extension
        ext = file_path.suffix.lower()
        content_type_map = {
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.md': 'text/markdown',
            '.json': 'application/json'
        }
        content_type = content_type_map.get(ext, 'application/octet-stream')
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, content_type)}
            response = requests.post(f"{API_BASE_URL}/ingest/", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Created {data['chunks_created']} chunks")
            return True
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Ingest all PDFs from documents folder."""
    print("=" * 60)
    print("FILIR Chatbot - Document Ingestion Tool")
    print("=" * 60)
    print()
    
    # Check if service is running
    print("🔍 Checking if chatbot service is running...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Service is not healthy!")
            print("   Make sure the service is running:")
            print("   python -m uvicorn app.main:app --reload --port 8001")
            sys.exit(1)
        print("✅ Service is running\n")
    except Exception as e:
        print(f"❌ Cannot connect to service: {e}")
        print("   Make sure the service is running:")
        print("   python -m uvicorn app.main:app --reload --port 8001")
        sys.exit(1)
    
    # Find all supported document files
    docs_folder = Path(DOCUMENTS_FOLDER)
    if not docs_folder.exists():
        print(f"❌ Folder '{DOCUMENTS_FOLDER}' not found!")
        print(f"   Create it and add document files there.")
        sys.exit(1)
    
    pdf_files = list(docs_folder.glob("*.pdf"))
    docx_files = list(docs_folder.glob("*.docx"))
    md_files = list(docs_folder.glob("*.md"))
    json_files = list(docs_folder.glob("*.json"))
    all_files = pdf_files + docx_files + md_files + json_files
    
    if not all_files:
        print(f"⚠️  No document files found in '{DOCUMENTS_FOLDER}' folder")
        print(f"   Add your documents (PDF, DOCX, MD, JSON) there and run this script again.")
        sys.exit(0)
    
    print(f"📚 Found {len(all_files)} document(s):")
    print(f"   PDF: {len(pdf_files)}, DOCX: {len(docx_files)}, MD: {len(md_files)}, JSON: {len(json_files)}\n")
    
    # Ingest each file
    success_count = 0
    failed_count = 0
    
    for pdf_file in all_files:
        if ingest_document(pdf_file):
            success_count += 1
        else:
            failed_count += 1
        print()
    
    # Summary
    print("=" * 60)
    print("Summary:")
    print(f"  ✅ Successfully ingested: {success_count}")
    print(f"  ❌ Failed: {failed_count}")
    print("=" * 60)
    
    if success_count > 0:
        print("\n✨ Documents are now ready for Q&A!")
        print("   Users can ask questions via the chatbot widget.")
    
    # List all documents in database
    print("\n📋 Listing all documents in database...")
    try:
        response = requests.get(f"{API_BASE_URL}/ingest/documents")
        if response.status_code == 200:
            data = response.json()
            print(f"\nTotal documents in database: {data['total']}")
            for doc in data['documents']:
                print(f"  • {doc['document_name']}: {doc['chunk_count']} chunks")
    except Exception as e:
        print(f"⚠️  Could not list documents: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Ingestion cancelled")
        sys.exit(0)
