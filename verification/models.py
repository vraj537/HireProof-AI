from django.db import models
class Candidate(models.Model):
 STATUS=[("pending","Pending"),("verified","Verified"),("review","Needs Review"),("rejected","Rejected")]
 name=models.CharField(max_length=150); email=models.EmailField(); role=models.CharField(max_length=150); location=models.CharField(max_length=120,blank=True)
 skills=models.TextField(blank=True); experience_years=models.DecimalField(max_digits=4,decimal_places=1,default=0)
 resume_text=models.TextField(blank=True)
 resume_file_data=models.BinaryField(blank=True,null=True); resume_file_name=models.CharField(max_length=255,blank=True); resume_content_type=models.CharField(max_length=100,blank=True)
 ai_score=models.PositiveIntegerField(default=0); ai_verdict=models.CharField(max_length=30,default="Pending"); ai_summary=models.TextField(blank=True)
 status=models.CharField(max_length=20,choices=STATUS,default="pending"); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 def skill_list(self): return [s.strip() for s in self.skills.split(",") if s.strip()]
 def __str__(self): return f"{self.name} — {self.role}"
class Evidence(models.Model):
 TYPES=[("education","Education"),("employment","Employment"),("project","Project"),("certificate","Certificate"),("identity","Identity")]
 candidate=models.ForeignKey(Candidate,on_delete=models.CASCADE,related_name="evidence"); evidence_type=models.CharField(max_length=30,choices=TYPES)
 title=models.CharField(max_length=200); source_url=models.URLField(blank=True); notes=models.TextField(blank=True); verified=models.BooleanField(default=False); created_at=models.DateTimeField(auto_now_add=True)
