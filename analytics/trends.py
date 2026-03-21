from sqlmodel import Session, select
from collections import defaultdict
from datetime import datetime, timedelta
from database.models import SkillTrend, JobSkillLink, Skill, Job

def update_skill_trends(session: Session):
    """
    Calculates job counts and average budgets for skills.
    Updates the skill_trends table with an execution snapshot.
    """
    print("Aggregating macro skill trends...")
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Query: Get jobs and skills mapped
    statement = (
        select(Skill.id, Job.budget_max)
        .join(JobSkillLink, JobSkillLink.skill_id == Skill.id)
        .join(Job, Job.id == JobSkillLink.job_id)
    )
    
    results = session.exec(statement).all()
    
    stats = defaultdict(lambda: {"count": 0, "sum_budget": 0.0})
    for skill_id, budget_max in results:
        stats[skill_id]["count"] += 1
        if budget_max:
            stats[skill_id]["sum_budget"] += budget_max

    # Update skill_trends table for today
    today = datetime.utcnow().date()
    for skill_id, data in stats.items():
        count = data["count"]
        avg_budget = data["sum_budget"] / count if count > 0 else 0
        
        # Upsert logic for today's snapshot
        stmt = select(SkillTrend).where(SkillTrend.skill_id == skill_id, SkillTrend.date == today)
        trend = session.exec(stmt).first()
        if not trend:
            trend = SkillTrend(skill_id=skill_id, date=today)
            session.add(trend)
            
        trend.job_count = count
        trend.avg_budget = avg_budget
        
        # Calculate a mock trend score (growth compared to historical could go here)
        trend.trend_score = float(count * 1.5)
    
    session.commit()
    print("Skill trends successfully committed to database.")
