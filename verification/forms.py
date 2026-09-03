from django import forms
from .models import Candidate,Evidence
class CandidateForm(forms.ModelForm):
 class Meta:
  model=Candidate; fields=["name","email","role","location","skills","experience_years","resume"]
  widgets={k:forms.TextInput(attrs={"class":"form-control"}) for k in ["name","email","role","location","skills","experience_years"]}
  widgets["skills"]=forms.TextInput(attrs={"class":"form-control","placeholder":"Python, Django, PostgreSQL, AI"})
  widgets["resume"]=forms.ClearableFileInput(attrs={"class":"form-control","accept":".pdf,.docx,.txt,.md"})
class EvidenceForm(forms.ModelForm):
 class Meta:
  model=Evidence; fields=["evidence_type","title","source_url","notes","verified"]
  widgets={"evidence_type":forms.Select(attrs={"class":"form-control"}),"title":forms.TextInput(attrs={"class":"form-control"}),"source_url":forms.URLInput(attrs={"class":"form-control"}),"notes":forms.Textarea(attrs={"class":"form-control","rows":3}),"verified":forms.CheckboxInput(attrs={"class":"form-check-input"})}
