from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lead.models import Lead
from team.models import Team
from client.models import Client
from profiles.models import Profile

#====================================================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.status import HTTP_200_OK
from team.models import Team
from client.serializers import ClientSerializer
from lead.serializers import LeadSerializer


class Dashboard(APIView):

  def get(self, request,*args, **kwargs):
    at = Profile.objects.get(user=request.user).active_team
    leads = Lead.objects.filter(team=at,  converted_to_client=False).order_by('-created_at')[0:5]
    clients = Client.objects.filter(team=at,).order_by('-created_at')[0:5]

    leadSeri = LeadSerializer(leads, many=True)
    clientSeri = ClientSerializer(leads, many=True)

    return Response({'leads':leadSeri, "clientSeri":clientSeri}, HTTP_200_OK)

# @login_required
# def dashboard(request):
#   at = Profile.objects.get(user=request.user).active_team
  
#   lead = Lead.objects.filter(team=at,  converted_to_client=False).order_by('-created_at')[0:5]
#   client = Client.objects.filter(team=at,).order_by('-created_at')[0:5]
#   return render(request, 'dashboard/dashboard.html', {
#     'leads': lead,
#     'clients': client
#   })