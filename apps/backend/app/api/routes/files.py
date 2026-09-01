from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.api.deps import get_current_user
from app.core.config import settings
from app.db import models

router = APIRouter()


@router.get("/sample")
async def download_sample(user: models.User = Depends(get_current_user)):
    base = Path(settings.STATIC_DIR).resolve()
    file_path = (base / "sample.txt").resolve()
    if base not in file_path.parents and file_path != base:
        raise HTTPException(status_code=400, detail="Invalid path")
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename="sample.txt")
