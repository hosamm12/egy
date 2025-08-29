from fastapi import APIRouter, Depends, Request, HTTPException
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings
from app.db.session import get_db, Base, engine
from app.models.user import User

router = APIRouter(prefix="/auth/oauth", tags=["oauth"])
settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)

oauth = OAuth()
if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='google',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )
if settings.MICROSOFT_CLIENT_ID and settings.MICROSOFT_CLIENT_SECRET:
    oauth.register(
        name='microsoft',
        client_id=settings.MICROSOFT_CLIENT_ID,
        client_secret=settings.MICROSOFT_CLIENT_SECRET,
        server_metadata_url='https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )

def create_access_token(data: dict, minutes: int | None = None):
    expire = datetime.utcnow() + timedelta(minutes=minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

@router.get("/{provider}/login")
async def oauth_login(provider: str, request: Request):
    if provider not in oauth:
        raise HTTPException(400, "Unsupported provider")
    redirect_uri = f"{settings.OAUTH_REDIRECT_BASE}/api/v1/auth/oauth/{provider}/callback"
    return await oauth[provider].authorize_redirect(request, redirect_uri)

@router.get("/{provider}/callback")
async def oauth_callback(provider: str, request: Request, db: Session = Depends(get_db)):
    if provider not in oauth:
        raise HTTPException(400, "Unsupported provider")
    token = await oauth[provider].authorize_access_token(request)
    userinfo = token.get("userinfo") or {}
    email = userinfo.get("email") or userinfo.get("preferred_username")
    if not email:
        raise HTTPException(400, "Could not read email from provider")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        # create user with random password hash
        user = User(email=email, hashed_password=pwd_context.hash("oauth"), full_name=userinfo.get("name"))
        db.add(user); db.commit(); db.refresh(user)

    jwt_token = create_access_token({"sub": str(user.id)})
    # Redirect to frontend callback with token in URL fragment (safer than query for logs)
    return RedirectResponse(url=f"/oauth-complete#token={jwt_token}")
