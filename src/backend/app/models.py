"""Modelos SQLAlchemy para o BioAccess"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from .db import Base


class User(Base):
    """Modelo de usuário do sistema"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False)  # public, director, minister
    clearance = Column(Integer, nullable=False)  # 1, 2, 3
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BiometricTemplate(Base):
    """Template biométrico (embedding facial)"""
    __tablename__ = "biometric_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    embedding = Column(JSON, nullable=False)  # armazena lista de floats
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    """Log de auditoria de todas as ações do sistema"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, nullable=False)
    action = Column(String, nullable=False)
    level_requested = Column(Integer, default=0)
    success = Column(Boolean, nullable=False)
    origin_ip = Column(String, nullable=True)
    ts = Column(DateTime(timezone=True), server_default=func.now(), index=True)
