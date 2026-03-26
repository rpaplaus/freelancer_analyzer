import streamlit as st
import pandas as pd
from sqlmodel import Session, select
from database.db import engine
from database.models import Job

st.title("💼 Job Explorer")
st.write("Browse and filter captured jobs directly.")

with Session(engine) as session:
    jobs = session.exec(select(Job).order_by(Job.posted_at.desc()).limit(100)).all()
    
if not jobs:
    st.info("No jobs found in the database. Run `python main.py scrape` first.")
else:
    job_dicts = []
    for j in jobs:
        job_dicts.append({
            "Title": j.title,
            "Budget Min": j.budget_min,
            "Budget Max": j.budget_max,
            "Hourly": j.hourly,
            "Proposals": j.proposals,
            "Category": j.category,
            "Posted": j.posted_at,
            "URL": j.url
        })
    df = pd.DataFrame(job_dicts)
    st.dataframe(df)
