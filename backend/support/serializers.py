from rest_framework.serializers import ModelSerializer
from .models import *

class Sugg2SaviorSerializer(ModelSerializer):
  class Meta:
    model = Sugg2Savior
    fields = "__all__"


class ReportUserSerializer(ModelSerializer):
  class Meta:
    model = ReportUser
    fields = "__all__"

