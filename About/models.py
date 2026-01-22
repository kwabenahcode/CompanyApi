from django.db import models

# Create your models here.
class Founder(models.Model):
    founder_name = models.CharField(max_length=225)
    founder_title = models.CharField(max_length=225)
    founder_story = models.TextField()
    founder_image = models.ImageField(upload_to="founder/",  blank=True, null=True)

    def __str__(self):
        return self.founder_name
    

class About(models.Model):
    about_us = models.TextField(blank=True)

    def __str__(self):
        return self.about_us[:10] 

class TrustedBy(models.Model):
    business_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.business_name

class DevTeam(models.Model):
    name = models.CharField(max_length=225, blank=True)
    job_title = models.CharField(max_length=225, blank=True)
    image = models.ImageField(upload_to="devteam/",  blank=True, null=True)
