from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.lead import LeadIn, LeadOut
from app.models.lead import Lead
from app.db.session import get_db, Base, engine

router = APIRouter(prefix="/data", tags=["data"])
Base.metadata.create_all(bind=engine)

@router.post("/leads", response_model=LeadOut)
def create_lead(item: LeadIn, db: Session = Depends(get_db)):
    row = Lead(source=item.source, tag=item.tag, payload=item.payload)
    db.add(row); db.commit(); db.refresh(row)
    return row

@router.get("/leads", response_model=List[LeadOut])
def list_leads(source: Optional[str] = None, tag: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Lead)
    if source: q = q.filter(Lead.source == source)
    if tag: q = q.filter(Lead.tag == tag)
    return q.order_by(Lead.id.desc()).limit(100).all()
