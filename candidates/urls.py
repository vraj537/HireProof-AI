from django.urls import path
from . import views

app_name = "candidates"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("resume/upload/", views.upload_resume, name="upload_resume"),
]
