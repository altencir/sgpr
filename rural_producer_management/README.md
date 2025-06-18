rural_producer_management/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── producer.py
│   │   ├── farm.py
│   │   └── culture.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── producer_repository.py
│   │   ├── farm_repository.py
│   │   └── culture_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── producer_service.py
│   │   ├── farm_service.py
│   │   ├── culture_service.py
│   │   └── dashboard_service.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── producer_controller.py
│   │   ├── farm_controller.py
│   │   ├── culture_controller.py
│   │   └── dashboard_controller.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── producer.py
│   │   ├── farm.py
│   │   ├── culture.py
│   │   └── dashboard.py
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── logger.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── fixtures/
│   │   └── mock_data.py
│   ├── unit/
│   │   ├── test_services.py
│   │   ├── test_repositories.py
│   │   └── test_validators.py
│   └── integration/
│       └── test_api.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── alembic.ini
├── alembic/
├── README.md
└── openapi.yaml

# Execução
bash# Clonar e configurar
git clone <repo>
cd rural_producer_management

# Instalar dependências
pip install -r requirements.txt

# Executar com Docker
docker-compose up -d

# Executar testes
pytest

# Executar aplicação local
uvicorn app.main:app --reload

# Endpoints
POST /producers - Criar produtor
GET /producers - Listar produtores
GET /producers/{id} - Obter produtor
PUT /producers/{id} - Atualizar produtor
DELETE /producers/{id} - Deletar produtor
GET /dashboard - Dashboard com métricas

API disponível em: http://localhost:8000/docs