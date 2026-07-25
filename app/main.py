from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import init_db, get_db
from app.models import MatchHistory
from app.pdf_utils import extract_text_from_pdf
from app.matcher import analyze

app = FastAPI(title="ATS Resume Matcher", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: str = Form(None),
    db: Session = Depends(get_db),
):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported.")
    file_bytes = await resume.read()
    resume_text = extract_text_from_pdf(file_bytes)
    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from this PDF.")
    result = analyze(resume_text, job_description)
    record = MatchHistory(
        resume_filename=resume.filename,
        job_title=job_title,
        score=result["score"],
        verdict=result["verdict"],
        missing_keywords=", ".join(result["missing_keywords"]),
    )
    db.add(record)
    db.commit()
    return result

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(MatchHistory).order_by(MatchHistory.created_at.desc()).limit(20).all()
    return [{"id": r.id, "resume_filename": r.resume_filename, "job_title": r.job_title,
             "score": r.score, "verdict": r.verdict,
             "missing_keywords": r.missing_keywords.split(", ") if r.missing_keywords else [],
             "created_at": r.created_at.isoformat()} for r in records]

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")
