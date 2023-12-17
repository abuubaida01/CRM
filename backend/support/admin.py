from django.contrib import admin
from .models import Sugg2Savior, ReportUser
from django.utils.html import mark_safe, format_html

@admin.register(Sugg2Savior)
class SefarzSuggestions(admin.ModelAdmin):
  list_display = ('savior_adviser','suggestion','id', 'created' )

@admin.register(ReportUser)
class UserRep(admin.ModelAdmin):
  list_display = ('reporter_profile','reported_profile','problem','id', 'created' )


# @admin.register(SefarzMembers)
# class SefarzMembers(admin.ModelAdmin):
#   list_display = ('member_profile', 'deposit_receipt','id', 'created' )
