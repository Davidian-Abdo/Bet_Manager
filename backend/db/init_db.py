from backend.db.session import engine
from backend.db.base import Base
from backend.models.user import User
from sqlalchemy.orm import Session
from backend.core.security import get_password_hash

def init_db():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Optional: seed admin user
    db = Session(bind=engine)
    if not db.query(User).filter(User.email == "admin@betmanager.com").first():
        admin = User(
            email="admin@betmanager.com",
            hashed_password=get_password_hash("admin123"),
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created: admin@betmanager.com / admin123")
    else:
        print("ℹ️ Admin user already exists.")