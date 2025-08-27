import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.db.models import User
from app.core.security import get_password_hash

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def seed():
    from app.db.session import Base
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    try:
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(email="admin@example.com", full_name="Admin", hashed_password=get_password_hash("admin123"))
            db.add(admin)
            db.commit()
        print("Seed complete.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
