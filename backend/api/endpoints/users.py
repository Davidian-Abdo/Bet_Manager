# backend/api/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.user import UserCreate, UserOut, UserUpdate
from backend.services.user_service import create_user, get_user, update_user, delete_user
from backend.api.dependencies import get_db_session

router = APIRouter()

@router.post("/", response_model=UserOut)
def api_create_user(user: UserCreate, db: Session = Depends(get_db_session)):
    return create_user(db, user)

@router.get("/{user_id}", response_model=UserOut)
def api_get_user(user_id: int, db: Session = Depends(get_db_session)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
def api_update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db_session)):
    user = update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", response_model=UserOut)
def api_delete_user(user_id: int, db: Session = Depends(get_db_session)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user