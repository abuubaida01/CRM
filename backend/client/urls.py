from django.urls import path
from .views import *

urlpatterns = [
    path('', client_list, name='client_list'),
    path('<int:pk>', client_detail, name='client_detail'),
    path('add/', add_client, name='add_client'),
    path('delete/<int:pk>/', client_delete, name='client_delete'),
    path('edit/<int:pk>/', client_edit, name='client_edit'),
    path('add-comment/<int:pk>/', client_detail, name='add_client_comment'),
    path('add-file/<int:pk>/', clients_add_file, name='clients_add_file'),
    path('client_export/', client_export, name='client_export'),

]


