from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.db.session import init_db

app = FastAPI(title="EgySaaS Backend")

# CORS
origins = []
try:
    from app.core.config import settings
    origins = settings.BACKEND_CORS_ORIGINS
except Exception:
    origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.on_event("startup")
def on_startup():
    init_db()
