from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from app.utils.validators import validate_cpf_cnpj

class ProducerBase(BaseModel):
    cpf_cnpj: str
    name: str
    
    @validator('cpf_cnpj')
    def validate_cpf_cnpj_format(cls, v):
        if not validate_cpf_cnpj(v):
            raise ValueError('CPF/CNPJ inválido')
        return v

class ProducerCreate(ProducerBase):
    pass

class ProducerUpdate(ProducerBase):
    pass

class ProducerResponse(ProducerBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True