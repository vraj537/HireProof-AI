from django.conf import settings
from django.db import models


def resume_upload_path(instance, filename):
    return f"resumes/{instance.candidate.user.username}/{filename}"


class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="candidate_profile")
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    current_role = models.CharField(max_length=150, blank=True)
    years_experience = models.PositiveSmallIntegerField(default=0)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Resume(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("verified", "Verified"),
        ("flagged", "Flagged"),
        ("failed", "Failed"),
    ]

    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name="resumes")
    file = models.FileField(upload_to=resume_upload_path)
    job_title_applied = models.CharField(max_length=150, blank=True)
    raw_text = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.uploaded_at:%Y-%m-%d}"
