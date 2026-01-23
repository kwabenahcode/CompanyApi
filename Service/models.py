from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Service(models.Model):
    service_name = models.CharField(max_length=225)
    service_description = RichTextField()
    service_image = models.ImageField(upload_to="service/",  blank=True, null=True)

    def __str__(self):
        return self.service_name

class TopClient(models.Model):
    name = models.CharField(max_length=225)
    business_logo = models.ImageField(upload_to="topclient/", blank=True, null=True)
