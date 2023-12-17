from django.urls import path

from .views import *

app_name = 'lead'

urlpatterns = [
    path('createLead/', CreateLeadAPIView.as_view(), name='add_lead'),
    path('', LeadListAPIViews.as_view(), name='leads_list'),
    path('<int:pk>/', LeadDetailAPIView.as_view(), name='lead_detail'),
    path('delete/<int:pk>/', LeadDestroyAPIView.as_view(), name='leads_delete'),
    path('edit/<int:pk>/', UpdateLeadAPIView.as_view(), name='leads_edit'),
    path('convert/<int:pk>/', ConverLead2Client.as_view(), name='convert_to_client'),
    path('add_comment/<int:pk>/', CommentAPIView.as_view(), name='AddCommentView'),
    path('add_file/<int:pk>/', AttachFile2LeadAPIView.as_view(), name='AddFileView'),
]
