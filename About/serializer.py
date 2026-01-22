from rest_framework import serializers
from .models import *

class GetFounderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Founder
        fields = ["id", "founder_name", "founder_story", "founder_title", "founder_image"]


class GetAboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ["id", "about_us"]

class GetTrustedCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustedBy
        fields = ["id", "business_name"]

class GetDevTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevTeam
        fields = ["id", "name", "job_title", "image"]