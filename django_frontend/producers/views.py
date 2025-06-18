from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Producer, Farm, Culture
from .forms import ProducerForm, FarmForm, CultureForm
from .services import DashboardService

class ProducerListView(ListView):
    model = Producer
    template_name = 'producers/producer_list.html'
    context_object_name = 'producers'
    paginate_by = 20

class ProducerCreateView(CreateView):
    model = Producer
    form_class = ProducerForm
    template_name = 'producers/producer_form.html'
    success_url = reverse_lazy('producer_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Produtor criado com sucesso!')
        return super().form_valid(form)

class ProducerUpdateView(UpdateView):
    model = Producer
    form_class = ProducerForm
    template_name = 'producers/producer_form.html'
    success_url = reverse_lazy('producer_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Produtor atualizado com sucesso!')
        return super().form_valid(form)

class ProducerDeleteView(DeleteView):
    model = Producer
    template_name = 'producers/producer_confirm_delete.html'
    success_url = reverse_lazy('producer_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Produtor excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

class FarmListView(ListView):
    model = Farm
    template_name = 'producers/farm_list.html'
    context_object_name = 'farms'
    paginate_by = 20

def dashboard_view(request):
    dashboard_service = DashboardService()
    context = dashboard_service.get_dashboard_data()
    return render(request, 'producers/dashboard.html', context)

def dashboard_data(request):
    """API endpoint para dados dos gráficos"""
    dashboard_service = DashboardService()
    data = dashboard_service.get_chart_data()
    return JsonResponse(data)