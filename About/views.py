from django.shortcuts import render
from .serializer import *
from .models import *
from rest_framework import generics
from rest_framework.response import Response

# Create your views here.
class GetFounderAPI(generics.GenericAPIView):
    serializer_class = GetFounderSerializer

    def get(self, request, *args, **kwargs):
        founder = Founder.objects.all()
        serializer = self.serializer_class(founder, many=True)
        return Response({"founder":serializer.data}, status=200)

class GetAboutAPI(generics.GenericAPIView):
    serializer_class = GetAboutUsSerializer

    def get(self, request, *args, **kwargs):
        about_us = About.objects.all()
        serializer = self.serializer_class(about_us, many=True)
        return Response({"about_us":serializer.data}, status=200)
    
class GetTrustedCompaniesAPI(generics.GenericAPIView):
    serializer_class = GetTrustedCompaniesSerializer

    def get(self, request, *args, **kwargs):
        business_name = TrustedBy.objects.all()
        serializer = self.serializer_class(business_name, many=True)
        return Response({"companies": serializer.data}, status=200)
    
class GetDevTeamAPI(generics.GenericAPIView):
    serializer_class = GetDevTeamSerializer

    def get(self, request, *args, **kwargs):
        devteam = DevTeam.objects.all()
        serializer = self.serializer_class(devteam, many=True)
        return Response({"devteam": serializer.data}, status=200)