from django.urls import path
from support import views
app_name = 'support'  

urlpatterns = [
    path('Sugg2Savior', views.Sugg2SaviorAPIView.as_view(), name='Sugg2SaviorFunc'),
    path('ReportUser', views.ReportUserAPI.as_view(), name='ReportUserFunc'),

]
