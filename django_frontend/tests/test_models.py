import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from producers.models import Producer, Farm, Culture

class TestProducerModel(TestCase):
    def test_create_producer_valid_cpf(self):
        producer = Producer.objects.create(
            cpf_cnpj="111.444.777-35",
            name="João Silva"
        )
        assert producer.name == "João Silva"
        assert producer.cpf_cnpj == "111.444.777-35"
        assert str(producer) == "João Silva"
    
    def test_create_producer_valid_cnpj(self):
        producer = Producer.objects.create(
            cpf_cnpj="11.222.333/0001-81",
            name="Empresa Rural Ltda"
        )
        assert producer.name == "Empresa Rural Ltda"
    
    def test_producer_unique_cpf_cnpj(self):
        Producer.objects.create(
            cpf_cnpj="111.444.777-35",
            name="João Silva"
        )
        
        with pytest.raises(Exception):  # IntegrityError
            Producer.objects.create(
                cpf_cnpj="111.444.777-35",
                name="Outro João"
            )
    
    def test_producer_str_representation(self):
        producer = Producer(name="Maria Santos")
        assert str(producer) == "Maria Santos"
    
    def test_producer_ordering(self):
        Producer.objects.create(cpf_cnpj="111.444.777-35", name="Z Silva")
        Producer.objects.create(cpf_cnpj="222.333.444-56", name="A Santos")
        
        producers = list(Producer.objects.all())
        assert producers[0].name == "A Santos"
        assert producers[1].name == "Z Silva"

class TestFarmModel(TestCase):
    def setUp(self):
        self.producer = Producer.objects.create(
            cpf_cnpj="111.444.777-35",
            name="João Silva"
        )
    
    def test_create_farm_valid_areas(self):
        farm = Farm.objects.create(
            producer=self.producer,
            name="Fazenda Esperança",
            city="Ribeirão Preto",
            state="SP",
            total_area=Decimal("1000.00"),
            arable_area=Decimal("800.00"),
            vegetation_area=Decimal("200.00")
        )
        assert farm.total_area == Decimal("1000.00")
        assert farm.state == "SP"
        assert "Fazenda Esperança" in str(farm)
        assert "João Silva" in str(farm)
    
    def test_farm_area_validation_success(self):
        farm = Farm(
            producer=self.producer,
            name="Fazenda Teste",
            city="São Paulo",
            state="SP",
            total_area=Decimal("100.00"),
            arable_area=Decimal("70.00"),
            vegetation_area=Decimal("30.00")  # Total = 100
        )
        
        # Não deve levantar exceção
        farm.clean()
    
    def test_farm_area_validation_failure(self):
        farm = Farm(
            producer=self.producer,
            name="Fazenda Teste",
            city="São Paulo",
            state="SP",
            total_area=Decimal("100.00"),
            arable_area=Decimal("80.00"),
            vegetation_area=Decimal("30.00")  # Total > 100
        )
        
        with pytest.raises(ValidationError):
            farm.clean()
    
    def test_farm_state_choices(self):
        farm = Farm(
            producer=self.producer,
            name="Fazenda Teste",
            city="São Paulo",
            state="XX",  # Estado inválido
            total_area=Decimal("100.00"),
            arable_area=Decimal("80.00"),
            vegetation_area=Decimal("20.00")
        )
        
        # Django validará isso no form, não no model
        assert farm.state == "XX"
    
    def test_farm_cascade_delete(self):
        farm = Farm.objects.create(
            producer=self.producer,
            name="Fazenda Teste",
            city="São Paulo",
            state="SP",
            total_area=Decimal("100.00"),
            arable_area=Decimal("80.00"),
            vegetation_area=Decimal("20.00")
        )
        
        farm_id = farm.id
        self.producer.delete()
        
        assert not Farm.objects.filter(id=farm_id).exists()

class TestCultureModel(TestCase):
    def setUp(self):
        self.producer = Producer.objects.create(
            cpf_cnpj="111.444.777-35",
            name="João Silva"
        )
        self.farm = Farm.objects.create(
            producer=self.producer,
            name="Fazenda Teste",
            city="São Paulo",
            state="SP",
            total_area=Decimal("1000.00"),
            arable_area=Decimal("800.00"),
            vegetation_area=Decimal("200.00")
        )
    
    def test_create_culture(self):
        culture = Culture.objects.create(
            farm=self.farm,
            name="SOJA",
            harvest_year="Safra 2024"
        )
        assert culture.name == "SOJA"
        assert culture.harvest_year == "Safra 2024"
        assert "SOJA" in str(culture)
        assert "Safra 2024" in str(culture)
    
    def test_culture_choices(self):
        # Testar se as opções estão disponíveis
        choices = dict(Culture.CULTURE_CHOICES)
        assert "SOJA" in choices
        assert "MILHO" in choices
        assert "CAFE" in choices
    
    def test_culture_unique_together(self):
        Culture.objects.create(
            farm=self.farm,
            name="SOJA",
            harvest_year="Safra 2024"
        )
        
        with pytest.raises(Exception):  # IntegrityError
            Culture.objects.create(
                farm=self.farm,
                name="SOJA",
                harvest_year="Safra 2024"  # Mesma fazenda, cultura e safra
            )
    
    def test_culture_cascade_delete(self):
        culture = Culture.objects.create(
            farm=self.farm,
            name="SOJA",
            harvest_year="Safra 2024"
        )
        
        culture_id = culture.id
        self.farm.delete()
        
        assert not Culture.objects.filter(id=culture_id).exists()

class TestModelManagers(TestCase):
    def setUp(self):
        self.producer = Producer.objects.create(
            cpf_cnpj="111.444.777-35",
            name="João Silva"
        )
        
        # Criar algumas fazendas para teste
        Farm.objects.create(
            producer=self.producer, name="Fazenda SP", city="São Paulo", state="SP",
            total_area=1000, arable_area=800, vegetation_area=200
        )
        Farm.objects.create(
            producer=self.producer, name="Fazenda MG", city="Uberlândia", state="MG",
            total_area=500, arable_area=400, vegetation_area=100
        )
    
    def test_farm_with_totals(self):
        totals = Farm.objects.with_totals()
        
        assert totals['total_farms'] == 2
        assert totals['total_area'] == 1500
        assert totals['total_arable'] == 1200
        assert totals['total_vegetation'] == 300
    
    def test_farm_by_state(self):
        states = Farm.objects.by_state()
        
        assert len(states) == 2
        # Verificar se contém SP e MG
        state_codes = [s['state'] for s in states]
        assert 'SP' in state_codes
        assert 'MG' in state_codes# Sistema de Gestão de Produtores Rurais

## Estrutura do Projeto