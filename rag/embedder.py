from sqlmodel import Session, select
from database.db import engine
from database.models import Job, AnalysisResult
from rag.vector_store import get_vector_store
from langchain_core.documents import Document

def embed_new_jobs():
    """Extracts jobs and inserts them into ChromaDB as Vectors."""
    try:
        vector_store = get_vector_store()
    except ValueError as e:
        print(e)
        return
        
    print("Preparing documents for semantic embedding...")
    with Session(engine) as session:
        # Get all jobs
        jobs = session.exec(select(Job)).all()
        
        docs_to_add = []
        for job in jobs:
            content = f"Title: {job.title}\nDescription: {job.description}\nCategory: {job.category}\n"
            
            # Enrich embedding with LLM analysis if available
            analysis = session.exec(select(AnalysisResult).where(AnalysisResult.job_id == job.id)).first()
            if analysis and analysis.result:
                techs = analysis.result.get("core_technologies", [])
                content += f"Tech Stack: {', '.join(techs)}\n"
            
            doc = Document(
                page_content=content,
                metadata={
                    "job_id": job.id,
                    "external_id": job.external_id or "",
                    "budget_max": float(job.budget_max or 0.0),
                    "url": str(job.url)
                },
                id=str(job.id) # Deduplicate by job ID intrinsically
            )
            docs_to_add.append(doc)
            
        if docs_to_add:
            print(f"Generating vectors for {len(docs_to_add)} jobs via OpenAI...")
            vector_store.add_documents(docs_to_add, ids=[doc.id for doc in docs_to_add])
            print("Successfully encoded and saved all jobs to ChromaDB.")
        else:
            print("No jobs found to embed.")
