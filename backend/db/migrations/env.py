from __future__ import with_statement
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ FORCE LOAD .env FILE FROM PROJECT ROOT
from dotenv import load_dotenv

# Load .env file from PROJECT ROOT
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

print(f"🔧 Loading environment from: {env_path}")
print(f"🔧 File exists: {os.path.exists(env_path)}")

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Now import your models and settings
from db.base import Base
from core.config import settings

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the SQLAlchemy URL (for alembic.ini compatibility)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

print(f"✅ Database URL configured: {settings.DATABASE_URL.replace(settings.DB_PASSWORD, '***')}")

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    from sqlalchemy import create_engine
    import psycopg2
    
    # ✅ NUCLEAR OPTION: Force TCP with explicit connection parameters
    print("🔧 Using nuclear TCP connection...")
    
    # Build connection string that FORCES TCP
    connection_string = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@127.0.0.1:{settings.DB_PORT}/{settings.DB_NAME}"
    
    print(f"🔧 Connection string: {connection_string.replace(settings.DB_PASSWORD, '***')}")
    
    connectable = create_engine(
        connection_string,
        poolclass=pool.NullPool,
        # ✅ EXPLICITLY FORCE TCP CONNECTION
        connect_args={
            'host': '127.0.0.1',  # Explicit IP, not localhost
            'port': settings.DB_PORT,
            'dbname': settings.DB_NAME,
            'user': settings.DB_USER,
            'password': settings.DB_PASSWORD
        }
    )
    
    try:
        with connectable.connect() as connection:
            print("✅ Database connection successful via TCP!")
            
            context.configure(
                connection=connection,
                target_metadata=target_metadata
            )
            
            with context.begin_transaction():
                print("🚀 Running migrations...")
                context.run_migrations()
                print("✅ Migrations completed successfully!")
                
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()