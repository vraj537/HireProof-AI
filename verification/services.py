"""Evidence-based resume verification using Hugging Face Inference API."""
import json
import re
import requests
from django.conf import settings

CLAIM_LABELS = [
    "consistent and credible professional experience",
    "exaggerated or inflated claims",
    "vague or unverifiable claims",
    "contradictory statements",
]

RED_FLAG_PATTERNS = [
    (r"\b(ninja|guru|rockstar)\b", "Buzzword overuse without concrete evidence"),
    (r"\b(\d{2,})\+?\s*years?\b", "Unusually high experience claim - verify against timeline"),
    (r"\bexpert\b.{0,20}\ball\b", "Overly broad expertise claim"),
]


def _call_huggingface(text: str) -> dict:
    """Call HF zero-shot-classification inference endpoint to score claim credibility."""
    if not settings.HUGGINGFACE_API_KEY:
        return {"error": "missing_api_key"}

    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
    payload = {"inputs": text[:2000], "parameters": {"candidate_labels": CLAIM_LABELS}}
    try:
        resp = requests.post(settings.HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as exc:
        return {"error": str(exc)}


def _rule_based_flags(text: str) -> list:
    flags = []
    for pattern, message in RED_FLAG_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            flags.append(message)
    return flags


def verify_resume_text(text: str) -> dict:
    """Return an evidence-based verification dict for the given resume text."""
    hf_result = _call_huggingface(text)
    flags = _rule_based_flags(text)

    scores_by_label = {}
    if isinstance(hf_result, dict) and "labels" in hf_result and "scores" in hf_result:
        scores_by_label = dict(zip(hf_result["labels"], hf_result["scores"]))

    credible_score = scores_by_label.get("consistent and credible professional experience", 0.5)
    exaggeration = scores_by_label.get("exaggerated or inflated claims", 0.0)
    contradiction = scores_by_label.get("contradictory statements", 0.0)

    evidence_score = round(credible_score * 100, 2)
    consistency_score = round((1 - contradiction) * 100, 2)

    if flags:
        evidence_score = max(0, evidence_score - (10 * len(flags)))

    if evidence_score >= 70 and not flags:
        verdict = "credible"
    elif evidence_score < 40 or contradiction > 0.5:
        verdict = "suspicious"
    else:
        verdict = "needs_review"

    summary_parts = [f"Credibility score: {evidence_score}/100."]
    if exaggeration:
        summary_parts.append(f"Exaggeration likelihood: {round(exaggeration * 100, 1)}%.")
    if flags:
        summary_parts.append(f"{len(flags)} rule-based flag(s) detected.")
    if hf_result.get("error"):
        summary_parts.append(f"AI model note: {hf_result['error']} (fell back to rule-based scoring).")

    return {
        "evidence_score": evidence_score,
        "consistency_score": consistency_score,
        "verdict": verdict,
        "ai_summary": " ".join(summary_parts),
        "flags": flags,
        "model_used": settings.HUGGINGFACE_RESUME_MODEL,
        "raw": hf_result,
    }
