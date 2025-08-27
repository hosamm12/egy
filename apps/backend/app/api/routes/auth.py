from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db import models
from app.core.security import verify_password, get_password_hash, create_access_token
from app.api.deps import get_db, get_current_user

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserOut(BaseModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True

class LoginForm(BaseModel):
    username: EmailStr
    password: str

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(email=user.email, full_name=user.full_name, is_active=user.is_active)

@router.post("/login", response_model=Token)
def login(form_data: LoginForm, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    token = create_access_token(subject=user.email)
    return Token(access_token=token)

@router.get("/me", response_model=UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    return UserOut(email=current_user.email, full_name=current_user.full_name, is_active=current_user.is_active)
