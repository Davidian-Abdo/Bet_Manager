# backend/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from services.user_service import get_user_by_token
from db.session import SessionLocal

# OAuth2 for auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# DB session dependency
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Current user dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user