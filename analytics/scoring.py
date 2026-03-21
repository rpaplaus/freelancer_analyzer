from sqlmodel import Session
from database.models import Job, JobScore

def compute_job_score(session: Session, job: Job) -> JobScore:
    """
    Computes a comprehensive score to decide if the freelancer should apply.
    """
    # 1. Budget Score
    budget_score = 0.0
    if job.budget_max and job.budget_max >= 50:
        budget_score = 3.0
    elif job.budget_min and job.budget_min >= 20:
        budget_score = 1.0

    # 2. Client Score
    client_score = 0.0
    if job.client:
        if job.client.total_spent and job.client.total_spent > 5000:
            client_score += 3.0
        if job.client.rating and job.client.rating >= 4.5:
            client_score += 1.0

    # 3. Competition Score
    competition_score = 0.0
    if job.proposals is not None:
        if job.proposals < 10:
            competition_score = 4.0
        elif job.proposals > 50:
            competition_score = -2.0

    # 4. Skill Match / Trend
    # For now, placeholder
    skill_match_score = 2.0

    final_score = budget_score + client_score + competition_score + skill_match_score

    score_entry = JobScore(
        job_id=job.id,
        budget_score=budget_score,
        client_score=client_score,
        competition_score=competition_score,
        skill_match_score=skill_match_score,
        final_score=final_score
    )
    session.add(score_entry)
    session.commit()
    session.refresh(score_entry)
    return score_entry
