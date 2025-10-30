# backend/models/project.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum, JSON
from sqlalchemy.orm import relationship
from backend.db.base import Base
import enum


class ProjectStatus(str, enum.Enum):
    planned = "planned"
    in_progress = "in_progress"
    completed = "completed"
    delayed = "delayed"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    project_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    client_name = Column(String(200))
    client_contact = Column(String(100))
    budget_total = Column(Float)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.planned)
    start_date = Column(Date)
    end_date = Column(Date)
    phases = Column(JSON, default=list)  # Simplified for now
    team_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    team_lead = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")