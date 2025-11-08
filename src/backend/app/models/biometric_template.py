from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, JSON
from sqlalchemy.orm import relationship
from app.config import Base

class BiometricTemplate(Base):
    __tablename__ = "biometric_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    embedding = Column(JSON, nullable=False)  # Armazena o array do embedding em JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship
    # user = relationship("User", back_populates="biometric_template")
