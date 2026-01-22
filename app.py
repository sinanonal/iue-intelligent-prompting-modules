import streamlit as st
from auth import init_course_page

st.set_page_config(
    page_title="Home — Intelligent Prompting",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_course_page("Home Page", "app.py")

st.title("📘 Intelligent Prompting: Using AI for Creative and Analytical Thinking")
st.header("Welcome")

st.markdown("""
Welcome to the course! Use the sidebar to open **Course Overview** first,
then continue to **Module 1**.
""")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("➡️ Course Overview", use_container_width=True):
        st.switch_page("pages/00_Course Overview.py")
