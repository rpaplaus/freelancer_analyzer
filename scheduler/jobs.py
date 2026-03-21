from sqlmodel import Session
from database.db import engine
from analytics.trends import update_skill_trends

def scrape_job():
    print("Running scrape_job...")
    from scraper.pipeline import run_pipeline
    run_pipeline()

def run_analysis_job():
    print("Running run_analysis_job...")

def update_stats_job():
    print("Running update_stats_job...")
    with Session(engine) as session:
        update_skill_trends(session)

def update_rag_job():
    print("Running update_rag_job...")
