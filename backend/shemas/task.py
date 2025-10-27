# backend/schemas/tasks.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    due_date: Optional[datetime]

class TaskCreate(TaskBase):
    assigned_to: int
    project_id: int

class TaskUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]
    due_date: Optional[datetime]
    assigned_to: Optional[int]

class TaskOut(TaskBase):
    id: int
    project_id: int
    assigned_to: int

    class Config:
        orm_mode = True