"""
Test script to verify the FILIR ChatBot setup.
Run this after starting the service to ensure everything works.
"""

import requests
import sys

API_BASE_URL = "http://localhost:8001"

def test_health():
    """Test health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service is {data['status']}")
            print(f"   Database: {'✅ Connected' if data['database_connected'] else '❌ Not connected'}")
            print(f"   OpenAI: {'✅ Configured' if data['openai_configured'] else '❌ Not configured'}")
            return data['database_connected'] and data['openai_configured']
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to service: {e}")
        print("   Make sure the service is running: python -m uvicorn app.main:app --reload --port 8001")
        return False

def test_documents_list():
    """Test document listing."""
    print("\n📄 Testing document listing...")
    try:
        response = requests.get(f"{API_BASE_URL}/ingest/documents")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total']} documents")
            for doc in data['documents']:
                print(f"   - {doc['document_name']}: {doc['chunk_count']} chunks")
            return True
        else:
            print(f"❌ Failed to list documents: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat():
    """Test chat endpoint with a simple question."""
    print("\n💬 Testing chat endpoint...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat/",
            json={"question": "Hello, can you help me?", "top_k": 5}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat working! Model: {data['model_used']}")
            print(f"   Answer: {data['answer'][:100]}...")
            print(f"   Sources: {len(data['sources'])} chunks retrieved")
            return True
        elif response.status_code == 404:
            print("⚠️  No documents uploaded yet")
            print("   Upload a PDF first: POST /ingest/")
            return True  # This is expected if no documents
        else:
            print(f"❌ Chat failed: {response.status_code}")
            print(f"   {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("FILIR ChatBot Service Test")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("\n❌ Service is not healthy. Please check configuration.")
        sys.exit(1)
    
    # Test documents
    test_documents_list()
    
    # Test chat
    test_chat()
    
    print("\n" + "=" * 60)
    print("✨ All tests completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Upload a PDF: curl -X POST http://localhost:8001/ingest/ -F 'file=@your.pdf'")
    print("2. Open frontend: http://localhost:5173")
    print("3. Go to Petitions page and click the chat widget")
    print("4. API Docs: http://localhost:8001/docs")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted")
        sys.exit(0)
