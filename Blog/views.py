from django.shortcuts import render

from .models import *
from .serializer import GetAllBlogsSerializer, GetFeaturedBlogsSerializer, GetDetailedBlogSerializer
from rest_framework import generics
from rest_framework.response import Response
# Create your views here.

class GetFeaturedBlogAPI(generics.GenericAPIView):
    serializer_class = GetFeaturedBlogsSerializer

    def get(self, request):
        featuredblogs = FeaturedBlog.objects.all()
        serializer = self.serializer_class(featuredblogs, many=True)
        return Response({"featuredblogs": serializer.data}, status=200)
    
class GetAllBlogsAPI(generics.GenericAPIView):
    serializer_class = GetAllBlogsSerializer

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = self.serializer_class(blogs, many=True)
        return Response({"blogs":serializer.data}, status=200)
    
class GetDetailedBlogAPI(generics.GenericAPIView):
    serializer_class = GetDetailedBlogSerializer

    def get(self, request, *args, **kwargs):
        try:
            slug = kwargs.get("slug")
            if slug:
                blog = Blog.objects.get(slug=slug)
                serializer = self.serializer_class(blog, many=False)
                return Response({"blog":serializer.data})
            else:
                return Response({"status":"failed", "message":"No slug match the query"})

        except Exception as e:
            pass


    