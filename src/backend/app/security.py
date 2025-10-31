"""Segurança: JWT, autenticação e controle de acesso"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .config import settings
from .db import get_db
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria token JWT para autenticação"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_EXPIRATION_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def hash_password(password: str) -> str:
    """Gera hash da senha usando bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se senha corresponde ao hash"""
    return pwd_context.verify(plain_password, hashed_password)


def verify_token(token: str) -> dict:
    """Verifica e decodifica token JWT"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
) -> User:
    """Dependency para obter usuário autenticado via JWT"""
    token = credentials.credentials
    payload = verify_token(token)
    username = payload.get("sub")
    
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return user


def require_level(required_clearance: int):
    """Factory para dependency que exige nível mínimo de clearance"""
    async def check_clearance(user: User = Depends(get_current_user)) -> User:
        if user.clearance < required_clearance:
            raise HTTPException(
                status_code=403,
                detail=f"Clearance insuficiente. Necessário: {required_clearance}, Seu: {user.clearance}"
            )
        return user
    return check_clearance
