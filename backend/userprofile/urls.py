from django.urls import path 
from .views import *
from django.contrib.auth import views
from .forms import LoginForm

urlpatterns = [
    path("signup/", signup, name='signup'),
    path("log-in/", views.LoginView.as_view(template_name='userprofile/login.html', authentication_form=LoginForm), name='login'),
    path('log-out/', views.LogoutView.as_view(), name='logout'),
    path('my_account/', my_account, name='my_account'),
]
