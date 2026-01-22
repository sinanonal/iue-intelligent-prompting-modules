# pages/01_Module_1.py
import streamlit as st
import auth

st.set_page_config(page_title="Module 1", layout="wide")
auth.require_identity(require_email=False)

st.title("Module 1 — Foundations of Generative AI")

st.markdown("""
### What you will do in Module 1
- Read the three short readings (use the Module 1 Readings page)
- Submit a short reflection
- Upload any supporting file if required by your instructor
""")

st.info("Use the left menu to open **Module 1 Readings** and **Submit Assignments**.")
