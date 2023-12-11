from django.urls import path
from .views import *

urlpatterns = [
    path('', client_list, name='client_list'),
    path('<int:pk>', client_detail, name='client_detail'),
    path('add/', add_client, name='add_client'),
    path('delete/<int:pk>/', client_delete, name='client_delete'),
    path('edit/<int:pk>/', client_edit, name='client_edit'),
]


