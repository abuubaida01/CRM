from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lead.models import Lead
from team.models import Team
from client.models import Client


@login_required
def dashboard(request):
  team = Team.objects.filter(created_by=request.user)[0]
  lead = Lead.objects.filter(team=team,  converted_to_client=False).order_by('-created_at')[0:5]
  client = Client.objects.filter(team=team,).order_by('-created_at')[0:5]
  return render(request, 'dashboard/dashboard.html', {
    'leads': lead,
    'clients': client
  })