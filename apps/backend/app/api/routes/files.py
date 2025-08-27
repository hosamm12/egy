from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

@router.get("/sample")
def download_sample():
    """Return a sample text file for download."""
    file_path = Path(__file__).resolve().parent.parent.parent / "static" / "sample.txt"
    return FileResponse(file_path, filename="sample.txt")
