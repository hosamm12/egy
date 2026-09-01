import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.files import router as files_router
from app.api.routes.health import router as health_router
from app.core.config import settings
from app.db.session import init_db

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("egysaas")

app = FastAPI(title="EgySaaS Backend", version="1.0.0")

origins = [str(o).rstrip("/") for o in settings.BACKEND_CORS_ORIGINS]
origins = [o for o in origins if 'localhost' not in o and '127.0.0.1' not in o]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\\.vercel\\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        try:
            response = await call_next(request)
        except Exception:
            log.exception("unhandled_error request_id=%s path=%s", request_id, request.url.path)
            return JSONResponse(
                status_code=500,
                content={"error": {"code": "internal_error", "message": "Unexpected error", "request_id": request_id}},
            )
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response


app.add_middleware(RequestContextMiddleware)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(health_router, prefix="/api/v1/health", tags=["health"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(files_router, prefix="/files", tags=["files"])
app.include_router(files_router, prefix="/api/v1/files", tags=["files"])


@app.on_event("startup")
def on_startup():
    init_db()
