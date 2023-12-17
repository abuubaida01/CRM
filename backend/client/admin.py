from django.contrib import admin
from .models import * 

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
  list_display = [
    'id',
    'team',
    'created_by',
    'name',
    'email',
    'description',
    'modified_at',
    'created_at',
  ]


@admin.register(ClientFile)
class ClientAdmin(admin.ModelAdmin):
  list_display = [
    'id',
    'team',
    'created_by',
    'client',
    'file',
    'created_at',
  ]


@admin.register(Comment)
class ClientAdmin(admin.ModelAdmin):
  list_display = [
    'id',
    'team',
    'created_by',
    'client',
    'content',
    'created_at',
    
  ]
