from django.contrib import admin
from .models import Profile
# Register your models here.


# admin.site.register(Profile)
# admin.site.register(Relationship)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('user','cat','restriction_hits','cur_add','reported','promote','created')

