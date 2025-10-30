# test_db_connection.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'postgres')
        )
        print("✅ Database connection successful!")
        
        # Check if database exists
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datname = %s", (os.getenv('DB_NAME', 'DAOUDI_DB'),))
        db_exists = cur.fetchone()
        
        if db_exists:
            print(f"✅ Database '{os.getenv('DB_NAME', 'DAOUDI_DB')}' exists")
        else:
            print(f"❌ Database '{os.getenv('DB_NAME', 'DAOUDI_DB')}' doesn't exist")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

test_connection()