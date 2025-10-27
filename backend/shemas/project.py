# backend/schemas/project.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .user import UserOut


class ProjectBase(BaseModel):
    name: str
    client: str
    description: Optional[str] = None
    budget: Optional[float] = 0.0


class ProjectCreate(ProjectBase):
    start_date: datetime
    end_date: Optional[datetime]


class ProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    budget: Optional[float]
    end_date: Optional[datetime]


class ProjectOut(ProjectBase):
    id: int
    start_date: datetime
    end_date: Optional[datetime]
    progress: float
    members: List[UserOut] = []

    class Config:
        orm_mode = True