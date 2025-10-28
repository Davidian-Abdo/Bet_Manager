# backend/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.services.user_service import get_user_by_token
from backend.db.session import SessionLocal

# OAuth2 for auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# DB session dependency
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Current user dependency (updated)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session)
):
    user = get_user_by_token(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )
    return user