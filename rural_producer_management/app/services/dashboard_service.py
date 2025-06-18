from typing import Dict, List
from app.repositories.farm_repository import FarmRepository
from app.repositories.culture_repository import CultureRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)

class DashboardService:
    def __init__(self, farm_repo: FarmRepository, culture_repo: CultureRepository):
        self._farm_repo = farm_repo
        self._culture_repo = culture_repo
    
    async def get_dashboard_data(self) -> Dict:
        logger.info("Generating dashboard data")
        
        farms = await self._farm_repo.get_all()
        cultures = await self._culture_repo.get_all()
        
        total_farms = len(farms)
        total_hectares = sum(float(farm.total_area) for farm in farms)
        
        state_distribution = {}
        for farm in farms:
            state_distribution[farm.state] = state_distribution.get(farm.state, 0) + 1
        
        culture_distribution = {}
        for culture in cultures:
            culture_distribution[culture.name] = culture_distribution.get(culture.name, 0) + 1
        
        land_use = {
            "arable": sum(float(farm.arable_area) for farm in farms),
            "vegetation": sum(float(farm.vegetation_area) for farm in farms)
        }
        
        return {
            "total_farms": total_farms,
            "total_hectares": total_hectares,
            "state_distribution": state_distribution,
            "culture_distribution": culture_distribution,
            "land_use": land_use
        }