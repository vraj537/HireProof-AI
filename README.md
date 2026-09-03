# HireProof-AI

Evidence-Based AI Candidate Verification & Hiring Intelligence Platform.

## Stack
- Python + Django
- Neon PostgreSQL
- Hugging Face Inference API
- Educavo frontend theme (only the CSS/JS/images required by HireProof pages are included)
- Vercel deployment

## Run
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Set `DATABASE_URL`, `DJANGO_SECRET_KEY`, `HF_TOKEN`, `HF_MODEL`, and `CSRF_TRUSTED_ORIGINS` in `.env`.
