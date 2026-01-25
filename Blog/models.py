# models.py
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class Blog(models.Model):
    blog_category = models.CharField(max_length=255)
    blog_title = models.CharField(max_length=255)
    blog_image = models.ImageField(upload_to="blogs/", blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blog_title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.blog_title)
            unique_slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class FeaturedBlog(models.Model):
    name = models.CharField(max_length=225)
    description = RichTextField(blank=True)
    link = models.URLField(max_length=1000, blank=True)
    image = models.ImageField(upload_to="featuredblogs/", blank=True, null=True)
    featured_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name