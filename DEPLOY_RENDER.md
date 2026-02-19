# Deploy FILIR ChatBot on Render

Quick guide to deploy your chatbot on Render.

## Step 1: Connect Your Repository

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your Git repository (GitHub/GitLab/Bitbucket)
4. Select the `FILIR_ChatBot` repository

## Step 2: Configure the Service

### Basic Settings:
- **Name:** `filir-chatbot` (or any name you want)
- **Region:** Choose closest to your users
- **Branch:** `main` (or your default branch)
- **Root Directory:** Leave empty (or `FILIR_ChatBot` if repo is in subfolder)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Environment Variables:
Click **"Advanced"** → **"Add Environment Variable"** and add these:

**Required:**
```
OPENAI_API_KEY=sk-your-openai-key-here
POSTGRES_HOST=your-postgres-host.render.com
POSTGRES_PORT=5432
POSTGRES_DB=your-database-name
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
FRONTEND_URL=https://your-frontend-url.com
```

**Optional (with defaults):**
```
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
API_HOST=0.0.0.0
```

## Step 3: Create PostgreSQL Database (if needed)

If you don't have a database yet:

1. In Render Dashboard → **"New +"** → **"PostgreSQL"**
2. Choose plan (Free tier available)
3. Copy the connection details:
   - **Host:** `xxx.render.com`
   - **Port:** `5432`
   - **Database:** `xxx`
   - **User:** `xxx`
   - **Password:** `xxx`
4. Use these in your Web Service environment variables

## Step 4: Initialize Database

After deployment, connect to your database and run:

```sql
-- Enable pgvector extension (if using PostgreSQL on Render)
CREATE EXTENSION IF NOT EXISTS vector;

-- The table will be created automatically by SQLAlchemy on first startup
-- But if you want to create it manually, use init_db.sql
```

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repo
   - Install dependencies
   - Start your service
3. Wait for deployment to complete (2-3 minutes)

## Step 6: Test

Once deployed, you'll get a URL like:
```
https://filir-chatbot.onrender.com
```

Test endpoints:
- Health: `https://filir-chatbot.onrender.com/health`
- API Docs: `https://filir-chatbot.onrender.com/docs`

## Troubleshooting

### Build Fails:
- Check build logs in Render dashboard
- Make sure `requirements.txt` is correct
- Verify Python version compatibility

### Service Won't Start:
- Check logs in Render dashboard
- Verify all environment variables are set
- Make sure database is accessible from Render

### Database Connection Error:
- Verify PostgreSQL is running
- Check firewall rules (Render PostgreSQL should allow Render services)
- Double-check credentials in environment variables

### CORS Errors:
- Update `FRONTEND_URL` environment variable to your actual frontend URL
- Make sure it includes protocol (`https://`)

## Notes

- **Free tier:** Services spin down after 15 minutes of inactivity (first request will be slow)
- **Upgrade:** For always-on service, upgrade to paid plan
- **Logs:** View real-time logs in Render dashboard
- **Environment:** All secrets are encrypted in Render

## Quick Deploy Checklist

- [ ] Repository connected to Render
- [ ] Web Service created
- [ ] Environment variables set (all required ones)
- [ ] PostgreSQL database created (if needed)
- [ ] Database initialized (pgvector extension)
- [ ] Service deployed successfully
- [ ] Health endpoint tested
- [ ] Frontend URL updated in CORS settings

---

**That's it! Your chatbot is now live on Render! 🚀**

