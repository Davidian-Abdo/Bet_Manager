# backend/models/user.py
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from backend.db.base import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    engineer = "engineer"
    drafter = "drafter"
    manager = "manager"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.engineer)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
