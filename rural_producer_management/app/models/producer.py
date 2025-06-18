from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Producer(Base):
    __tablename__ = "producers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cpf_cnpj = Column(String(18), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    farms = relationship("Farm", back_populates="producer", cascade="all, delete-orphan")