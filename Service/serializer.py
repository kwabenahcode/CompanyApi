from .models import *
from rest_framework import serializers

class GetServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "service_name", "service_description", "service_image"]


class GetTopClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopClient
        fields = ["id", "name", "business_logo"]