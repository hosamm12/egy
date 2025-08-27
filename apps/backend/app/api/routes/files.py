from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from app.core.config import settings

router = APIRouter()


@router.get("/sample")
async def download_sample():
    """Return a sample text file for download."""
    file_path = Path(settings.STATIC_DIR) / "sample.txt"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename="sample.txt")
