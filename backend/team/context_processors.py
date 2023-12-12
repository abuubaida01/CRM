from .models import Team 
from userprofile.models import Userprofile

def active_team(request):
  if request.user.is_authenticated:
    uu  = Userprofile.objects.get(user=request.user)
    if uu.active_team:
      active_team = uu.active_team
    else:
      active_team = Team.objects.filter(created_by=request.user)[0]
  else: 
    active_team = None

  return {'active_team': active_team}