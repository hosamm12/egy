
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.lead import Lead

def persist_leads(db: Session, source: str, tag: str, items: list):
    for it in items:
        row = Lead(source=source, tag=tag, payload=it)
        db.add(row)
    db.commit()

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
from app.services.security import get_current_user

try:
    from app.agents.master_controller import MasterController  # type: ignore
except Exception:
    MasterController = None
from app.agents import router as router_agent

router = APIRouter(prefix="/agents", tags=["agents"])

class RunPayload(BaseModel):
    prompt: str
    params: Dict[str, Any] | None = None

@router.post("/master")
def run_master(payload: RunPayload, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    if MasterController:
        try:
            ctl = MasterController()
            res = ctl.run(payload.prompt, payload.params or {})
            items = res.get('items') if isinstance(res, dict) else None
            if items: persist_leads(db, 'master', 'auto', items)
            return {"ok": True, "result": res, "user": user_id}
        except Exception as e:
            raise HTTPException(500, f"MasterController error: {e}")
    res = router_agent.run(payload.prompt, payload.params or {})
    items = res.get('items') if isinstance(res, dict) else None
    if items: persist_leads(db, 'router', 'auto', items)
    return {"ok": True, "result": res, "user": user_id}

@router.post("/route")
def run_route(payload: RunPayload, user_id: str = Depends(get_current_user)):
    res = router_agent.run(payload.prompt, payload.params or {})
    items = res.get('items') if isinstance(res, dict) else None
    if items: persist_leads(db, 'router', 'auto', items)
    return {"ok": True, "result": res, "user": user_id}
