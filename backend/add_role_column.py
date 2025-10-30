import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

# Load environment
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

def add_role_column():
    print("🔧 Adding role column to users table...")
    
    # Build connection string manually with TCP
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')  # Use IP for TCP
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME')
    
    # ✅ USE TCP CONNECTION STRING
    connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"🔗 Using TCP connection: {connection_string.replace(DB_PASSWORD, '***')}")
    
    # ✅ CREATE ENGINE WITH TCP CONFIGURATION
    engine = create_engine(
        connection_string,
        poolclass=NullPool,
        connect_args={
            'host': DB_HOST,
            'port': DB_PORT,
            'dbname': DB_NAME,
            'user': DB_USER,
            'password': DB_PASSWORD
        }
    )
    
    try:
        with engine.connect() as conn:
            print("✅ Database connection successful!")
            
            # Check if role column already exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'role';
            """))
            
            if result.fetchone():
                print("✅ Role column already exists!")
                return True
            
            # Add role column
            print("➕ Adding role column...")
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN role VARCHAR NOT NULL DEFAULT 'engineer';
            """))
            conn.commit()
            print("✅ Role column added successfully!")
            print("   - Default value: 'engineer'")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    add_role_column()