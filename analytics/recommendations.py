from sqlmodel import Session, select
from database.models import Job, JobScore

def get_best_jobs(session: Session, limit: int = 20):
    """
    Returns the top jobs sorted by highest final score.
    """
    statement = select(Job).join(JobScore).order_by(JobScore.final_score.desc()).limit(limit)
    return session.exec(statement).all()

def get_low_competition(session: Session, limit: int = 20):
    statement = select(Job).join(JobScore).where(JobScore.competition_score >= 3.0).order_by(JobScore.final_score.desc()).limit(limit)
    return session.exec(statement).all()

def get_hidden_gems(session: Session):
    # Hidden gems: High budget, low proposals, good client score
    statement = select(Job).join(JobScore).where(
        JobScore.budget_score >= 2.0,
        JobScore.competition_score >= 3.0,
        JobScore.client_score >= 2.0
    )
    return session.exec(statement).all()
