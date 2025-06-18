from django import forms
from django.core.exceptions import ValidationError
from .models import Producer, Farm, Culture
from .utils import validate_cpf_cnpj

class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = ['cpf_cnpj', 'name']
        widgets = {
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00 ou 00.000.000/0000-00'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do produtor'
            })
        }
    
    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data['cpf_cnpj']
        if not validate_cpf_cnpj(cpf_cnpj):
            raise ValidationError('CPF/CNPJ inválido')
        return cpf_cnpj

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['producer', 'name', 'city', 'state', 'total_area', 'arable_area', 'vegetation_area']
        widgets = {
            'producer': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'total_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'arable_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'vegetation_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        total_area = cleaned_data.get('total_area')
        arable_area = cleaned_data.get('arable_area')
        vegetation_area = cleaned_data.get('vegetation_area')
        
        if total_area and arable_area and vegetation_area:
            if arable_area + vegetation_area > total_area:
                raise ValidationError('Soma das áreas não pode exceder área total')
        
        return cleaned_data

class CultureForm(forms.ModelForm):
    class Meta:
        model = Culture
        fields = ['farm', 'name', 'harvest_year']
        widgets = {
            'farm': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.Select(attrs={'class': 'form-control'}),
            'harvest_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Safra 2024'
            })
        }