from django.contrib import admin

from .models import * 

admin.site.register(Lead)
admin.site.register(Comment)
admin.site.register(LeadFile)