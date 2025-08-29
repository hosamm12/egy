from sqlalchemy import Column, Integer, String, DateTime, func, JSON
from app.db.session import Base

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), index=True, nullable=True)
    tag = Column(String(100), index=True, nullable=True)
    payload = Column(JSON, nullable=False, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
