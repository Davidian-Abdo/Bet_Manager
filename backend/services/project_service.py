# backend/services/project_service.py
from sqlalchemy.orm import Session
from backend.models.project import Project
from backend.schemas.project import ProjectCreate, ProjectUpdate
from fastapi import HTTPException
from datetime import datetime


def create_project(db: Session, project_data: ProjectCreate):
    project = Project(
        name=project_data.name,
        client=project_data.client,
        description=project_data.description,
        start_date=project_data.start_date,
        end_date=project_data.end_date,
        budget=project_data.budget
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_project(db: Session, project_id: int):
    """
    Retrieve a single project by ID.
    """
    return db.query(Project).filter(Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of projects with optional pagination.
    """
    return db.query(Project).offset(skip).limit(limit).all()

def update_project(db: Session, project_id: int, data: ProjectUpdate):
    project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projet introuvable")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(project, k, v)
    db.commit()
    db.refresh(project)
    return project


def calculate_progress(db: Session, project_id: int):
    # Example logic: % of tasks done
    project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projet introuvable")

    total_tasks = len(project.tasks)
    done_tasks = len([t for t in project.tasks if t.status == "done"])
    project.progress = (done_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    db.commit()
    db.refresh(project)
    return project.progress

def delete_project(db: Session, project_id: int) -> bool:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return False
    db.delete(project)
    db.commit()
    return True