from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database.db import get_session
from database.models import Job, AnalysisResult

router = APIRouter()

@router.get("/jobs")
def get_jobs(skip: int = 0, limit: int = 20, session: Session = Depends(get_session)):
    jobs = session.exec(select(Job).offset(skip).limit(limit)).all()
    return jobs

@router.get("/jobs/{job_id}")
def get_job(job_id: int, session: Session = Depends(get_session)):
    job = session.exec(select(Job).where(Job.id == job_id)).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    analysis = session.exec(select(AnalysisResult).where(AnalysisResult.job_id == job_id)).first()
    
    return {
        "job": job,
        "analysis": analysis.result if analysis else None
    }
