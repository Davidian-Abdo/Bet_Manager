from sqlalchemy.orm import Session
from backend.core.security import hash_password, verify_password
from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt  # make sure you have `python-jose` installed
from backend.core.config import get_settings

def create_user(db: Session, user_data: UserCreate):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def update_user(db: Session, user_id: int, data: UserUpdate):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

settings = get_settings()


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    :param data: Dictionary with payload data (e.g., {"sub": user_id})
    :param expires_delta: Optional timedelta for token expiry
    :return: Encoded JWT token as string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def get_user_by_token(token: str, db: Session):
    """
    Get user from JWT token.
    
    :param token: JWT token string
    :param db: Database session
    :return: User object or None if invalid
    """
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
            
    except jwt.JWTError:
        return None
    
def get_user(db: Session, user_id: int):
    """
    Retrieve a user by ID.
    """
    return db.query(User).filter(User.id == user_id).first()


def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user by ID.
    Returns True if deleted, False if not found.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return Tru