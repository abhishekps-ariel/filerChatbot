# FILIR ChatBot - RAG Q&A System

A Python-based chatbot service using **OpenAI GPT-4o-mini** and **pgvector** for Retrieval Augmented Generation (RAG) on petition documents.

## 🏗️ Architecture

- **FastAPI** - RESTful API framework
- **PostgreSQL + pgvector** - Vector database for embeddings
- **OpenAI GPT-4o-mini** - Answer generation
- **OpenAI text-embedding-3-small** - Document embeddings
- **PyPDF** - PDF text extraction

## 📋 Features

- ✅ Upload PDF documents and automatically chunk them
- ✅ Create embeddings and store in pgvector
- ✅ Ask questions about petition documents
- ✅ Retrieve relevant context using similarity search
- ✅ Generate accurate answers with GPT-4o-mini
- ✅ Track source documents and relevance scores

## 🚀 Setup

### Prerequisites

- Python 3.11+
- PostgreSQL with pgvector extension
- OpenAI API key

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd FILIR_ChatBot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```env
   OPENAI_API_KEY=sk-...
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=filir_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   FRONTEND_URL=http://localhost:5173
   ```

5. **Initialize the database:**
   ```bash
   # Connect to PostgreSQL and run:
   psql -U postgres -d filir_db -f init_db.sql
   ```

6. **Run the server:**
   ```bash
   python -m uvicorn app.main:app --reload --port 8001
   ```

7. **Access the API:**
   - API: http://localhost:8001
   - Docs: http://localhost:8001/docs
   - Health: http://localhost:8001/health

## 🐳 Docker Setup

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

This will start both the chatbot service and PostgreSQL with pgvector.

## 📡 API Endpoints

### Upload Document
```bash
POST /ingest/
Content-Type: multipart/form-data

# Upload a PDF file
curl -X POST "http://localhost:8001/ingest/" \
  -F "file=@petition_document.pdf"
```

### Ask Question
```bash
POST /chat/
Content-Type: application/json

{
  "question": "What are the main petition categories?",
  "top_k": 5  // optional, default: 5
}
```

### List Documents
```bash
GET /ingest/documents
```

### Delete Document
```bash
DELETE /ingest/{document_name}
```

### Health Check
```bash
GET /health
```

## 🔄 How It Works

### 1. Document Ingestion
```
PDF Upload → Text Extraction → Text Chunking → Create Embeddings → Store in pgvector
```

### 2. Question Answering (RAG)
```
User Question → Create Embedding → Similarity Search → Retrieve Top Chunks → GPT-4o-mini → Answer
```

## 🛠️ Configuration

Edit `app/config.py` or use environment variables:

- `CHUNK_SIZE` - Text chunk size (default: 1000)
- `CHUNK_OVERLAP` - Overlap between chunks (default: 200)
- `TOP_K_RESULTS` - Number of chunks to retrieve (default: 5)
- `OPENAI_MODEL` - GPT model (default: gpt-4o-mini)
- `OPENAI_EMBEDDING_MODEL` - Embedding model (default: text-embedding-3-small)

## 📊 Database Schema

```sql
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_name VARCHAR(255) NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    embedding vector(1536),  -- OpenAI embeddings
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Testing

```bash
# Test document upload
curl -X POST "http://localhost:8001/ingest/" \
  -F "file=@sample.pdf"

# Test chat
curl -X POST "http://localhost:8001/chat/" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this petition about?"}'
```

## 🔗 Integration with React Frontend

The chatbot widget will be integrated into the Petitions page (`FILIR_UI/src/pages/ViewAllPetitions.tsx`).

API Base URL: `http://localhost:8001`

## 📝 Project Structure

```
FILIR_ChatBot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── services/
│   │   ├── document_processor.py  # PDF processing
│   │   ├── embeddings.py          # OpenAI embeddings
│   │   ├── retrieval.py           # pgvector search
│   │   └── chat.py                # GPT-4o-mini chat
│   └── routers/
│       ├── ingest.py        # Upload endpoints
│       └── chat.py          # Chat endpoints
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── init_db.sql
└── .env.example
```

## 🔐 Security Notes

- Never commit `.env` file
- Use environment variables for secrets
- Restrict CORS origins in production
- Implement rate limiting for production use

## 📞 Support

For issues or questions, contact the development team.
