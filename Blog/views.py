from django.shortcuts import render

from .models import *
from .serializer import *
from rest_framework import generics
from rest_framework.response import Response
# Create your views here.

class GetFeaturedBlogAPI(generics.GenericAPIView):
    serializer_class = True

    def get(self, request):
        featuredblogs = FeaturedBlog.objects.all()
        serializer = self.serializer_class(featuredblogs, many=True)
        return Response({"featuredblogs": serializer.data}, status=200)
    
class GetAllBlogsAPI(generics.GenericAPIView):
    serializer_class = True

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = self.serializer_class(blogs, many=True)
        return Response({"blogs":serializer.data}, status=200)
    
class GetDetailedBlogAPI(generics.GenericAPIView):
    serializer_class = True

    def get(self, request):
        blog = Blog.objects.get(id=id)
        serializer = self.serializer_class


    