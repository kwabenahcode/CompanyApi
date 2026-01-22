from django.db import models

# Create your models here.
class Value(models.Model):
    title = models.CharField(max_length=200, blank=True, )
    content = models.TextField(blank=True, )

    def __str__(self):
        return self.title
    
class Testimonial(models.Model):
    client_name = models.CharField(max_length=150, blank=True)
    client_message = models.TextField(blank=True)
    job_title = models.CharField(max_length=225)

    def __str__(self):
        return f"{self.client_name} the {self.job_title}"



