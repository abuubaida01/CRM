from django.urls import path 
from .views import *

urlpatterns = [
    path('edit/<int:pk>', edit_team, name='edit_team')
]
