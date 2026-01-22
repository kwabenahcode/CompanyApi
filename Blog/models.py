from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class FeaturedBlog(models.Model):
    name = models.CharField(max_length=225)
    description = RichTextField(blank=True)
    link = models.URLField(max_length=1000, blank=True)
    image = models.ImageField(upload_to="featuredblogs/", blank=True, null=True)


class Blog(models.Model):
    blog_category = models.CharField(max_length=255)
    blog_name = models.CharField(max_length=255)
    blog_image = models.ImageField(upload_to="blogs/", blank=True, null=True)