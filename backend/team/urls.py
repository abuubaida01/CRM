from django.urls import path 
from .views import *

app_name = 'team'

urlpatterns = [
    path('CreateTeam/', CreateTeamAPIView.as_view(), name='createTeam'),
    path('edit/<int:pk>', UpdateTeamAPIView.as_view(), name='edit_team'),
    path('detail/<int:pk>', RetrieveTeamAPIView.as_view(), name='team_detail'),
    path('activate/<int:pk>', ActivateTeam.as_view(), name='team_activate'),
    path('', ListTeamsAPIView.as_view(), name='list_team'),

    path('CreatePlan/', CreatePlanAPIView.as_view(), name='CreatePlan'),
    path("updatePlan/<int:pk>/", UpdatePlanAPIView.as_view(), name='UpdatePlan'),
    path("ListPlan/", ListPlanAPIView.as_view(), name='ListPlan'),
    path("plan/<int:pk>/", RetrievePlanAPIView.as_view(), name='ListPlan'),
    path("delete/<int:pk>/", DestroyPlanAPIView.as_view(), name='ListPlan'),


]
