import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.repositories.producer_repository import ProducerRepository
from app.models.producer import Producer
from tests.fixtures.mock_data import MOCK_PRODUCERS

class TestProducerRepository:
    @pytest.fixture
    def mock_session(self):
        return Mock()
    
    @pytest.fixture
    def repository(self, mock_session):
        return ProducerRepository(mock_session)
    
    @pytest.mark.asyncio
    async def test_create_producer(self, repository, mock_session):
        # Arrange
        producer_data = MOCK_PRODUCERS[0].dict()
        mock_producer = Mock(spec=Producer)
        
        with patch.object(Producer, '__init__', return_value=None) as mock_init:
            mock_producer.id = "test-id"
            mock_session.add = Mock()
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()
            
            # Act
            result = await repository.create(producer_data)
            
            # Assert
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_by_id(self, repository, mock_session):
        # Arrange
        producer_id = "test-id"
        mock_producer = Mock(spec=Producer)
        mock_session.query.return_value.filter.return_value.first.return_value = mock_producer
        
        # Act
        result = await repository.get_by_id(producer_id)
        
        # Assert
        mock_session.query.assert_called_with(Producer)
        assert result == mock_producer
    
    @pytest.mark.asyncio
    async def test_get_all(self, repository, mock_session):
        # Arrange
        mock_producers = [Mock(spec=Producer), Mock(spec=Producer)]
        mock_session.query.return_value.all.return_value = mock_producers
        
        # Act
        result = await repository.get_all()
        
        # Assert
        mock_session.query.assert_called_with(Producer)
        assert result == mock_producers