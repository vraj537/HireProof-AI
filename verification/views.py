from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from candidates.models import Resume


@login_required
def result(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, candidate__user=request.user)
    verification = getattr(resume, "verification", None)
    return render(request, "verification/result.html", {"resume": resume, "verification": verification})
