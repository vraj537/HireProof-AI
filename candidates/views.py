from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from verification.models import VerificationResult
from verification.services import verify_resume_text

from .forms import CandidateProfileForm, ResumeUploadForm
from .models import CandidateProfile, Resume
from .utils import extract_text


@login_required
def dashboard(request):
    profile, _ = CandidateProfile.objects.get_or_create(
        user=request.user, defaults={"full_name": request.user.get_full_name() or request.user.username}
    )
    resumes = profile.resumes.select_related("verification").order_by("-uploaded_at")
    return render(request, "candidates/dashboard.html", {"profile": profile, "resumes": resumes})


@login_required
def edit_profile(request):
    profile, _ = CandidateProfile.objects.get_or_create(
        user=request.user, defaults={"full_name": request.user.get_full_name() or request.user.username}
    )
    if request.method == "POST":
        form = CandidateProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("candidates:dashboard")
    else:
        form = CandidateProfileForm(instance=profile)
    return render(request, "candidates/edit_profile.html", {"form": form})


@login_required
def upload_resume(request):
    profile, _ = CandidateProfile.objects.get_or_create(
        user=request.user, defaults={"full_name": request.user.get_full_name() or request.user.username}
    )
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.candidate = profile
            resume.status = "processing"
            resume.save()

            try:
                text = extract_text(resume.file)
            except Exception:
                text = ""
            resume.raw_text = text

            result = verify_resume_text(text)
            VerificationResult.objects.update_or_create(
                resume=resume,
                defaults={
                    "evidence_score": result["evidence_score"],
                    "consistency_score": result["consistency_score"],
                    "verdict": result["verdict"],
                    "ai_summary": result["ai_summary"],
                    "flags": result["flags"],
                    "model_used": result["model_used"],
                },
            )
            resume.status = "verified" if result["verdict"] != "suspicious" else "flagged"
            resume.save()

            messages.success(request, "Resume uploaded and verified.")
            return redirect("verification:result", resume_id=resume.id)
    else:
        form = ResumeUploadForm()
    return render(request, "candidates/upload_resume.html", {"form": form})
