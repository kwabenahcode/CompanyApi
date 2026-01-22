from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializer import *

# Create your views here.
class GetValuesAPI(generics.GenericAPIView):
    serializer_class = GetValueSerializer

    def get(self, request, *args, **kwargs):
        values = Value.objects.all()
        serializer = self.serializer_class(values, many=True)
        return Response({"value": serializer.data}, status=200)


class GetTestimonialsAPI(generics.GenericAPIView):
    serializer_class = GetTestimonialsSerializer

    def get(self, request, *args, **kwargs):
        testimonials = Testimonial.objects.all()
        serializer = self.serializer_class(testimonials, many=True) 
        return Response({"testimonials":serializer.data}, status=200)



    