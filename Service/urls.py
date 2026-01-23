from django.urls import path
from . import views 

urlpatterns = [
    path('services', views.GetServiceAPI.as_view(), name="services"),
    path('topclients', views.GetTopClientAPI.as_view(), name="topclients")

]