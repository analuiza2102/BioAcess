"""Configuração do banco de dados SQLAlchemy + Supabase PostgreSQL"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.SUPABASE_DB_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency para obter sessão de banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
