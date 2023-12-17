from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import AddLeadForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lead
from django.contrib import messages
from .forms import AddCommentForm, LeadFileForm
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from client.models import Client, Comment as Client_Comment
from django.views.generic import View
from profiles.models import Profile

#====================================================
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.status import HTTP_200_OK
from .serializers import * 

from team.models import Team


class LeadListAPIViews(ListAPIView):
  serializer_class = LeadSerializer

  def get_queryset(self):
      return Lead.objects.filter(created_by=self.request.user) 

  


class LeadDetailAPIView(RetrieveAPIView):
  serializer_class = LeadSerializer
  queryset = Lead.objects.all()
  lookup_field = 'pk'



class CommentAPIView(ListCreateAPIView):
  serializer_class = CommentSerializer
  queryset = Comment.objects.all()

  def post(self, request, pk,*args, **kwargs):
    at = Profile.objects.get(user=request.user).active_team
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(HTTP_200_OK)



class AttachFile2LeadAPIView(ListCreateAPIView):
  serializer_class = LeadFileSerializer
  queryset = LeadFile.objects.all()

  def post(self, request, pk,*args, **kwargs):
      # at = Profile.objects.get(user=request.user).active_team
      # lead = Lead.objects.get(pk=pk, user=self.request.user)
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(HTTP_200_OK)




class CreateLeadAPIView(ListCreateAPIView):
  serializer_class = LeadSerializer
  queryset = Lead.objects.all()

  def post(self, request,*args, **kwargs):
    at = Profile.objects.get(user=request.user).active_team
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(team=at)
    return Response(HTTP_200_OK)


class UpdateLeadAPIView(RetrieveUpdateAPIView):
  serializer_class = LeadSerializer
  queryset = Lead.objects.all()
  lookup_field = 'pk'

  def patch(self, request, pk, *args, **kwargs):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    serializer = self.get_serializer(lead, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(HTTP_200_OK)


class LeadDestroyAPIView(RetrieveDestroyAPIView):
  serializer_class = LeadSerializer
  queryset = Lead.objects.all()
  lookup_field = 'pk'



class ConverLead2Client(APIView):
  serializer_class = LeadSerializer

  def post(self, request, pk, *args, **kwargs):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    at = Profile.objects.get(user=request.user).active_team
    
    client = Client.objects.create(name=lead.name, email=lead.email, description=lead.description, created_by=request.user, team=at)
    lead.converted_to_client = True 
    lead.save()

    # convert comments as well
    # comments = lead.comments.all()
    # for comment in comments:
    #   Client_Comment.objects.create(
    #     content= comment.content, 
    #     client = client,
    #     created_by=comment.created_by,
    #     team = at
    #   )

    return Response(HTTP_200_OK)



@login_required
def convert_to_client(request, pk):
  lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
  at = Profile.objects.get(user=request.user).active_team



  client = Client.objects.create(name=lead.name, email=lead.email, description=lead.description, created_by=request.user, team=at)

  lead.converted_to_client = True 
  messages.success(request, 'Lead was converted to client')

  lead.save()

  # convert lead comment into client comment
  comments = lead.comments.all()
  for comment in comments:
    Client_Comment.objects.create(
      content= comment.content, 
      client = client,
      created_by=comment.created_by,
      team = team
    )
  return redirect('leads_list')



