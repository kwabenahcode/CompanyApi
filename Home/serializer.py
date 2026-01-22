from rest_framework import serializers
from .models import *

class GetValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ["title", "content"]


class GetTestimonialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["client_name", "client_message", "job_title"]