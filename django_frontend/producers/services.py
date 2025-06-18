from django.db.models import Sum, Count
from .models import Producer, Farm, Culture

class DashboardService:
    def get_dashboard_data(self):
        farms = Farm.objects.all()
        cultures = Culture.objects.all()
        
        total_farms = farms.count()
        total_hectares = farms.aggregate(Sum('total_area'))['total_area__sum'] or 0
        
        return {
            'total_farms': total_farms,
            'total_hectares': float(total_hectares),
            'total_producers': Producer.objects.count(),
            'total_cultures': cultures.count(),
        }
    
    def get_chart_data(self):
        # Distribuição por estado
        state_data = list(
            Farm.objects.values('state')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        # Distribuição por cultura
        culture_data = list(
            Culture.objects.values('name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        # Uso do solo
        land_use_data = Farm.objects.aggregate(
            arable=Sum('arable_area'),
            vegetation=Sum('vegetation_area')
        )
        
        return {
            'states': state_data,
            'cultures': culture_data,
            'land_use': [
                {'name': 'Área Agricultável', 'value': float(land_use_data['arable'] or 0)},
                {'name': 'Área de Vegetação', 'value': float(land_use_data['vegetation'] or 0)}
            ]
        }