from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls"), name='index' ),
    path('user/', include("user.urls"), name='index' ),
    path('dashboard/', include("dashboard.urls"), name='dashboard' ),
    path('dashboard/lead/', include("lead.urls"), name='lead' ),
    path('dashboard/client/', include("client.urls"), name='client' ),
    path('dashboard/team/', include("team.urls"), name='team' ),
    path('api-auth/', include('rest_framework.urls')),
]
