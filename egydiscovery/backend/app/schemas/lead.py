from pydantic import BaseModel
from typing import Any, Optional

class LeadIn(BaseModel):
    source: Optional[str] = None
    tag: Optional[str] = None
    payload: dict[str, Any]

class LeadOut(BaseModel):
    id: int
    source: Optional[str] = None
    tag: Optional[str] = None
    payload: dict
    class Config:
        from_attributes = True
