import streamlit as st

st.set_page_config(
    page_title="Freelancer Analyzer",
    page_icon="💸",
    layout="wide"
)

st.title("Freelancer Analyzer Dashboard")
st.markdown("Welcome to the Freelancer Analyzer. Please select a page from the sidebar to view insights.")

st.sidebar.success("Select a dashboard above.")
