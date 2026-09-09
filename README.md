# HireProof-AI

**Evidence-Based AI Candidate Verification & Hiring Intelligence Platform**

HireProof-AI is a Django-based platform that verifies candidate resumes using AI. It scores every resume for consistency and credibility, flags exaggerated or vague claims, and gives recruiters an evidence-based verdict instead of gut-feel hiring.

## Features

- Candidate registration & profile management
- Resume upload (PDF / DOCX / TXT) with automatic text extraction
- AI-powered credibility scoring via Hugging Face zero-shot classification
- Rule-based red-flag detection (buzzwords, inflated experience, vague claims)
- Evidence Score + Consistency Score + Verdict (Credible / Needs Review / Suspicious)
- Recruiter-style dashboard to track every candidate's verification history
- Django admin for full backend management

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python + Django |
| Database | PostgreSQL (Neon) |
| AI | Hugging Face Inference API |
| Frontend | HTML5, CSS3, Bootstrap (Educavo template, customized) |
| Deployment | Vercel |
| Static Files | WhiteNoise |

## Local Setup

```bash
git clone <repo-url>
cd hireproof-ai
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env          # fill in your keys
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Environment Variables

See `.env.example`:

- `SECRET_KEY` — Django secret key
- `DEBUG` — `True` locally, `False` in production
- `ALLOWED_HOSTS` — comma separated hosts
- `DATABASE_URL` — Neon Postgres connection string
- `HUGGINGFACE_API_KEY` — Hugging Face inference API token
- `HUGGINGFACE_RESUME_MODEL` — model used for zero-shot claim scoring (default `facebook/bart-large-mnli`)

## Deployment (Vercel + Neon)

1. Create a Postgres database on [Neon](https://neon.tech), copy the connection string into `DATABASE_URL`.
2. Push this repo to GitHub.
3. Import the repo in [Vercel](https://vercel.com) — it auto-detects `vercel.json` and `build_files.sh`.
4. Add all `.env.example` variables under Vercel Project → Settings → Environment Variables.
5. Deploy. Vercel runs migrations and `collectstatic` automatically via `build_files.sh`.

## How Verification Works

1. Candidate uploads a resume.
2. Text is extracted (`pypdf` / `python-docx`).
3. Text is sent to the Hugging Face zero-shot-classification endpoint against credibility labels.
4. Rule-based checks scan for buzzwords, inflated experience, and vague/contradictory phrasing.
5. Scores are combined into an **Evidence Score**, **Consistency Score**, and a final **Verdict**.
6. Result is saved and shown on the candidate's dashboard.

If no Hugging Face API key is set, the system automatically falls back to rule-based scoring only, so the app never breaks.

## Project Structure

```
hireproof/       # project settings, urls, wsgi
core/            # landing page
accounts/        # login / register / logout
candidates/      # profile, resume upload, dashboard
verification/    # AI verification engine + result view
templates/        # HTML templates (Educavo-based UI)
static/           # css, js, fonts, images
```

---
Built by Vraj.
