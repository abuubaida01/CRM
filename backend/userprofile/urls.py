from django.urls import path 
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path("signup/", signup, name='signup'),
    path("log-in/", views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('log-out/', views.LogoutView.as_view(), name='logout')
]
