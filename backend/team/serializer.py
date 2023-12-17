from rest_framework import serializers
from .models import *


class PlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = Plan
    fields = "__all__"



class TeamSerializer(serializers.ModelSerializer):
  class Meta:
    model=Team 
    fields ="__all__"

