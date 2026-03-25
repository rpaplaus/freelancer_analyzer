from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.jobs import scrape_job, update_stats_job
from sqlmodel import Session, select
from database.db import engine
from database.models import Job
import time

def complete_pipeline():
    print("[CRON] Starting Full Pipeline iteration...")
    
    # 1. Scrape
    scrape_job()
    
    # 2. LLM Classify
    from llm_analysis.job_classifier import analyze_unprocessed_jobs
    analyze_unprocessed_jobs()
    
    # 3. Score
    from analytics.scoring import compute_job_score
    print("[CRON] Scoring newly analyzed jobs...")
    with Session(engine) as session:
        jobs = session.exec(select(Job)).all()
        for j in jobs:
            compute_job_score(session, j)
            
    # 4. Trends
    update_stats_job()
    
    # 5. Embed in Vector DB
    from rag.embedder import embed_new_jobs
    embed_new_jobs()
    
    print("[CRON] Full Pipeline iteration finished successfully.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    interval = 60 # 1 hour
    scheduler.add_job(complete_pipeline, 'interval', minutes=interval)
    scheduler.start()
    
    print(f"Scheduler started. The AI Pipeline will execute autonomously every {interval} minutes.")
    print("Press Ctrl+C to exit.")
    
    complete_pipeline()
    
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
