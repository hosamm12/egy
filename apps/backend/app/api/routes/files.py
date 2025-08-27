from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()


@router.get("/sample", response_class=FileResponse)
async def download_sample():
    """Return a sample text file for download."""
    file_path = Path(__file__).resolve().parent.parent.parent / "static" / "sample.txt"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename="sample.txt")
