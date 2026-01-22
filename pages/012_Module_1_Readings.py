# pages/02_Module_1_Readings.py
import streamlit as st
import auth
from content import MODULE1_READINGS

st.set_page_config(page_title="Module 1 Readings", layout="wide")
auth.require_identity(require_email=False)

st.title("Module 1 Readings")

# Sidebar reading navigation (titles visible)
reading_choice = st.sidebar.radio(
    "Choose a reading section:",
    list(MODULE1_READINGS.keys()),
    index=0
)

st.markdown(MODULE1_READINGS[reading_choice])

# Manual confirmation for progress (no auto-check)
if "module1_readings_progress" not in st.session_state:
    st.session_state.module1_readings_progress = {}

if st.button("I reviewed this reading"):
    st.session_state.module1_readings_progress[reading_choice] = True
    auth.log_event("module1_reading_reviewed", {"reading": reading_choice})
    st.success("Recorded.")

with st.sidebar:
    st.markdown("### Reading progress")
    for k in MODULE1_READINGS.keys():
        done = st.session_state.module1_readings_progress.get(k, False)
        st.write(("✅ " if done else "⬜ ") + k)
