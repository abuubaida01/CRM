from rest_framework.serializers import ModelSerializer, Serializer
from .models import Profile

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
