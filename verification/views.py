from django.contrib import messages
from django.shortcuts import get_object_or_404,redirect,render
from .models import Candidate
from .forms import CandidateForm,EvidenceForm
from .services import analyze_candidate,extract_resume_text
def dashboard(request):
 qs=Candidate.objects.all(); total=qs.count(); verified=qs.filter(status="verified").count(); review=qs.filter(status="review").count(); avg=round(sum(c.ai_score for c in qs)/total) if total else 0; return render(request,"verification/dashboard.html",{"total":total,"verified":verified,"review":review,"avg":avg,"recent":qs.order_by("-created_at")[:6],"stat_items":[("Candidates",total),("Verified",verified),("Needs Review",review),("Average AI Score",f"{avg}%")],"features":[("assets/images/features/icon/3.png","Resume Intelligence","Extract candidate context"),("assets/images/features/icon/2.png","Evidence Profiles","Attach verifiable proof"),("assets/images/features/icon/1.png","Explainable AI","Get an evidence-based signal")]})
def candidates(request):
 q=request.GET.get("q","").strip(); qs=Candidate.objects.all().order_by("-created_at")
 if q: qs=qs.filter(name__icontains=q)|qs.filter(role__icontains=q)|qs.filter(email__icontains=q)
 return render(request,"verification/candidates.html",{"candidates":qs,"q":q})
def candidate_new(request):
 form=CandidateForm(request.POST or None,request.FILES or None)
 if form.is_valid():
  c=form.save(commit=False); c.resume_text=extract_resume_text(form.cleaned_data.get("resume")); c.save(); messages.success(request,"Candidate added. Run AI analysis to generate a verification score."); return redirect("candidate_detail",c.pk)
 return render(request,"verification/candidate_form.html",{"form":form})
def candidate_detail(request,pk): return render(request,"verification/candidate_detail.html",{"candidate":get_object_or_404(Candidate,pk=pk),"evidence_form":EvidenceForm()})
def analyze(request,pk):
 c=get_object_or_404(Candidate,pk=pk); score,verdict,summary=analyze_candidate(c); c.ai_score=score;c.ai_verdict=verdict;c.ai_summary=summary;c.status="verified" if score>=80 else ("review" if score>=60 else "rejected");c.save(); messages.success(request,"AI verification updated."); return redirect("candidate_detail",pk)
def add_evidence(request,pk):
 c=get_object_or_404(Candidate,pk=pk); form=EvidenceForm(request.POST)
 if form.is_valid(): e=form.save(commit=False);e.candidate=c;e.save();messages.success(request,"Evidence added.")
 return redirect("candidate_detail",pk)
