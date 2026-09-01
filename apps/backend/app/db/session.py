from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

connect_args = {}
engine_kwargs = {"pool_pre_ping": True}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    if ":memory:" in settings.DATABASE_URL:
        engine_kwargs = {"poolclass": StaticPool, "connect_args": connect_args}
    else:
        engine_kwargs = {"connect_args": connect_args}
else:
    engine_kwargs.update(pool_size=settings.DB_POOL_SIZE, max_overflow=settings.DB_MAX_OVERFLOW)

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db() -> None:
    from app.db import models  # noqa: F401

    if not settings.is_production:
        Base.metadata.create_all(bind=engine)
