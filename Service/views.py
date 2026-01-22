from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework import generics
from rest_framework.response import Response

# Create your views here.
class GetServiceAPI(generics.GenericAPIView):
    serializer_class = GetServiceSerializer

    def get(self):
        services = Service.objects.all()
        serializer = self.serializer_class(services, many=True)
        return Response({"services":serializer.data}, status=200)
    

class GetTopClientAPI(generics.GenericAPIView):
    serializer_class = GetTopClientSerializer

    def get(self):
        topclients = TopClient.objects.all()
        serializer = self.serializer_class(topclients, many=True)
        return Response({"topclients": serializer.data}, status=200)
