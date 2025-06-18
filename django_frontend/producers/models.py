from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal
import uuid

class Producer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf_cnpj = models.CharField(
        max_length=18, 
        unique=True,
        validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})]
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'producers'
        ordering = ['name']

class Farm(models.Model):
    STATES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATES)
    total_area = models.DecimalField(max_digits=10, decimal_places=2)
    arable_area = models.DecimalField(max_digits=10, decimal_places=2)
    vegetation_area = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if self.arable_area + self.vegetation_area > self.total_area:
            raise models.ValidationError('Soma das áreas não pode exceder área total')
    
    def __str__(self):
        return f"{self.name} - {self.producer.name}"
    
    class Meta:
        db_table = 'farms'

class Culture(models.Model):
    CULTURE_CHOICES = [
        ('SOJA', 'Soja'), ('MILHO', 'Milho'), ('ALGODAO', 'Algodão'), ('CAFE', 'Café'),
        ('CANA', 'Cana-de-açúcar'), ('ARROZ', 'Arroz'), ('FEIJAO', 'Feijão'),
        ('TRIGO', 'Trigo'), ('OUTROS', 'Outros')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='cultures')
    name = models.CharField(max_length=100, choices=CULTURE_CHOICES)
    harvest_year = models.CharField(max_length=9)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.harvest_year}"
    
    class Meta:
        db_table = 'cultures'
        unique_together = ['farm', 'name', 'harvest_year']