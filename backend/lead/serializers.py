from rest_framework.serializers import ModelSerializer
from .models import *


class LeadSerializer(ModelSerializer):
  class Meta:
    model = Lead 
    fields = ('created_by',
    'created_at',
    'modified_at',
    'priority',
    'status',
    'name',
    'email',
    'description',
    'converted_to_client',
    'team',)
    # fields = ('priority', 'status', 'name', 'email', 'description', 'converted_to_client',)


class LeadFileSerializer(ModelSerializer):
  class Meta:
    model = LeadFile 
    fields = "__all__"



class CommentSerializer(ModelSerializer):
  class Meta:
    model = Comment
    fields = "__all__"
