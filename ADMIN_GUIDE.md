# Admin Quick Start - FILIR ChatBot

## Setup (One-time)

### 1. Initialize Database
Your PostgreSQL is already running at `54.172.110.96`. Just add the pgvector extension:

```powershell
# Connect to your database
psql -h 54.172.110.96 -U postgres -d localdb

# In PostgreSQL prompt, run:
CREATE EXTENSION IF NOT EXISTS vector;

# Create the table
\i init_db.sql

# Verify
\dt document_chunks

# Exit
\q
```

### 2. Install Python Dependencies
```powershell
cd D:\Abhishek-SoftwareTrainee\FILIR\FILIR_UI\FILIR_ChatBot

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
The `.env` file is already configured with your database:
- ✅ Database: `54.172.110.96:5432/localdb`
- ✅ OpenAI API Key: Already set
- ✅ Frontend URL: `http://localhost:5173`

---

## Daily Workflow

### Start the ChatBot Service

```powershell
# Navigate to chatbot folder
cd D:\Abhishek-SoftwareTrainee\FILIR\FILIR_UI\FILIR_ChatBot

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start service
python -m uvicorn app.main:app --reload --port 8001
```

**Service is running when you see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001
Database initialized successfully!
```

**Access:**
- API Docs: http://localhost:8001/docs
- Health Check: http://localhost:8001/health

---

## Managing Documents (Admin Only)

Users **do NOT upload files**. Only admins manage the knowledge base.

### Add Petition Documents

1. **Place PDF files in `documents/` folder:**
   ```
   FILIR_ChatBot/
   └── documents/
       ├── petition_guidelines.pdf
       ├── petition_categories.pdf
       └── petition_faq.pdf
   ```

2. **Run ingestion script:**
   ```powershell
   # Make sure service is running first!
   python ingest_documents.py
   ```

   This will:
   - Process all PDFs in `documents/` folder
   - Extract text and create chunks
   - Generate embeddings
   - Store in database

### View Uploaded Documents

```powershell
# List all documents
curl http://localhost:8001/ingest/documents
```

Or visit: http://localhost:8001/docs → `/ingest/documents` endpoint

### Remove a Document

```powershell
# Delete a specific document
curl -X DELETE http://localhost:8001/ingest/petition_guidelines.pdf
```

Or use API docs: http://localhost:8001/docs → `/ingest/{document_name}` DELETE

---

## User Experience

Users will:
1. Go to **Petitions page** in the frontend
2. See a **purple chat button** (bottom-right)
3. Click it and **ask questions**
4. Get **AI-powered answers** based on your uploaded documents

Users **cannot** upload documents - they only ask questions!

---

## Testing

### 1. Test the Service
```powershell
python test_service.py
```

### 2. Test with a Question
```powershell
curl -X POST http://localhost:8001/chat/ `
  -H "Content-Type: application/json" `
  -d '{\"question\": \"What are the petition categories?\"}'
```

### 3. Test in Frontend
1. Start frontend: `npm run dev` (in FILIR_UI folder)
2. Go to Petitions page
3. Click chat button
4. Ask a question

---

## Folder Structure

```
FILIR_ChatBot/
├── documents/              ← PUT PDFs HERE (admin only)
│   ├── petition_guidelines.pdf
│   └── ...
├── app/                    ← Application code
├── venv/                   ← Python virtual environment
├── .env                    ← Configuration (already set up)
├── ingest_documents.py     ← Run this to process PDFs
└── test_service.py         ← Run this to test
```

---

## Troubleshooting

### Service won't start
- Check if port 8001 is already in use
- Verify `.env` file exists and has correct values
- Make sure virtual environment is activated

### Documents not ingesting
- Ensure service is running first
- Check PDFs are in `documents/` folder
- Verify database connection: http://localhost:8001/health

### Chat widget not appearing
- Make sure Python service is running
- Check browser console for errors
- Verify frontend is running

### Database errors
- Confirm pgvector extension is installed:
  ```sql
  SELECT * FROM pg_extension WHERE extname = 'vector';
  ```
- Check connection to `54.172.110.96:5432`

---

## Production Deployment

When deploying to production:

1. **Environment Variables:**
   - Set `OPENAI_API_KEY` as environment variable
   - Update `POSTGRES_HOST`, `POSTGRES_PASSWORD`
   - Set `FRONTEND_URL` to production URL

2. **Run as Service:**
   - Use a process manager (PM2, systemd, Windows Service)
   - Or use Docker: `docker-compose up -d`

3. **Security:**
   - Add authentication to admin endpoints
   - Enable HTTPS
   - Restrict CORS origins

---

## Quick Commands Reference

```powershell
# Start service
cd D:\Abhishek-SoftwareTrainee\FILIR\FILIR_UI\FILIR_ChatBot
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8001

# Ingest documents
python ingest_documents.py

# Test service
python test_service.py

# View health
curl http://localhost:8001/health

# List documents
curl http://localhost:8001/ingest/documents

# Delete document
curl -X DELETE http://localhost:8001/ingest/filename.pdf
```

---

**Questions?** Check the logs in the terminal where the service is running!
