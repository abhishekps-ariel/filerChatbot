"""
Setup PostgreSQL database for FILIR ChatBot (WITHOUT pgvector).
This is a simplified version that stores embeddings as JSON arrays.
Performance will be slower but it will work!
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database configuration (from .env)
DB_CONFIG = {
    'host': '54.172.110.96',
    'port': 5432,
    'database': 'localdb',
    'user': 'postgres',
    'password': 'Admin'
}

def setup_database():
    """Set up the database without pgvector extension."""
    print("=" * 60)
    print("FILIR ChatBot - Database Setup (No pgvector)")
    print("=" * 60)
    print()
    print("⚠️  Note: Running without pgvector extension")
    print("   Similarity search will be slower but functional")
    print()
    
    # Connect to database
    print(f"🔌 Connecting to database at {DB_CONFIG['host']}...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("✅ Connected successfully!\n")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return False
    
    # Create document_chunks table (without vector type)
    print("📋 Creating document_chunks table...")
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS document_chunks (
                id SERIAL PRIMARY KEY,
                document_name VARCHAR(255) NOT NULL,
                chunk_text TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                embedding JSONB,
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✅ Table created\n")
    except Exception as e:
        print(f"❌ Failed to create table: {e}")
        return False
    
    # Create indexes
    print("🔍 Creating indexes...")
    try:
        # Index on document_name
        cur.execute("""
            CREATE INDEX IF NOT EXISTS document_chunks_name_idx 
            ON document_chunks(document_name);
        """)
        print("✅ Created document name index\n")
    except Exception as e:
        print(f"⚠️  Warning: Could not create indexes: {e}\n")
    
    # Verify setup
    print("🔍 Verifying setup...")
    try:
        # Check if table exists
        cur.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'document_chunks';
        """)
        table_exists = cur.fetchone()[0] > 0
        
        if table_exists:
            print("✅ Table 'document_chunks' exists")
            
            # Check row count
            cur.execute("SELECT COUNT(*) FROM document_chunks;")
            count = cur.fetchone()[0]
            print(f"   Current documents: {count} chunks")
        else:
            print("❌ Table was not created properly")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not verify: {e}")
    
    # Close connection
    cur.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✨ Database setup complete!")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: Using JSONB for embeddings (slower)")
    print("   For better performance, ask admin to install pgvector")
    print("\nNext steps:")
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("2. Put PDF files in documents/ folder")
    print("3. Start the service:")
    print("   python -m uvicorn app.main:app --reload --port 8001")
    print("4. Run ingestion:")
    print("   python ingest_documents.py")
    
    return True

if __name__ == "__main__":
    try:
        success = setup_database()
        if not success:
            print("\n❌ Setup failed. Please check the errors above.")
            exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled")
        exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)
