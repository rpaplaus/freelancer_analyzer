from typing import Optional, List
from sqlmodel import Session, select
from database.models import Platform, Client, Job, Skill, JobSkillLink

def get_or_create_platform(session: Session, name: str, base_url: str = None) -> Platform:
    statement = select(Platform).where(Platform.name == name)
    platform = session.exec(statement).first()
    if not platform:
        platform = Platform(name=name, base_url=base_url)
        session.add(platform)
        session.commit()
        session.refresh(platform)
    return platform

def get_or_create_client(session: Session, platform_id: int, external_id: str, **kwargs) -> Client:
    statement = select(Client).where(Client.platform_id == platform_id, Client.external_id == external_id)
    client = session.exec(statement).first()
    if not client:
        client = Client(platform_id=platform_id, external_id=external_id, **kwargs)
        session.add(client)
        session.commit()
        session.refresh(client)
    else:
        # Update client stats if provided
        for key, value in kwargs.items():
            setattr(client, key, value)
        session.add(client)
        session.commit()
        session.refresh(client)
    return client

def create_job(session: Session, **job_data) -> Job:
    # Handle skills separately
    skills_data = job_data.pop("skills", [])
    
    # Check if job exists
    if job_data.get("external_id") and job_data.get("platform_id"):
        stmt = select(Job).where(Job.platform_id == job_data["platform_id"], Job.external_id == job_data["external_id"])
        existing = session.exec(stmt).first()
        if existing:
            # Update existing job with new scraped data (e.g. proposals)
            for key, value in job_data.items():
                if value is not None:
                    setattr(existing, key, value)
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing

    job = Job(**job_data)
    session.add(job)
    session.commit()
    session.refresh(job)

    # Handle skills
    for skill_name in skills_data:
        skill = get_or_create_skill(session, skill_name.lower())
        
        # Link skill
        link_stmt = select(JobSkillLink).where(JobSkillLink.job_id == job.id, JobSkillLink.skill_id == skill.id)
        existing_link = session.exec(link_stmt).first()
        if not existing_link:
            link = JobSkillLink(job_id=job.id, skill_id=skill.id)
            session.add(link)
    
    session.commit()
    return job

def get_or_create_skill(session: Session, name: str) -> Skill:
    statement = select(Skill).where(Skill.name == name)
    skill = session.exec(statement).first()
    if not skill:
        skill = Skill(name=name)
        session.add(skill)
        session.commit()
        session.refresh(skill)
    return skill
