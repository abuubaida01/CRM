from django.contrib import admin
from .models import * 

admin.site.register(Client)
admin.site.register(Comment)
admin.site.register(ClientFile)

