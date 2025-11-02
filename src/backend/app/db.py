"""Configuração do banco de dados SQLAlchemy + Supabase PostgreSQL"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os

# Prioridade: SUPABASE_DB_URL > DATABASE_URL > SQLite local
db_url = (
    settings.SUPABASE_DB_URL or 
    settings.DATABASE_URL or 
    os.getenv("DATABASE_URL") or
    "sqlite:///./bioaccess.db"  # Fallback para desenvolvimento
)

# Ajustar configurações baseado no tipo de banco
if db_url.startswith("postgresql"):
    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
elif db_url.startswith("sqlite"):
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(db_url)

print(f"🗄️  Conectando ao banco: {db_url.split('@')[0] if '@' in db_url else 'SQLite local'}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency para obter sessão de banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

