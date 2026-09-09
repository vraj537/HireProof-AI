from django.db import models
from candidates.models import Resume


class VerificationResult(models.Model):
    VERDICT_CHOICES = [
        ("credible", "Credible"),
        ("needs_review", "Needs Review"),
        ("suspicious", "Suspicious"),
    ]

    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name="verification")
    evidence_score = models.FloatField(default=0.0, help_text="0-100 evidence-based credibility score")
    consistency_score = models.FloatField(default=0.0, help_text="0-100 internal consistency of claims")
    verdict = models.CharField(max_length=20, choices=VERDICT_CHOICES, default="needs_review")
    ai_summary = models.TextField(blank=True, help_text="Hugging Face model output / explanation")
    flags = models.JSONField(default=list, blank=True, help_text="List of specific red flags found")
    model_used = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resume} -> {self.verdict}"
