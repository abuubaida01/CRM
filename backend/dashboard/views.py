from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lead.models import Lead
from team.models import Team
from client.models import Client
from userprofile.models import Userprofile


@login_required
def dashboard(request):
  at = Userprofile.objects.get(user=request.user).active_team
  
  lead = Lead.objects.filter(team=at,  converted_to_client=False).order_by('-created_at')[0:5]
  client = Client.objects.filter(team=at,).order_by('-created_at')[0:5]
  return render(request, 'dashboard/dashboard.html', {
    'leads': lead,
    'clients': client
  })