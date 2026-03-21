import argparse
import sys
from config.settings import settings

def main():
    parser = argparse.ArgumentParser(description="Freelancer Analyzer main execution point.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Scraper command
    scrape_parser = subparsers.add_parser("scrape", help="Run the scrapers manually")
    
    # API command
    api_parser = subparsers.add_parser("api", help="Run the FastAPI application")

    # Scheduler command
    scheduler_parser = subparsers.add_parser("scheduler", help="Run the APScheduler background tasks")

    # Dashboard command
    dashboard_parser = subparsers.add_parser("dashboard", help="Run the Streamlit dashboard")

    # Scoring engine command
    score_parser = subparsers.add_parser("score", help="Run scoring engine across all jobs")

    # Trends aggregation command
    trends_parser = subparsers.add_parser("trends", help="Aggregate macro trends")

    # Seed database command
    seed_parser = subparsers.add_parser("seed", help="Seed database with dummy data")

    # Reset database command
    reset_parser = subparsers.add_parser("reset", help="Drop and recreate all database tables")

    # LLM Analyzer command
    analyze_parser = subparsers.add_parser("analyze", help="Run LLM analysis on pending jobs")

    # Vector Embedder command
    embed_parser = subparsers.add_parser("embed", help="Generate vector semantic embeddings")



    args = parser.parse_args()

    if args.command == "scrape":
        print("Starting manual scrape job...")
        from scraper.pipeline import run_pipeline
        run_pipeline()
    elif args.command == "api":
        import uvicorn
        print("Starting FastAPI server...")
        uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=False)
    elif args.command == "scheduler":
        from scheduler.cron import start_scheduler
        start_scheduler()
    elif args.command == "dashboard":
        import os
        import sys
        print("Starting Streamlit Dashboard...")
        os.system(f"{sys.executable} -m streamlit run dashboard/app.py")
    elif args.command == "score":
        from sqlmodel import Session, select
        from database.db import engine
        from database.models import Job
        from analytics.scoring import compute_job_score
        with Session(engine) as session:
            jobs = session.exec(select(Job)).all()
            for j in jobs:
                compute_job_score(session, j)
            print(f"Computed scores for {len(jobs)} jobs.")
    elif args.command == "trends":
        from sqlmodel import Session
        from database.db import engine
        from analytics.trends import update_skill_trends
        with Session(engine) as session:
            update_skill_trends(session)
        print("Updated macro trends successfully.")
    elif args.command == "seed":
        from database.seed import run_seed
        run_seed()
    elif args.command == "reset":
        from database.reset import run_reset
        run_reset()
    elif args.command == "analyze":
        from llm_analysis.job_classifier import analyze_unprocessed_jobs
        analyze_unprocessed_jobs()
    elif args.command == "embed":
        from rag.embedder import embed_new_jobs
        embed_new_jobs()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
