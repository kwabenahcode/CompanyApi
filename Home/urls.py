from django.urls import path
from . import views

urlpatterns = [
    path("oforitech_values", views.GetValuesAPI.as_view(), name="oforitech_values"),
    path("testimonials", views.GetTestimonialsAPI.as_view(), name="testimonials"),
]