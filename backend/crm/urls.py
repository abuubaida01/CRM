from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls"), name='index' ),
    path('user/', include("userprofile.urls"), name='index' ),
    path('dashboard/', include("dashboard.urls"), name='dashboard' ),
    path('dashboard/lead/', include("lead.urls"), name='lead' ),
    path('dashboard/client/', include("client.urls"), name='client' ),
    path('dashboard/teams/', include("team.urls"), name='team' ),
]
