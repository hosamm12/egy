import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, validate_password_strength
from app.db.models import User
from app.db.session import Base

DATABASE_URL = os.environ.get("DATABASE_URL")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


def seed() -> None:
    if not DATABASE_URL:
        raise SystemExit("DATABASE_URL is required")
    if not ADMIN_PASSWORD:
        raise SystemExit("ADMIN_PASSWORD is required; do not use a hardcoded default")
    try:
        validate_password_strength(ADMIN_PASSWORD)
    except ValueError as exc:
        raise SystemExit(str(exc))

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    try:
        admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if not admin:
            admin = User(
                email=ADMIN_EMAIL,
                full_name="Admin",
                hashed_password=get_password_hash(ADMIN_PASSWORD),
                role="admin",
            )
            db.add(admin)
            db.commit()
        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    sys.exit(0)
