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
        serializer = self.serializer_class(founder, many=False)
        return Response({"founder":serializer.data}, status=200)
    