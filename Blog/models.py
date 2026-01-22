from django.db import models

# Create your models here.
class FeaturedBlog(models.Model):
    name = models.CharField(max_length=225)