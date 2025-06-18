from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Farm(Base):
    __tablename__ = "farms"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    producer_id = Column(String, ForeignKey("producers.id"), nullable=False)
    name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    total_area = Column(Numeric(10, 2), nullable=False)
    arable_area = Column(Numeric(10, 2), nullable=False)
    vegetation_area = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    producer = relationship("Producer", back_populates="farms")
    cultures = relationship("Culture", back_populates="farm", cascade="all, delete-orphan")