from django.contrib import admin

from .models import Team, Plan


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
  list_display = [
    'id',
    'plan',
    'name',
    'created_by',
    'created_at',
  ]


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
  list_display = [
    'id',
    'name',
    'price',
    'description',
    'max_leads',
    'max_clients',
  ]