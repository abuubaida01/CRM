from django.urls import path 
from .views import *


urlpatterns = [
    path('add-lead/', add_lead, name='add_lead'),
    path('', leads_list, name='leads_list'),
    path('<int:pk>/', lead_detail.as_view(), name='lead_detail'),
    path('delete/<int:pk>/', leads_delete, name='leads_delete'),
    path('edit/<int:pk>/', leads_edit, name='leads_edit'),
    path('convert/<int:pk>/', convert_to_client, name='convert_to_client'),
    path('<int:pk>/add_comment/', AddCommentView.as_view(), name='AddCommentView'),
    path('<int:pk>/add_file/', AddFileView.as_view(), name='AddFileView'),
]
