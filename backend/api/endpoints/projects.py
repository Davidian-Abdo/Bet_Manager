# backend/api/endpoints/projects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from services.project_service import create_project, get_project, get_projects, update_project, delete_project
from api.dependencies import get_db_session

router = APIRouter()

@router.post("/", response_model=ProjectOut)
def api_create_project(project: ProjectCreate, db: Session = Depends(get_db_session)):
    return create_project(db, project)

@router.get("/", response_model=list[ProjectOut])
def api_get_projects(db: Session = Depends(get_db_session)):
    return get_projects(db)

@router.get("/{project_id}", response_model=ProjectOut)
def api_get_project(project_id: int, db: Session = Depends(get_db_session)):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectOut)
def api_update_project(project_id: int, project_data: ProjectUpdate, db: Session = Depends(get_db_session)):
    project = update_project(db, project_id, project_data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", response_model=ProjectOut)
def api_delete_project(project_id: int, db: Session = Depends(get_db_session)):
    project = delete_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project