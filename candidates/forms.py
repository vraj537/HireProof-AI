from django import forms
from .models import CandidateProfile, Resume


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ["full_name", "phone", "current_role", "years_experience", "linkedin_url", "github_url"]


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["file", "job_title_applied"]
