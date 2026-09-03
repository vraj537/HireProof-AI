import os,json,re,requests
def fallback(c):
 skills=len(c.skill_list()); ev=c.evidence.filter(verified=True).count(); score=min(98,35+min(35,skills*6)+min(20,float(c.experience_years)*5)+min(15,ev*5)); verdict="Strong Match" if score>=80 else ("Review" if score>=60 else "Needs Review")
 return int(score),verdict,f"Heuristic screening found {skills} listed skills, {c.experience_years:g} years experience and {ev} verified evidence item(s). Add stronger evidence or a complete resume for higher confidence."
def analyze_candidate(c):
 token=os.getenv("HF_TOKEN","").strip(); model=os.getenv("HF_MODEL","HuggingFaceTB/SmolLM2-1.7B-Instruct"); base=os.getenv("HF_API_URL","https://router.huggingface.co/hf-inference/models").rstrip("/")
 prompt=f"You are HireProof AI. Analyze only supplied evidence. Return strict JSON with score (0-100), verdict (Strong Match/Review/Needs Review), summary (under 60 words). Candidate: {c.name}; role: {c.role}; experience: {c.experience_years}; skills: {c.skills}; resume: {c.resume_text[:5000]}; verified evidence: {c.evidence.filter(verified=True).count()}."
 if not token: return fallback(c)
 try:
  r=requests.post(f"{base}/{model}",headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"},json={"inputs":prompt,"parameters":{"max_new_tokens":180,"temperature":0.2}},timeout=35); r.raise_for_status(); data=r.json(); text=data[0].get("generated_text","") if isinstance(data,list) else data.get("generated_text",""); m=re.search(r"\{.*\}",text,re.S)
  if m:
   o=json.loads(m.group(0)); return max(0,min(100,int(o.get("score",0)))),str(o.get("verdict","Review")),str(o.get("summary","AI analysis completed."))
 except Exception: pass
 return fallback(c)
def extract_resume_text(upload):
 if not upload:return ""
 try:
  n=upload.name.lower()
  if n.endswith(".pdf"):
   from pypdf import PdfReader; return "\n".join((p.extract_text() or "") for p in PdfReader(upload).pages)[:12000]
  if n.endswith(".docx"):
   from docx import Document; return "\n".join(p.text for p in Document(upload).paragraphs)[:12000]
  if n.endswith((".txt",".md")): return upload.read().decode("utf-8","ignore")[:12000]
 except Exception: pass
 return ""
