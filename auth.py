# auth.py
import streamlit as st
import pandas as pd
from datetime import date

# ====== SETTINGS ======
SEMESTER_END = date(2026, 5, 15)     # change each semester
ROSTER_PATH = "roster.csv"           # put roster.csv next to app.py
ALLOWED_DOMAIN = "@siue.edu"         # optional

# ====== HELPERS ======
def _norm_email(x: str) -> str:
    return (x or "").strip().lower()

@st.cache_data
def _load_roster(path: str) -> set[str]:
    df = pd.read_csv(path)
    if "email" not in df.columns:
        raise ValueError("Roster CSV must include a column named 'email'.")
    return {_norm_email(e) for e in df["email"].dropna().tolist()}

def logout():
    # Clear only auth-related session keys (safe)
    for k in ["authorized", "user_email"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

def require_access():
    # 1) Semester cutoff
    if date.today() > SEMESTER_END:
        st.error("This course app is no longer available (semester access has ended).")
        st.stop()

    # 2) Session defaults
    st.session_state.setdefault("authorized", False)
    st.session_state.setdefault("user_email", "")

    # 3) If authorized, show logout + proceed
    if st.session_state["authorized"]:
        with st.sidebar:
            st.markdown("### Account")
            st.write(st.session_state["user_email"])
            if st.button("Log out", use_container_width=True):
                logout()
        return

    # 4) Not authorized: show login screen and STOP the rest of the page
    roster = _load_roster(ROSTER_PATH)

    st.title("Course App Login")
    email = st.text_input("Enter your SIUE email", placeholder="name@siue.edu")

    col1, col2 = st.columns([1, 2])
    with col1:
        login_clicked = st.button("Log in", use_container_width=True)
    with col2:
        st.caption("Access is limited to enrolled students during the semester.")

    if login_clicked:
        email_n = _norm_email(email)

        if not email_n.endswith(ALLOWED_DOMAIN):
            st.error("Please use your SIUE email address.")
            st.stop()

        if email_n not in roster:
            st.error("Your email is not on the course roster. If you just added the class, contact the instructor.")
            st.stop()

        st.session_state["authorized"] = True
        st.session_state["user_email"] = email_n
        st.success("Login successful.")
        st.rerun()

    st.stop()
