# backend/models/user.py
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from backend.db.base import Base
from sqlalchemy.orm import relationship
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    engineer = "engineer"
    drafter = "drafter"
    manager = "manager"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.engineer)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    projects = relationship("Project", back_populates="team_lead")
    tasks = relationship("Task", back_populates="user")