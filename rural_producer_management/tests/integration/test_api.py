import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.fixtures.mock_data import MOCK_PRODUCERS, MOCK_FARMS, MOCK_CULTURES

client = TestClient(app)

class TestProducerAPI:
    def test_create_producer_success(self):
        # Arrange
        producer_data = MOCK_PRODUCERS[0].dict()
        
        # Act
        response = client.post("/producers/", json=producer_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == producer_data["name"]
        assert data["cpf_cnpj"] == producer_data["cpf_cnpj"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_producer_invalid_cpf(self):
        # Arrange
        invalid_producer = MOCK_PRODUCERS[0].dict()
        invalid_producer["cpf_cnpj"] = "123.456.789-00"  # CPF inválido
        
        # Act
        response = client.post("/producers/", json=invalid_producer)
        
        # Assert
        assert response.status_code == 422
        assert "CPF/CNPJ inválido" in str(response.json())
    
    def test_create_producer_duplicate_cpf(self):
        # Arrange
        producer_data = MOCK_PRODUCERS[0].dict()
        
        # Act - Criar primeiro produtor
        response1 = client.post("/producers/", json=producer_data)
        assert response1.status_code == 201
        
        # Act - Tentar criar com mesmo CPF
        response2 = client.post("/producers/", json=producer_data)
        
        # Assert
        assert response2.status_code == 400
    
    def test_get_producers_empty(self):
        # Act
        response = client.get("/producers/")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_producer_by_id_not_found(self):
        # Act
        response = client.get("/producers/non-existent-id")
        
        # Assert
        assert response.status_code == 404
    
    def test_update_producer_success(self):
        # Arrange - Criar produtor primeiro
        producer_data = MOCK_PRODUCERS[0].dict()
        create_response = client.post("/producers/", json=producer_data)
        producer_id = create_response.json()["id"]
        
        update_data = {"name": "Nome Atualizado", "cpf_cnpj": producer_data["cpf_cnpj"]}
        
        # Act
        response = client.put(f"/producers/{producer_id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Nome Atualizado"
    
    def test_delete_producer_success(self):
        # Arrange - Criar produtor primeiro
        producer_data = MOCK_PRODUCERS[0].dict()
        create_response = client.post("/producers/", json=producer_data)
        producer_id = create_response.json()["id"]
        
        # Act
        response = client.delete(f"/producers/{producer_id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verificar se foi deletado
        get_response = client.get(f"/producers/{producer_id}")
        assert get_response.status_code == 404

class TestFarmAPI:
    def setup_method(self):
        # Criar produtor para os testes de fazenda
        producer_data = MOCK_PRODUCERS[0].dict()
        response = client.post("/producers/", json=producer_data)
        self.producer_id = response.json()["id"]
    
    def test_create_farm_success(self):
        # Arrange
        farm_data = MOCK_FARMS[0].dict()
        farm_data["producer_id"] = self.producer_id
        
        # Act
        response = client.post("/farms/", json=farm_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == farm_data["name"]
        assert data["producer_id"] == self.producer_id
    
    def test_create_farm_invalid_areas(self):
        # Arrange
        farm_data = MOCK_FARMS[0].dict()
        farm_data["producer_id"] = self.producer_id
        farm_data["arable_area"] = 900.0
        farm_data["vegetation_area"] = 200.0  # Total > 1000
        
        # Act
        response = client.post("/farms/", json=farm_data)
        
        # Assert
        assert response.status_code == 422
    
    def test_create_farm_nonexistent_producer(self):
        # Arrange
        farm_data = MOCK_FARMS[0].dict()
        farm_data["producer_id"] = "non-existent-id"
        
        # Act
        response = client.post("/farms/", json=farm_data)
        
        # Assert
        assert response.status_code == 404

class TestCultureAPI:
    def setup_method(self):
        # Criar produtor e fazenda para os testes de cultura
        producer_data = MOCK_PRODUCERS[0].dict()
        producer_response = client.post("/producers/", json=producer_data)
        self.producer_id = producer_response.json()["id"]
        
        farm_data = MOCK_FARMS[0].dict()
        farm_data["producer_id"] = self.producer_id
        farm_response = client.post("/farms/", json=farm_data)
        self.farm_id = farm_response.json()["id"]
    
    def test_create_culture_success(self):
        # Arrange
        culture_data = MOCK_CULTURES[0].dict()
        culture_data["farm_id"] = self.farm_id
        
        # Act
        response = client.post("/cultures/", json=culture_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == culture_data["name"]
        assert data["farm_id"] == self.farm_id
    
    def test_create_duplicate_culture(self):
        # Arrange
        culture_data = MOCK_CULTURES[0].dict()
        culture_data["farm_id"] = self.farm_id
        
        # Act - Criar primeira cultura
        response1 = client.post("/cultures/", json=culture_data)
        assert response1.status_code == 201
        
        # Act - Tentar criar duplicata
        response2 = client.post("/cultures/", json=culture_data)
        
        # Assert
        assert response2.status_code == 409  # Conflict

class TestDashboardAPI:
    def test_get_dashboard_empty(self):
        # Act
        response = client.get("/dashboard/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        required_fields = [
            "total_farms", "total_hectares", 
            "state_distribution", "culture_distribution", "land_use"
        ]
        
        for field in required_fields:
            assert field in data
        
        assert data["total_farms"] == 0
        assert data["total_hectares"] == 0.0
    
    def test_get_dashboard_with_data(self):
        # Arrange - Criar dados de teste
        producer_data = MOCK_PRODUCERS[0].dict()
        producer_response = client.post("/producers/", json=producer_data)
        producer_id = producer_response.json()["id"]
        
        farm_data = MOCK_FARMS[0].dict()
        farm_data["producer_id"] = producer_id
        farm_response = client.post("/farms/", json=farm_data)
        farm_id = farm_response.json()["id"]
        
        culture_data = MOCK_CULTURES[0].dict()
        culture_data["farm_id"] = farm_id
        client.post("/cultures/", json=culture_data)
        
        # Act
        response = client.get("/dashboard/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_farms"] == 1
        assert data["total_hectares"] == float(farm_data["total_area"])
        assert len(data["state_distribution"]) > 0
        assert len(data["culture_distribution"]) > 0

class TestAPIValidation:
    def test_invalid_json(self):
        # Act
        response = client.post("/producers/", json={"invalid": "data"})
        
        # Assert
        assert response.status_code == 422
    
    def test_missing_required_fields(self):
        # Act
        response = client.post("/producers/", json={"name": "Test"})  # Missing cpf_cnpj
        
        # Assert
        assert response.status_code == 422
    
    def test_invalid_field_types(self):
        # Act
        response = client.post("/farms/", json={
            "producer_id": "valid-id",
            "name": "Test Farm",
            "total_area": "invalid_number"  # Should be number
        })
        
        # Assert
        assert response.status_code == 422

class TestAPIErrors:
    def test_server_error_handling(self):
        # Simular erro interno seria complexo, mas podemos testar endpoints inexistentes
        response = client.get("/nonexistent-endpoint/")
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        # Act
        response = client.patch("/producers/")  # PATCH not allowed on collection
        
        # Assert
        assert response.status_code == 405