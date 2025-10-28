# backend/db/base.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all your models here so Alembic can detect them
from backend.models.user import User
from backend.models.project import Project
from backend.models.document import Document
from backend.models.activity_log import ActivityLog