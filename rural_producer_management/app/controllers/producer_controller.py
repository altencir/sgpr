from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.services.producer_service import ProducerService
from app.schemas.producer import ProducerCreate, ProducerUpdate, ProducerResponse
from app.dependencies import get_producer_service

router = APIRouter(prefix="/producers", tags=["producers"])

@router.post("/", response_model=ProducerResponse, status_code=status.HTTP_201_CREATED)
async def create_producer(
    data: ProducerCreate,
    service: ProducerService = Depends(get_producer_service)
):
    return await service.create(data)

@router.get("/{producer_id}", response_model=ProducerResponse)
async def get_producer(
    producer_id: str,
    service: ProducerService = Depends(get_producer_service)
):
    producer = await service.get_by_id(producer_id)
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer

@router.get("/", response_model=List[ProducerResponse])
async def list_producers(service: ProducerService = Depends(get_producer_service)):
    return await service.get_all()

@router.put("/{producer_id}", response_model=ProducerResponse)
async def update_producer(
    producer_id: str,
    data: ProducerUpdate,
    service: ProducerService = Depends(get_producer_service)
):
    producer = await service.update(producer_id, data)
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer

@router.delete("/{producer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_producer(
    producer_id: str,
    service: ProducerService = Depends(get_producer_service)
):
    if not await service.delete(producer_id):
        raise HTTPException(status_code=404, detail="Producer not found")