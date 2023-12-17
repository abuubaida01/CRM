from django.contrib import admin

from .models import * 



@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin): 
  list_display = [
    'id',
    'created_by',
    'created_at',
    'modified_at',
    'priority',
    'status',
    'name',
    'email',
    'description',
    'converted_to_client',
    'team',
  ]
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = [
    'id',
    'team',
    'lead',
    'created_by',
    'content',
    'created_at',
  ]
  pass

@admin.register(LeadFile)
class LeadFileAdmin(admin.ModelAdmin):
  list_display = [
    'id',
    'team',
    'lead',
    'created_by',
    'file',
    'created_at',
  ]