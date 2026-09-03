from django.contrib import admin
from .models import Candidate,Evidence
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin): list_display=("name","role","ai_score","status","created_at"); search_fields=("name","email","role"); list_filter=("status","ai_verdict")
@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin): list_display=("title","candidate","evidence_type","verified"); list_filter=("evidence_type","verified")
