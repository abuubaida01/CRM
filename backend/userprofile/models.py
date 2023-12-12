from team.models import Team
from django.db import models
from django.contrib.auth.models import User

class Userprofile(models.Model):
  user = models.OneToOneField(User, related_name='UserProfile', on_delete=models.CASCADE)
  active_team = models.ForeignKey(Team, related_name='userprofiles', blank=True, on_delete=models.CASCADE, null=True)
