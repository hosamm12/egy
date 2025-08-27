from fastapi import APIRouter

router = APIRouter()

# Use explicit "/" path to register a "GET /health" endpoint that also
# plays nicely with FastAPI's automatic trailing‑slash handling.
# When the path was an empty string, requesting "/health/" resulted in a
# 404 even though the intention is to expose a conventional health check
# endpoint at that URL.
@router.get("/")
def read_health():
    return {"status": "ok"}
