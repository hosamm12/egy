from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, Any, Dict
import os, requests
from app.services.security import get_current_user

router = APIRouter(prefix="/events", tags=["events"])

WEBHOOK_BASE = os.getenv("WEBHOOK_URL", "http://n8n:5678")

class LeadForm(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    message: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = "form"
    tag: Optional[str] = "site"
    score: Optional[int] = None
    extra: Dict[str, Any] = {}

@router.post("/lead")
def event_lead(payload: LeadForm):
    try:
        r = requests.post(f"{WEBHOOK_BASE}/webhook/lead_ingest", json=payload.dict())
        return {"ok": True, "status": r.status_code, "n8n": r.json() if r.headers.get("content-type","").startswith("application/json") else r.text}
    except Exception as e:
        raise HTTPException(500, f"n8n error: {e}")

class ChatEvent(BaseModel):
    session_id: str
    event_type: str  # e.g., 'start', 'message'
    text: Optional[str] = ""
    channel: Optional[str] = "web"
    meta: Dict[str, Any] = {}

@router.post("/chat")
def event_chat(payload: ChatEvent, user_id: str = Depends(get_current_user)):
    try:
        data = payload.dict() | {"user_id": user_id}
        r = requests.post(f"{WEBHOOK_BASE}/webhook/chat_event", json=data)
        return {"ok": True, "status": r.status_code}
    except Exception as e:
        raise HTTPException(500, f"n8n error: {e}")
