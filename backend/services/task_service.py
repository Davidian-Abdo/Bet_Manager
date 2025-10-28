# backend/services/task_service.py
from sqlalchemy.orm import Session
from backend.models.tasks import Task
from backend.schemas.task import TaskCreate, TaskUpdate

def create_task(db: Session, task: TaskCreate):
    db_task = Task(
        name=task.name,
        description=task.description,
        status=task.status,
        due_date=task.due_date,
        assigned_to=task.assigned_to,
        project_id=task.project_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, project_id: int = None):
    query = db.query(Task)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    return query.all()

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    db.delete(task)
    db.commit()
    return task
