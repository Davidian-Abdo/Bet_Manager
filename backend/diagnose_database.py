import os
import sys
from dotenv import load_dotenv

# ✅ CORRECT PATH - .env is next to backend folder
current_dir = os.path.dirname(os.path.abspath(__file__))  # backend folder
project_root = os.path.dirname(current_dir)  # Bet_Manager folder
env_path = os.path.join(project_root, '.env')

print(f"🔧 Looking for .env at: {env_path}")
print(f"🔧 File exists: {os.path.exists(env_path)}")

if os.path.exists(env_path):
    load_dotenv(env_path)
    print("✅ .env file loaded successfully!")
else:
    print("❌ .env file not found!")
    sys.exit(1)

# Debug: Show loaded environment variables
print("\n🔧 Environment variables loaded:")
env_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
for key in env_vars:
    value = os.getenv(key)
    if value:
        masked_value = '***' if key == 'DB_PASSWORD' else value
        print(f"  - {key}: {masked_value}")
    else:
        print(f"  - {key}: ❌ NOT FOUND")

# Check if we have the minimum required variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    print("\n❌ MISSING REQUIRED ENVIRONMENT VARIABLES!")
    print("Please check your .env file exists and contains:")
    print("DB_USER=your_username")
    print("DB_PASSWORD=your_password") 
    print("DB_NAME=DAOUDI_DB")
    sys.exit(1)

# Now proceed with database connection
from sqlalchemy import create_engine, text

def diagnose_database():
    print("\n🔍 COMPREHENSIVE DATABASE DIAGNOSIS")
    print("=" * 50)
    
    # Build connection string
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"🔧 Using connection: {connection_string.replace(DB_PASSWORD, '***')}")
    
    # ✅ APPLY THE NUCLEAR TCP FIX (same as in env.py)
    engine = create_engine(
        connection_string,
        # ✅ FORCE TCP CONNECTION
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
            print("✅ Database connection successful via TCP!")
            
            # 1. Check current database
            result = conn.execute(text("SELECT current_database();"))
            current_db = result.scalar()
            print(f"📊 Connected to database: {current_db}")
            
            # 2. Check all schemas
            print(f"\n📋 ALL SCHEMAS IN DATABASE:")
            result = conn.execute(text("SELECT schema_name FROM information_schema.schemata;"))
            schemas = [row[0] for row in result]
            for schema in schemas:
                print(f"  - {schema}")
            
            # 3. Check ALL tables in ALL schemas
            print(f"\n📋 ALL TABLES IN ALL SCHEMAS:")
            result = conn.execute(text("""
                SELECT table_schema, table_name 
                FROM information_schema.tables 
                WHERE table_type = 'BASE TABLE'
                ORDER BY table_schema, table_name;
            """))
            tables_found = False
            for schema, table in result:
                print(f"  - {schema}.{table}")
                tables_found = True
            
            if not tables_found:
                print("  ❌ NO TABLES FOUND IN ANY SCHEMA!")
            
            # 4. Check alembic_version table specifically
            print(f"\n🔍 CHECKING FOR ALEMBIC_VERSION TABLE:")
            result = conn.execute(text("""
                SELECT table_schema, table_name 
                FROM information_schema.tables 
                WHERE table_name = 'alembic_version';
            """))
            alembic_tables = list(result)
            if alembic_tables:
                for schema, table in alembic_tables:
                    print(f"  ✅ Found: {schema}.{table}")
                    
                    # Check what version is recorded
                    version_result = conn.execute(text(f'SELECT version_num FROM "{schema}"."{table}";'))
                    version = version_result.scalar()
                    print(f"  📝 Current migration version: {version}")
            else:
                print("  ❌ alembic_version table NOT found!")
                
            # 5. Check public schema specifically for your tables
            print(f"\n🎯 CHECKING PUBLIC SCHEMA FOR YOUR TABLES:")
            your_tables = ['users', 'projects', 'documents', 'activity_logs']
            for table in your_tables:
                result = conn.execute(text(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = '{table}'
                    );
                """))
                exists = result.scalar()
                if exists:
                    print(f"  ✅ {table} - FOUND in public schema")
                else:
                    print(f"  ❌ {table} - NOT FOUND in public schema")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_database()