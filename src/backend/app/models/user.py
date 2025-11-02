from sqlalchemy import Column, Integer, String, DateTime, func
from app.config import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # bcrypt hash
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
