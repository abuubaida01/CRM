from django.urls import path 
from .views import *


urlpatterns = [
    path('add-lead/', add_lead, name='add_lead'),
    path('', leads_list, name='leads_list'),
    path('<int:pk>/', lead_detail, name='lead_detail'),
    path('delete/<int:pk>/', leads_delete, name='leads_delete'),
    path('edit/<int:pk>/', leads_edit, name='leads_edit'),
]
