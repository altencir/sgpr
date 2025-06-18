from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/data/', views.dashboard_data, name='dashboard_data'),
    
    path('producers/', views.ProducerListView.as_view(), name='producer_list'),
    path('producers/create/', views.ProducerCreateView.as_view(), name='producer_create'),
    path('producers/<uuid:pk>/edit/', views.ProducerUpdateView.as_view(), name='producer_update'),
    path('producers/<uuid:pk>/delete/', views.ProducerDeleteView.as_view(), name='producer_delete'),
    
    path('farms/', views.FarmListView.as_view(), name='farm_list'),
]