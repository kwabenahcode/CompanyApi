from rest_framework import serializers
from .models import FeaturedBlog, Blog

class GetFeaturedBlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedBlog
        fields = ["id", "name", "description", "link", "image", "featured_date"]

class GetAllBlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields = ["id", "blog_title", "content", "blog_category","blog_image", "slug", "description" ]

class GetDetailedBlogSerializer(serializers.ModelSerializer):
    related_blogs = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ["id", "blog_title", "content", "blog_category","blog_image", "created_at", "slug", "related_blogs"]

    def get_related_blogs(self, blog):
        related_blogs = Blog.objects.filter(blog_category=blog.blog_category).exclude(id=blog.id)
        serializer =  GetAllBlogsSerializer(related_blogs, many=True)
        return serializer.data





