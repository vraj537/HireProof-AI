"""Text extraction helpers for uploaded resumes."""
from pypdf import PdfReader
from docx import Document


def extract_text(file_field) -> str:
    name = file_field.name.lower()
    file_field.open()
    try:
        if name.endswith(".pdf"):
            reader = PdfReader(file_field)
            return "\n".join((page.extract_text() or "") for page in reader.pages)
        if name.endswith(".docx"):
            doc = Document(file_field)
            return "\n".join(p.text for p in doc.paragraphs)
        return file_field.read().decode("utf-8", errors="ignore")
    finally:
        file_field.close()
