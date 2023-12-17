from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, ClientFile, Comment
from .forms import AddClientForm, CommentForm, ClientFileForm
from django.contrib import messages
import csv
from .serializers import ClientSerializer, ClientFileSerializer, CommentSerializer
from team.models import Team

#====================================================
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.status import HTTP_200_OK



class ClientListAPIView(ListAPIView):
  serializer_class = ClientSerializer
  # permission_classes = [IsAuthenticated]
  def get_queryset(self):
      return Client.objects.filter(created_by=self.request.user)


class CDetailExportAPI(APIView):
  def get(self, request, *args, **kwargs):
    clients = Client.objects.filter(created_by=self.request.user)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="clients.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["Client", "Description", "Created_at", "Created_by"])

    for client in clients:
      writer.writerow([client.name, client.description, client.created_at, client.created_by])
      
    return response


class AttachFileWithClient(CreateAPIView):
  serializer_class = ClientFileSerializer
  model = ClientFile

  def post(self, request, pk, *args, **kwargs):
    client = get_object_or_404(Client, created_by=self.request.user, pk=pk)
    active_team = Profile.objects.get(user=request.user).active_team
    serializer =  self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(HTTP_200_OK)


class ClientDetailAPIView(RetrieveAPIView):
  model = Client
  serializer_class = ClientSerializer
  lookup_field = 'pk'
  queryset = Client.objects.all()


class CommentAPIView(ListCreateAPIView):
  serializer_class = CommentSerializer
  queryset = Comment.objects.all()

  def post(self, request, *args, **kwargs):
    client = get_object_or_404(Client, created_by=request.user, pk=self.kwargs['pk'])
    at = Profile.objects.get(user=request.user).active_team
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(team=at, client=client, created_by=self.request.user)
    return Response(HTTP_200_OK)



class AddClientAPIView(CreateAPIView):
  serializer_class = ClientSerializer

  def post(self, request,*args, **kwargs):
    at = Profile.objects.get(user=request.user).active_team
    serializer = ClientSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(created_by=self.request.user, team=at)
    return Response(HTTP_200_OK)



class UpdateClientAPIView(RetrieveUpdateAPIView):
  serializer_class = ClientSerializer
  queryset = Client.objects.all()
  lookup_field = 'pk'

  def patch(self, request, pk ,*args, **kwargs):
    client = Client.objects.get(pk=pk, created_by=self.request.user)
    serializer = self.get_serializer(client, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(HTTP_200_OK) 
  


class DestroyClientAPIView(RetrieveDestroyAPIView):
  serializer_class = ClientSerializer
  lookup_field = 'pk'
  queryset = Client.objects.all()


