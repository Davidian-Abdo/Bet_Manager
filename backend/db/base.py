# backend/db/base.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all your models here so Alembic can detect them