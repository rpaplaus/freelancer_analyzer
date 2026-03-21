import streamlit as st
import pandas as pd
from sqlmodel import Session, select
from database.db import engine
from database.models import SkillTrend, Skill
from datetime import datetime

st.title("📈 Trending Skills & Markets")
st.markdown("Macro trends calculated directly from PostgreSQL history.")

with Session(engine) as session:
    today = datetime.utcnow().date()
    
    # Select the top trending skills mapped to their names for today
    statement = (
        select(Skill.name, SkillTrend.job_count, SkillTrend.avg_budget, SkillTrend.trend_score)
        .join(Skill)
        .where(SkillTrend.date == today)
        .order_by(SkillTrend.trend_score.desc())
        .limit(20)
    )
    
    results = session.exec(statement).all()
    
    if results:
        df = pd.DataFrame(results, columns=["Skill", "Job Count", "Avg Budget", "Trend Score"])
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Top 20 Trending Skills")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
        with col2:
            st.subheader("Visualizing Demand vs Budget")
            st.scatter_chart(df, x="Job Count", y="Avg Budget", color="Skill")
            
        st.subheader("Market Dominance")
        st.bar_chart(df, x="Skill", y="Trend Score")
    else:
        st.info("No trend data available for today yet! Wait for `update_stats_job` to run or run it manually.")
