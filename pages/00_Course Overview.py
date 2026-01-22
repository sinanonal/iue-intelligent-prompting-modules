import streamlit as st
import auth
from content import COURSE_OVERVIEW_SECTIONS

st.set_page_config(page_title="Course Overview", layout="wide")
auth.require_identity(require_email=False)

st.title("Course Overview")

# Manual progress tracker (no auto-check)
if "overview_progress" not in st.session_state:
    st.session_state.overview_progress = {}

def reviewed_button(section_key: str):
    if st.button(f"I reviewed: {section_key}", key=f"review_{section_key}"):
        st.session_state.overview_progress[section_key] = True
        auth.log_event("overview_section_reviewed", {"section": section_key})
        st.success("Recorded.")

with st.sidebar:
    st.markdown("### Overview checklist")
    for k in COURSE_OVERVIEW_SECTIONS.keys():
        done = st.session_state.overview_progress.get(k, False)
        st.write(("✅ " if done else "⬜ ") + k)

for section_key, section_md in COURSE_OVERVIEW_SECTIONS.items():
    st.markdown(section_md)
    reviewed_button(section_key)
    st.divider()
