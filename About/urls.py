from django.urls import path
from . import views

urlpatterns = [
    path("founder", views.GetFounderAPI.as_view(), name="founder"),
    path("about_us", views.GetAboutAPI.as_view(), name="about_us"),
    path("trusted_companies", views.GetTrustedCompaniesAPI.as_view(), name="trusted_companies"),
    path("dev_team", views.GetDevTeamAPI.as_view(), name="dev_team")
]