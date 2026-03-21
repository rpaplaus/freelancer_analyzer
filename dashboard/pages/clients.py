import streamlit as st
from sqlmodel import Session, select, func
from database.db import engine
from database.models import Client

st.title("🧠 Client Quality Analysis")
st.write("Determine which clients are likely to hire and pay well, based on tracked data.")

with Session(engine) as session:
    total_clients = session.exec(select(func.count(Client.id))).one()
    
    if total_clients > 0:
        # High quality = spent >= 5000 and rating >= 4.5
        hq_stmt = select(func.count(Client.id)).where(Client.total_spent >= 5000, Client.rating >= 4.5)
        hq_clients = session.exec(hq_stmt).one()
        
        avg_spent_stmt = select(func.avg(Client.total_spent)).where(Client.total_spent != None)
        avg_spent = session.exec(avg_spent_stmt).one() or 0.0

        col1, col2 = st.columns(2)
        hq_percentage = (hq_clients / total_clients * 100) if total_clients > 0 else 0
        
        col1.metric("High Quality Clients Tracked", f"{hq_clients} / {total_clients}", f"{hq_percentage:.1f}%")
        col2.metric("Average Client Spent", f"${avg_spent:,.2f}")
        
        st.subheader("Top Spenders")
        top_spenders = session.exec(select(Client).where(Client.total_spent != None).order_by(Client.total_spent.desc()).limit(10)).all()
        for c in top_spenders:
            country = c.country or "Unknown"
            rating = c.rating or "N/A"
            spent = f"${c.total_spent:,.2f}" if c.total_spent else "Hidden"
            hires = c.total_hires or 0
            st.markdown(f"🛂 **{country}** | ⭐ {rating} | 💰 {spent} spent | {hires} hires")
    else:
        st.info("No clients gathered yet. Make sure you fetch jobs with rich client details.")
