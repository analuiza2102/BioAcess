from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import os
import jwt
from datetime import datetime, timedelta

from app.config import get_db, Base, engine
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# Create a demo user if DB is empty (only for first run / local tests)
from sqlalchemy import select
def _ensure_demo_user(db: Session):
    exists = db.execute(select(User).where(User.username == "ana.luiza")).scalar_one_or_none()
    if not exists:
        pwd = CryptContext(schemes=["bcrypt"], deprecated="auto").hash("admin123")
        db.add(User(username="ana.luiza", password=pwd))
        db.commit()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login_user(body: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user with JSON payload {username, password}. Returns JWT.
    This endpoint is JSON-based to match the current frontend implementation.
    """
    try:
        # bootstrap demo user (safe for dev; remove in prod)
        _ensure_demo_user(db)

        from sqlalchemy import select
        user = db.execute(select(User).where(User.username == body.username)).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        if not pwd_context.verify(body.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha incorreta")

        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        # Log server-side and return a clean message
        print("Erro interno no /auth/login:", repr(e))
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
