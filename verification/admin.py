from django.contrib import admin
from .models import VerificationResult


@admin.register(VerificationResult)
class VerificationResultAdmin(admin.ModelAdmin):
    list_display = ("resume", "verdict", "evidence_score", "consistency_score", "created_at")
    list_filter = ("verdict",)
