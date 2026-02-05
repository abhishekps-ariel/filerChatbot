# 🚀 FILIR ChatBot - Quick Start Guide

## What We Built

✅ **Python FastAPI Service** (FILIR_ChatBot) - RAG-based Q&A system
✅ **React Chatbot Widget** - Integrated into Petitions page
✅ **No LangChain** - Direct OpenAI + pgvector (simple & fast)

---

## 📁 Project Structure

```
FILIR/
├── FILIR_UI/              # React frontend (existing)
│   └── src/components/ChatWidget/  # ← NEW chatbot widget
├── FILIR_XAF/             # .NET backend (existing)
└── FILIR_ChatBot/         # ← NEW Python service
    ├── app/
    │   ├── main.py        # FastAPI app
    │   ├── services/      # RAG logic
    │   └── routers/       # API endpoints
    ├── requirements.txt
    ├── .env.example
    └── README.md
```

---

## 🏃 Getting Started

### Step 1: Set Up Python Service

```powershell
# Navigate to chatbot folder
cd D:\Abhishek-SoftwareTrainee\FILIR\FILIR_ChatBot

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```powershell
# Copy example env file
copy .env.example .env

# Edit .env with your credentials
notepad .env
```

**Required values in `.env`:**
```env
OPENAI_API_KEY=sk-your-key-here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=filir_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
FRONTEND_URL=http://localhost:5173
```

### Step 3: Initialize Database

```powershell
# Connect to PostgreSQL and run:
psql -U postgres -d filir_db -f init_db.sql

# This will:
# - Enable pgvector extension
# - Create document_chunks table
# - Create indexes for fast similarity search
```

### Step 4: Start Python Service

```powershell
# Make sure you're in FILIR_ChatBot folder with venv activated
python -m uvicorn app.main:app --reload --port 8001
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

**Test it:**
- API Docs: http://localhost:8001/docs
- Health Check: http://localhost:8001/health

### Step 5: Start Frontend

```powershell
# In a NEW terminal, navigate to FILIR_UI
cd D:\Abhishek-SoftwareTrainee\FILIR\FILIR_UI

# Install dependencies (if needed)
npm install

# Start frontend
npm run dev
```

---

## 📝 How to Use

### 1. Upload Petition Documents

**Option A: Using API Docs** (http://localhost:8001/docs)
1. Go to `/ingest/` POST endpoint
2. Click "Try it out"
3. Upload a PDF file
4. Click "Execute"

**Option B: Using cURL**
```powershell
curl -X POST "http://localhost:8001/ingest/" -F "file=@petition_document.pdf"
```

### 2. Ask Questions

**Option A: Using the UI**
1. Navigate to Petitions page in your frontend
2. Click the chat widget (purple button, bottom-right)
3. Ask questions about the uploaded documents

**Option B: Using API Docs**
1. Go to `/chat/` POST endpoint
2. Enter your question
3. Get AI-generated answer with sources

**Option C: Using cURL**
```powershell
curl -X POST "http://localhost:8001/chat/" `
  -H "Content-Type: application/json" `
  -d '{\"question\": \"What are the petition categories?\"}'
```

---

## 🔍 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check service status |
| `/ingest/` | POST | Upload PDF document |
| `/ingest/documents` | GET | List all uploaded documents |
| `/ingest/{name}` | DELETE | Delete a document |
| `/chat/` | POST | Ask a question |

---

## 🧪 Testing the RAG System

1. **Upload a test PDF:**
   ```powershell
   # Create a test PDF with petition info first, then:
   curl -X POST "http://localhost:8001/ingest/" -F "file=@test_petition.pdf"
   ```

2. **Ask a question:**
   ```powershell
   curl -X POST "http://localhost:8001/chat/" `
     -H "Content-Type: application/json" `
     -d '{\"question\": \"What is this petition about?\", \"top_k\": 5}'
   ```

3. **Check the response:**
   - `answer`: AI-generated answer
   - `sources`: Relevant chunks with similarity scores
   - `model_used`: gpt-4o-mini

---

## 🐛 Troubleshooting

### Problem: "Database connection failed"
**Solution:**
- Check PostgreSQL is running
- Verify credentials in `.env`
- Make sure `init_db.sql` was executed

### Problem: "OpenAI API error"
**Solution:**
- Check your `OPENAI_API_KEY` in `.env`
- Verify you have credits in your OpenAI account
- Test with: `curl https://api.openai.com/v1/models -H "Authorization: Bearer YOUR_KEY"`

### Problem: "No relevant documents found"
**Solution:**
- Upload documents first using `/ingest/`
- Check uploaded documents: `GET /ingest/documents`

### Problem: "CORS error in frontend"
**Solution:**
- Ensure Python service is running on port 8001
- Check `FRONTEND_URL` in `.env` matches your frontend URL

### Problem: Chat widget not showing
**Solution:**
- Make sure frontend is rebuilt: `npm run dev`
- Check browser console for errors
- Verify Python service is running

---

## 🎯 How RAG Works

```
1. DOCUMENT UPLOAD
   PDF → Extract Text → Split into Chunks → Create Embeddings → Store in pgvector

2. QUESTION ANSWERING
   User Question → Create Embedding → Find Similar Chunks → Send to GPT-4o-mini → Answer
```

### Key Parameters

- **Chunk Size**: 1000 characters (configurable in `config.py`)
- **Chunk Overlap**: 200 characters (prevents context loss)
- **Top K**: 5 chunks retrieved per query
- **Embedding Model**: text-embedding-3-small (1536 dimensions)
- **Chat Model**: GPT-4o-mini

---

## 🐳 Docker Deployment (Optional)

```powershell
# Start both chatbot and PostgreSQL
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 📊 Cost Estimation

**OpenAI Costs** (approximate):
- Embeddings: ~$0.0001 per 1K tokens
- GPT-4o-mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens

**Example**: 100 pages PDF + 1000 questions/month ≈ $5-10/month

---

## 🔐 Production Checklist

Before deploying to production:

- [ ] Change `OPENAI_API_KEY` to production key
- [ ] Update `FRONTEND_URL` to production domain
- [ ] Enable PostgreSQL backups
- [ ] Add rate limiting to API endpoints
- [ ] Set up monitoring and logging
- [ ] Use environment variables (not .env file)
- [ ] Enable HTTPS
- [ ] Restrict CORS origins
- [ ] Add authentication to endpoints

---

## 📞 Support

- **Python Service Docs**: http://localhost:8001/docs
- **Project README**: FILIR_ChatBot/README.md

---

## ✨ Features Summary

✅ PDF document ingestion with automatic chunking
✅ OpenAI embeddings with pgvector storage
✅ Semantic search with similarity scoring
✅ GPT-4o-mini answer generation
✅ Source attribution (shows which documents were used)
✅ Beautiful chat UI on Petitions page
✅ Real-time typing indicators
✅ Error handling and retry logic
✅ Document management (list/delete)
✅ Health checks and monitoring
✅ Docker support
✅ Fully documented API

**No LangChain needed!** Simple, fast, and production-ready.
