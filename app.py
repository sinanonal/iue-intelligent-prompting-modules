# app.py
import streamlit as st
import auth
from content import COURSE_TITLE, WELCOME_MESSAGE

st.set_page_config(page_title=COURSE_TITLE, layout="wide")

# Sidebar identity (shows on home too, but does NOT block home)
auth.render_identity_sidebar(require_email=False)

st.title(COURSE_TITLE)
st.markdown(WELCOME_MESSAGE)

st.markdown("### Navigation")
st.write("Use the page menu on the left (Streamlit multipage) to open Course Overview, Module 1, Readings, and Submissions.")
