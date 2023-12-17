from django.urls import path
from .views import *

app_name='client'

urlpatterns = [
    path('', ClientListAPIView.as_view(), name='client_list'),
    path('detail/<int:pk>/', ClientDetailAPIView.as_view(), name='client_detail'),
    path('addClient/', AddClientAPIView.as_view(), name='add_client'),
    path('delete/<int:pk>/', DestroyClientAPIView.as_view(), name='client_delete'),
    path('edit/<int:pk>/', UpdateClientAPIView.as_view(), name='client_edit'),
    path('addComment/<int:pk>/', CommentAPIView.as_view(), name='add_client_comment'),
    path('add-file/<int:pk>/', AttachFileWithClient.as_view(), name='clients_add_file'),
    path('client_export/', CDetailExportAPI.as_view(), name='client_export'),

]


