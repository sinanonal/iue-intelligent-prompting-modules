import streamlit as st
import auth

st.set_page_config(page_title="Module 1", layout="wide")
auth.require_identity(require_email=False)

st.title("Module 1 — Foundations of Generative AI")

st.markdown("""
### What you will do
- Read the Module 1 readings
- Submit a short reflection (and optional file upload)
""")

# Manual confirmation for module page
if st.button("I reviewed Module 1 instructions"):
    auth.log_event("module_reviewed", {"module": 1, "item": "instructions"})
    st.success("Recorded.")
