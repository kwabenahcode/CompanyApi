from django.db import models

# Create your models here.
class Service(models.Model):
    service_name = models.CharField(max_length=225)
    service_description = models.TextField()
    service_image = models.ImageField(upload_to="service/",  blank=True, null=True)

    def __str__(self):
        return self.service_name

class TopClient(models.Model):
    name = models.CharField(max_length=225)
    business_logo = models.ImageField(upload_to="topclient/", blank=True, null=True)
