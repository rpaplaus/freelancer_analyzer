import streamlit as st
import pandas as pd
from sqlmodel import Session
from database.db import engine
from analytics.recommendations import get_best_jobs, get_hidden_gems
from rag.rag_query import search_similar_jobs

st.title("🎯 Top Recommendations & AI Search")
st.write("Find 'Hidden Gems' or ask our Vector Database to find jobs matching your exact skills semantically.")

st.subheader("🔍 AI Semantic Search (RAG)")
search_query = st.text_input("Describe your ideal job (e.g. 'I build FastApi and Langchain backends for $50/hr')")
if search_query:
    with st.spinner("Searching vector space..."):
        results = search_similar_jobs(search_query, k=5)
        if results:
            df_search = pd.DataFrame(results)
            st.dataframe(df_search, use_container_width=True)
        else:
            st.warning("No matches found in ChromaDB. Have you run `python main.py embed`?")

st.markdown("---")

with Session(engine) as session:
    hidden_gems = get_hidden_gems(session)
    best_jobs = get_best_jobs(session, limit=10)
    
    if hidden_gems:
        st.warning("Apply to these Hidden Gems immediately:")
        for job in hidden_gems:
            score = next((s.final_score for s in job.scores if s.final_score), "N/A")
            st.markdown(f"- **{job.title}** (Score: {score}) - ${job.budget_min}-${job.budget_max} - {job.proposals} Proposals")
    else:
        st.info("No Hidden Gems found right now.")
        
    st.subheader("Highest Scoring Jobs Overall")
    if best_jobs:
        job_dicts = []
        for j in best_jobs:
            score = next((s.final_score for s in j.scores if s.final_score), "N/A")
            job_dicts.append({
                "Score": score,
                "Title": j.title,
                "Budget Max": j.budget_max,
                "Proposals": j.proposals,
                "Posted": j.posted_at,
                "URL": j.url
            })
        st.dataframe(pd.DataFrame(job_dicts), width='stretch')
    else:
        st.info("No scored jobs found. Make sure the Scoring Engine is running (python main.py score).")
