# auth.py
import streamlit as st
import pandas as pd
from datetime import date

SEMESTER_END = date(2026, 5, 15)
ALLOWED_DOMAIN = "@siue.edu"

def _normalize_email(x: str) -> str:
    return (x or "").strip().lower()

@st.cache_data
def load_roster(path="roster.csv"):
    df = pd.read_csv(path)
    if "email" not in df.columns:
        raise ValueError("Roster CSV must include an 'email' column.")
    return {_normalize_email(e) for e in df["email"].dropna()}

def require_access():
    # semester cutoff
    if date.today() > SEMESTER_END:
        st.error("This course app is no longer available (semester access has ended).")
        st.stop()

    # session defaults
    if "authorized" not in st.session_state:
        st.session_state.authorized = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""

    if st.session_state.authorized:
        return

    roster = load_roster()

    st.title("Course App Login")
    email = st.text_input("Enter your SIUE email")

    if st.button("Log in"):
        email_n = _normalize_email(email)

        if not email_n.endswith(ALLOWED_DOMAIN):
            st.error("Please use your SIUE email.")
            st.stop()

        if email_n not in roster:
            st.error("Email not found on course roster.")
            st.stop()

        st.session_state.authorized = True
        st.session_state.user_email = email_n
        st.success("Login successful.")
        st.rerun()
