from app.schemas.producer import ProducerCreate
from app.schemas.farm import FarmCreate
from app.schemas.culture import CultureCreate

MOCK_PRODUCER = ProducerCreate(
    cpf_cnpj="12345678901",
    name="João Silva"
)

MOCK_FARM = FarmCreate(
    producer_id="test-id",
    name="Fazenda Esperança",
    city="Ribeirão Preto",
    state="SP",
    total_area=1000.00,
    arable_area=800.00,
    vegetation_area=200.00
)

MOCK_CULTURE = CultureCreate(
    farm_id="test-farm-id",
    name="Soja",
    harvest_year="Safra 2024"
)