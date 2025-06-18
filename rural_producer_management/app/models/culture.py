from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Culture(Base):
    __tablename__ = "cultures"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_id = Column(String, ForeignKey("farms.id"), nullable=False)
    name = Column(String(100), nullable=False)
    harvest_year = Column(String(9), nullable=False)  # "Safra 2024"
    created_at = Column(DateTime, server_default=func.now())
    
    farm = relationship("Farm", back_populates="cultures")