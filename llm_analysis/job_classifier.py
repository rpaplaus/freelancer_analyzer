from sqlmodel import Session, select
from database.db import engine
from database.models import Job, AnalysisResult
from config.settings import settings
import json
import os

def analyze_unprocessed_jobs():
    """Finds all jobs that haven't been analyzed yet and categorizes them with an LLM."""
    if not settings.OPENAI_API_KEY:
        print("OPENAI_API_KEY is missing. Skipping LLM Analysis.")
        return

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import PromptTemplate
    except ImportError:
        print("Please install langchain and langchain-openai via pip.")
        return

    llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
    
    prompt = PromptTemplate(
        input_variables=["title", "description", "budget"],
        template='''
You are an expert technical recruiter analyzing a freelance job post.
Given the following job details, classify it into specific categories and determine the difficulty.

Title: {title}
Description: {description}
Budget: ${budget}

Respond ONLY with a valid JSON document with the following structure:
{{
    "is_scam": boolean,
    "estimated_difficulty": "Entry", "Intermediate", or "Expert",
    "core_technologies": ["list of max 5 key technologies"],
    "hidden_requirements": "any subtle requirements mentioned (or empty)"
}}
'''
    )
    
    with Session(engine) as session:
        # Find jobs not in AnalysisResult
        existing_analysis = session.exec(select(AnalysisResult.job_id)).all()
        
        stmt = select(Job)
        if existing_analysis:
            stmt = stmt.where(Job.id.notin_(existing_analysis))
            
        target_jobs = session.exec(stmt).all()
        
        if not target_jobs:
            print("No new jobs to analyze.")
            return

        print(f"Found {len(target_jobs)} jobs pending LLM analysis.")
        
        success_count = 0
        for job in target_jobs:
            print(f"Analyzing job: {job.title[:60]}...")
            try:
                response = llm.invoke(prompt.format(
                    title=job.title, 
                    description=job.description[:1500],
                    budget=job.budget_max or 0
                ))
                
                # Parse raw string
                raw_json = response.content.strip()
                if raw_json.startswith("```json"):
                    raw_json = raw_json[7:-3].strip()
                elif raw_json.startswith("```"):
                    raw_json = raw_json[3:-3].strip()
                    
                result_data = json.loads(raw_json)
                
                analysis = AnalysisResult(
                    job_id=job.id,
                    analysis_type="job_classification",
                    result=result_data
                )
                session.add(analysis)
                session.commit()
                success_count += 1
            except Exception as e:
                print(f"LLM Error on job {job.id}: {e}")
                session.rollback()
                
        print(f"Batch LLM Job classification completed. Processed {success_count} jobs.")
