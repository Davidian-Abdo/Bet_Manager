# backend/api/endpoints/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.services.task_service import create_task, get_tasks, get_task, update_task, delete_task
from backend.schemas.task import TaskCreate, TaskUpdate, TaskOut
from backend.api.dependencies import get_db_session

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskOut)
def api_create_task(task: TaskCreate, db: Session = Depends(get_db_session)):
    return create_task(db, task)

@router.get("/", response_model=list[TaskOut])
def api_get_tasks(project_id: int = None, db: Session = Depends(get_db_session)):
    return get_tasks(db, project_id)

@router.get("/{task_id}", response_model=TaskOut)
def api_get_task(task_id: int, db: Session = Depends(get_db_session)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskOut)
def api_update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db_session)):
    task = update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", response_model=TaskOut)
def api_delete_task(task_id: int, db: Session = Depends(get_db_session)):
    task = delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return tas