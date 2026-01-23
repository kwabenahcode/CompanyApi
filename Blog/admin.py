# admin.py
from django.contrib import admin
from .models import Blog, FeaturedBlog  # Explicit imports, NOT *

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'blog_category', 'created_at', 'content_preview')
    list_filter = ('created_at', 'blog_category')
    search_fields = ('blog_title', 'content')
    prepopulated_fields = {'slug': ('blog_title',)}  # Auto-generate slug
    
    def content_preview(self, obj):
        # Strip HTML tags for preview
        import re
        text_only = re.sub('<[^<]+?>', '', obj.content)
        return f"{text_only[:50]}..." if len(text_only) > 50 else text_only
    content_preview.short_description = "Content Preview"


@admin.register(FeaturedBlog)
class FeaturedBlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured_date')
    list_filter = ('featured_date',)  # Note: tuple needs trailing comma
    search_fields = ('name', 'description')
    
    # If you want to show the link in admin
    # def link_display(self, obj):
    #     return obj.link[:50] + "..." if len(obj.link) > 50 else obj.link
    # link_display.short_description = "Link"