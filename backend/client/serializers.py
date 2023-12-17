from rest_framework import serializers
from .models import Client, ClientFile, Comment

class ClientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Client
    fields = ('name', 'email', 'description',)
    # read_only_fields = ('created_by', )


class ClientFileSerializer(serializers.ModelSerializer):
  class Meta:
    model = ClientFile
    fields = ('team', 'client', 'file', 'created_by')


class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ('content',)
