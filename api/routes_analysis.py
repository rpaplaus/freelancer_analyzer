from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.db import get_session

router = APIRouter()

@router.get("/trends")
def get_trends(session: Session = Depends(get_session)):
    return {"message": "Trends endpoint pending implementation"}
