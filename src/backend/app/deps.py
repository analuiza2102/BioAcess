"""Dependências reutilizáveis do FastAPI"""

from fastapi import Depends
from sqlalchemy.orm import Session
from .db import get_db
from .security import get_current_user, require_level
from .models import User

# Re-exporta dependências comuns para facilitar imports
__all__ = ["get_db", "get_current_user", "require_level"]
