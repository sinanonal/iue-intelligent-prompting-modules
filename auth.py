import streamlit as st
import pandas as pd
from datetime import date

# ===== SETTINGS =====
SEMESTER_END = date(2026, 5, 15)
ROSTER_PATH = "roster.csv"
ALLOWED_DOMAIN = "@siue.edu"

# ===== HELPERS =====
def _norm_email(x: str) -> str:
    return (x or "").strip().lower()

@st.cache_data
def _load_roster(path: str) -> set[str]:
    df = pd.read_csv(path)
    if "email" not in df.columns:
        raise ValueError("Roster CSV must include a column named 'email'.")
    return {_norm_email(e) for e in df["email"].dropna()}

# ===== AUTH ACTIONS =====
def logout():
    for k in ["authorized", "user_email"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

def require_access():
    # Semester cutoff
    if date.today() > SEMESTER_END:
        st.error("This course app is no longer available (semester access has ended).")
        st.stop()

    # Session defaults
    st.session_state.setdefault("authorized", False)
    st.session_state.setdefault("user_email", "")

    # Already logged in → allow page to render
    if st.session_state["authorized"]:
        return

    # Login screen
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
            st.error("Your email is not on the course roster.")
            st.stop()

        st.session_state["authorized"] = True
        st.session_state["user_email"] = email_n
        st.success("Login successful.")
        st.rerun()

    # IMPORTANT: stop page execution until logged in
    st.stop()

# ===== UI COMPONENTS =====
def render_top_bar(title: str):
    col_left, col_right = st.columns([6, 2])

    with col_left:
        st.markdown(f"### {title}")

    with col_right:
        st.markdown(
            f"<div style='text-align:right; font-size:0.85em;'>"
            f"Signed in as <b>{st.session_state['user_email']}</b>"
            f"</div>",
            unsafe_allow_html=True
        )
        if st.button("Log out", use_container_width=True):
            logout()

    st.divider()

def render_course_sidebar():
    st.sidebar.markdown("## 📚 Course Contents")

    pages = {
        "Home": "app.py",
        "Course Overview": "pages/00_Course Overview.py",
        "Module 1 — Foundations": "pages/01_Module 1.py",
        "Module 2 — Prompt Structure": "pages/02_Module 2.py",
        "Module 3 — Core Patterns": "pages/03_Module 3.py",
        "Module 4 — Refinement": "pages/04_Module 4.py",
        "Module 5 — Verification": "pages/05_Module 5.py",
        "Module 6 — Creativity": "pages/06_Module 6.py",
        "Module 7 — Complex Inputs": "pages/07_Module 7.py",
        "Module 8": "pages/08_Module 8.py",
        "Module 9": "pages/09_Module 9.py",
        "Module 10": "pages/10_Module 10.py",
        "Module 11": "pages/11_Module 11.py",
        "Module 12": "pages/12_Module 12.py",
        "Module 13": "pages/13_Module 13.py",
    }

    choice = st.sidebar.radio(
        "Navigate to:",
        list(pages.keys()),
        label_visibility="collapsed"
    )

    if st.sidebar.button("Open", use_container_width=True):
        st.switch_page(pages[choice])
