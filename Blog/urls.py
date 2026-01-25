from django.urls import path
from . import views

urlpatterns = [
    path("featured_blogs", views.GetFeaturedBlogAPI.as_view(), name="featured_blogs"),
    path("blogs", views.GetAllBlogsAPI.as_view(), name="blogs"),
    path("blog/<slug:slug>", views.GetDetailedBlogAPI.as_view(), name="detailed_blog")
]