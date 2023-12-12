from django.urls import path 
from .views import *

urlpatterns = [
    path('edit/<int:pk>', edit_team, name='edit_team'),
    path('detail/<int:pk>', team_detail, name='team_detail'),
    path('activate/<int:pk>', team_activate, name='team_activate'),
    path('', list_team, name='list_team'),
]
