from sqlmodel import Session
from database.db import engine, init_db
from database.crud import get_or_create_platform, create_job, get_or_create_client
from datetime import datetime, timedelta
import random

def run_seed():
    init_db()
    
    with Session(engine) as session:
        platform = get_or_create_platform(session, name="upwork", base_url="https://upwork.com")
        
        skills_pool = ["Python", "AI", "React", "Data Engineering", "Langchain", "FastAPI"]
        client_countries = ["United States", "United Kingdom", "Canada", "Germany", "Australia"]
        
        print("Seeding database with 50 mock jobs and clients...")
        for i in range(50):
            # Create a mock client
            spent = random.choice([0, 100, 5000, 15000, 50000])
            rating = random.uniform(3.5, 5.0) if spent > 0 else 0.0
            country = random.choice(client_countries)
            
            client = get_or_create_client(
                session,
                platform_id=platform.id,
                external_id=f"client_mock_{i}",
                country=country,
                total_spent=spent,
                rating=round(rating, 2),
                total_hires=random.randint(0, 20)
            )
            
            # Create a mock job
            budget = random.randint(50, 5000)
            skills = random.sample(skills_pool, k=random.randint(1, 4))
            
            job_data = {
                "platform_id": platform.id,
                "client_id": client.id,
                "external_id": f"job_mock_{i}",
                "title": f"Need expert in {skills[0]} for a project",
                "description": f"We are looking for a senior developer skilled in {', '.join(skills)}.",
                "url": f"https://upwork.com/jobs/mock_{i}",
                "posted_at": datetime.utcnow() - timedelta(days=random.randint(0, 10)),
                "budget_min": budget,
                "budget_max": budget,
                "hourly": False,
                "category": "Web Development" if "React" in skills else "Data Science & AI",
                "skills": skills,
                "proposals": random.randint(0, 60)
            }
            try:
                create_job(session, **job_data)
            except Exception as e:
                pass
                
        print("Database seeded! Run `python main.py score` and `python main.py trends` next.")
