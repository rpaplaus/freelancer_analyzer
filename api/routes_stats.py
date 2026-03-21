from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.db import get_session

router = APIRouter()

@router.get("/")
def get_summary_stats(session: Session = Depends(get_session)):
    return {"message": "Stats endpoint pending implementation"}
