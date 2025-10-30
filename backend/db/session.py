from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from backend.core.config import settings

# ✅ USE THE FIXED TCP CONNECTION STRING FROM SETTINGS
# This uses postgresql+psycopg2:// which forces TCP on Windows
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# ✅ CREATE ENGINE WITH TCP CONNECTION ARGUMENTS
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=NullPool,
    # ✅ FORCE TCP CONNECTION ON WINDOWS
    connect_args={
        'host': settings.DB_HOST,
        'port': settings.DB_PORT,
        'dbname': settings.DB_NAME,
        'user': settings.DB_USER,
        'password': settings.DB_PASSWORD
    }
)

# Session: used in dependencies
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()