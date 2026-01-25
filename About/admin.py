from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Founder)

from .models import About

class AboutAdmin(admin.ModelAdmin):
    # Show only first 100 characters in list view
    list_display = ('preview_about',)
    
    # Add search capability
    search_fields = ('about_us',)
    
    # Add a custom method to display preview
    def preview_about(self, obj):
        import re
        text_only = re.sub('<[^<]+?>', '', obj.about_us)
        return f"{text_only[:50]}..." if len(text_only) > 50 else text_only
        # return obj.about_us[:100] + "..." if len(obj.about_us) > 100 else obj.about_us
    preview_about.short_description = "About Preview"
admin.site.register(About, AboutAdmin)

admin.site.register(TrustedBy)
admin.site.register(DevTeam)
