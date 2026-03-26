from sqlmodel import Session
from database.db import get_session, engine, init_db
from database.crud import get_or_create_platform, create_job, get_or_create_client
from scraper.upwork_scraper import fetch_upwork_jobs
from scraper.remoteok_scraper import fetch_remoteok_jobs
from datetime import datetime

def run_pipeline():
    init_db()
    
    print("Fetching jobs from Multiple Sources...")
    all_raw_jobs = []
    
    # Source 1: Upwork Playwright API
    upwork_jobs = fetch_upwork_jobs("python")
    print(f"Playwright found {len(upwork_jobs)} Upwork jobs.")
    all_raw_jobs.extend(upwork_jobs)
    
    # Source 2: RemoteOK Public API
    remoteok_jobs = fetch_remoteok_jobs("python")
    print(f"API found {len(remoteok_jobs)} RemoteOK jobs.")
    all_raw_jobs.extend(remoteok_jobs)
    
    with Session(engine) as session:
        saved_count = 0
        for rjob in all_raw_jobs:
            platform = get_or_create_platform(session, name=rjob.platform)
            
            client = None
            if rjob.client_country or rjob.client_external_id or rjob.client_total_spent is not None:
                client = get_or_create_client(
                    session,
                    platform_id=platform.id,
                    external_id=rjob.client_external_id or f"unknown_{rjob.client_country}",
                    country=rjob.client_country,
                    total_spent=rjob.client_total_spent,
                    rating=rjob.client_rating,
                    total_hires=rjob.client_total_hires
                )
            
            job_data = {
                "platform_id": platform.id,
                "client_id": client.id if client else None,
                "external_id": rjob.external_id,
                "title": rjob.title,
                "description": rjob.description,
                "url": str(rjob.url),
                "posted_at": rjob.posted_at or datetime.utcnow(),
                "budget_min": rjob.budget_min,
                "budget_max": rjob.budget_max,
                "hourly": rjob.hourly,
                "category": rjob.category,
                "skills": rjob.skills,
                "proposals": rjob.proposals
            }
            
            try:
                job = create_job(session, **job_data)
                if job:
                    saved_count += 1
            except Exception as e:
                print(f"Error saving job {rjob.title}: {e}")
                session.rollback()
                
        print(f"Pipeline finished. Processed {saved_count} new cross-platform jobs in DB.")
