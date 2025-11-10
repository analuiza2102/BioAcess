import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# Aceita DATABASE_URL ou SUPABASE_DB_URL (mais flexível)
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL", "sqlite:///./bioaccess.db")

# Configurações de pool para PostgreSQL (evita conexões expiradas)
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        poolclass=NullPool,  # Não mantém pool de conexões (ideal para Supabase pooler)
        connect_args={
            "connect_timeout": 10,
            "options": "-c timezone=utc"
        }
    )
else:
    # SQLite
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
