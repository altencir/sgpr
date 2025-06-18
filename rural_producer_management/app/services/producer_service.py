from typing import List, Optional
from app.repositories.producer_repository import ProducerRepository
from app.schemas.producer import ProducerCreate, ProducerUpdate, ProducerResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

class ProducerService:
    def __init__(self, repository: ProducerRepository):
        self._repository = repository
    
    async def create(self, data: ProducerCreate) -> ProducerResponse:
        logger.info(f"Creating producer: {data.name}")
        producer = await self._repository.create(data.dict())
        logger.info(f"Producer created: {producer.id}")
        return ProducerResponse.from_orm(producer)
    
    async def get_by_id(self, producer_id: str) -> Optional[ProducerResponse]:
        producer = await self._repository.get_by_id(producer_id)
        return ProducerResponse.from_orm(producer) if producer else None
    
    async def get_all(self) -> List[ProducerResponse]:
        producers = await self._repository.get_all()
        return [ProducerResponse.from_orm(p) for p in producers]
    
    async def update(self, producer_id: str, data: ProducerUpdate) -> Optional[ProducerResponse]:
        logger.info(f"Updating producer: {producer_id}")
        producer = await self._repository.update(producer_id, data.dict())
        return ProducerResponse.from_orm(producer) if producer else None
    
    async def delete(self, producer_id: str) -> bool:
        logger.info(f"Deleting producer: {producer_id}")
        return await self._repository.delete(producer_id)