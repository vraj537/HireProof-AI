from django.contrib import admin
from .models import CandidateProfile, Resume


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "current_role", "years_experience")
    search_fields = ("full_name", "user__username")


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job_title_applied", "status", "uploaded_at")
    list_filter = ("status",)
