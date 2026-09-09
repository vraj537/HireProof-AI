from django.urls import path
from . import views

app_name = "verification"

urlpatterns = [
    path("resume/<int:resume_id>/", views.result, name="result"),
]
