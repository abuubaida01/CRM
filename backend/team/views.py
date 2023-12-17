from django.shortcuts import render, get_object_or_404, redirect
from .models import Team 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TeamForm
from profiles.models import Profile

#====================================================
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.status import HTTP_200_OK
from .serializer import * 
from team.models import Team



class CreateTeamAPIView(ListCreateAPIView):
  serializer_class = TeamSerializer
  queryset = Team.objects.all()

  def post(self, request,*args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(HTTP_200_OK)
      

class UpdateTeamAPIView(RetrieveUpdateAPIView):
  serializer_class = TeamSerializer
  queryset = Team.objects.all()
  lookup_field = 'pk'

  def put(self, request, pk,*args, **kwargs):
    team = Team.objects.get(pk=pk)
    serializer = self.get_serializer(team, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(HTTP_200_OK)


class RetrieveTeamAPIView(RetrieveAPIView):
  serializer_class = TeamSerializer
  queryset = Team.objects.all()
  lookup_field = 'pk'


class ListTeamsAPIView(ListAPIView):
  serializer_class = TeamSerializer

  def get_queryset(self):
      return Team.objects.filter(created_by=self.request.user)
    

class ActivateTeam(APIView):
  
  def post(self, request, pk,*args, **kwargs):
    team = Team.objects.filter(members__in=[request.user]).get(pk=pk)
    profiles = Profile.objects.get(user=request.user)
    profiles.active_team = team
    profiles.save()
    return Response(HTTP_200_OK)


class CreatePlanAPIView(ListCreateAPIView):
  serializer_class = PlanSerializer
  queryset = Plan.objects.all()

  def post(self, request,*args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(HTTP_200_OK)


class UpdatePlanAPIView(RetrieveUpdateAPIView):
  serializer_class = PlanSerializer
  queryset = Plan.objects.all()

  def put(self, request, pk,*args, **kwargs):
    plan = Plan.objects.get(pk=pk) 
    serializer = self.get_serializer(plan, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(HTTP_200_OK)


class ListPlanAPIView(ListAPIView):
  serializer_class = PlanSerializer
  
  def get_queryset(self):
    return Plan.objects.filter(user=self.request.user)


class RetrievePlanAPIView(RetrieveAPIView):
  serializer_class = PlanSerializer
  queryset = Plan.objects.all()
  lookup_field = 'pk'


class DestroyPlanAPIView(RetrieveDestroyAPIView):
  serializer_class = PlanSerializer
  queryset = Plan.objects.all()
  lookup_field = 'pk'

