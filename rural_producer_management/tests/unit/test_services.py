import pytest
from unittest.mock import Mock, AsyncMock
from app.services.producer_service import ProducerService
from app.services.dashboard_service import DashboardService
from app.schemas.producer import ProducerCreate, ProducerUpdate
from tests.fixtures.mock_data import MOCK_PRODUCERS

class TestProducerService:
    @pytest.fixture
    def mock_repository(self):
        return Mock()
    
    @pytest.fixture
    def service(self, mock_repository):
        return ProducerService(mock_repository)
    
    @pytest.mark.asyncio
    async def test_create_producer(self, service, mock_repository):
        # Arrange
        producer_data = MOCK_PRODUCERS[0]
        mock_producer = Mock()
        mock_producer.id = "test-id"
        mock_producer.name = producer_data.name
        mock_producer.cpf_cnpj = producer_data.cpf_cnpj
        
        mock_repository.create = AsyncMock(return_value=mock_producer)
        
        # Act
        result = await service.create(producer_data)
        
        # Assert
        mock_repository.create.assert_called_once_with(producer_data.dict())
        assert result.name == producer_data.name
        assert result.cpf_cnpj == producer_data.cpf_cnpj
    
    @pytest.mark.asyncio
    async def test_get_all_producers(self, service, mock_repository):
        # Arrange
        mock_producers = [Mock(id="1", name="Test 1"), Mock(id="2", name="Test 2")]
        mock_repository.get_all = AsyncMock(return_value=mock_producers)
        
        # Act
        result = await service.get_all()
        
        # Assert
        mock_repository.get_all.assert_called_once()
        assert len(result) == 2
    
    @pytest.mark.asyncio
    async def test_update_producer(self, service, mock_repository):
        # Arrange
        producer_id = "test-id"
        update_data = ProducerUpdate(name="Updated Name", cpf_cnpj="111.444.777-35")
        mock_producer = Mock()
        mock_producer.name = update_data.name
        
        mock_repository.update = AsyncMock(return_value=mock_producer)
        
        # Act
        result = await service.update(producer_id, update_data)
        
        # Assert
        mock_repository.update.assert_called_once_with(producer_id, update_data.dict())
        assert result.name == update_data.name
    
    @pytest.mark.asyncio
    async def test_delete_producer(self, service, mock_repository):
        # Arrange
        producer_id = "test-id"
        mock_repository.delete = AsyncMock(return_value=True)
        
        # Act
        result = await service.delete(producer_id)
        
        # Assert
        mock_repository.delete.assert_called_once_with(producer_id)
        assert result is True

class TestDashboardService:
    @pytest.fixture
    def mock_farm_repo(self):
        return Mock()
    
    @pytest.fixture
    def mock_culture_repo(self):
        return Mock()
    
    @pytest.fixture
    def service(self, mock_farm_repo, mock_culture_repo):
        return DashboardService(mock_farm_repo, mock_culture_repo)
    
    @pytest.mark.asyncio
    async def test_get_dashboard_data(self, service, mock_farm_repo, mock_culture_repo):
        # Arrange
        mock_farms = [
            Mock(total_area=1000.0, arable_area=800.0, vegetation_area=200.0, state="SP"),
            Mock(total_area=500.0, arable_area=400.0, vegetation_area=100.0, state="MG")
        ]
        mock_cultures = [
            Mock(name="SOJA"), Mock(name="MILHO"), Mock(name="SOJA")
        ]
        
        mock_farm_repo.get_all = AsyncMock(return_value=mock_farms)
        mock_culture_repo.get_all = AsyncMock(return_value=mock_cultures)
        
        # Act
        result = await service.get_dashboard_data()
        
        # Assert
        assert result["total_farms"] == 2
        assert result["total_hectares"] == 1500.0
        assert "state_distribution" in result
        assert "culture_distribution" in result
        assert "land_use" in result