from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class FarmBase(BaseModel):
    name: str
    city: str
    state: str
    total_area: Decimal
    arable_area: Decimal
    vegetation_area: Decimal
    
    @validator('state')
    def validate_state(cls, v):
        if len(v) != 2 or not v.isupper():
            raise ValueError('Estado deve ter 2 caracteres maiúsculos')
        return v
    
    @validator('vegetation_area')
    def validate_area_sum(cls, v, values):
        if 'arable_area' in values and 'total_area' in values:
            if v + values['arable_area'] > values['total_area']:
                raise ValueError('Soma das áreas não pode exceder área total')
        return v

class FarmCreate(FarmBase):
    producer_id: str

class FarmUpdate(FarmBase):
    pass

class FarmResponse(FarmBase):
    id: str
    producer_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True