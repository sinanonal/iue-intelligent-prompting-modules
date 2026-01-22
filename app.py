import streamlit as st
import pandas as pd
from datetime import date

# -----------------------------
# CONFIG (edit these)
# -----------------------------
SEMESTER_END = date(2026, 5, 15)  # <-- change each semester
ROSTER_PATH = "roster.csv"        # <-- place roster.csv in your repo

ALLOWED_DOMAIN = "@siue.edu"      # optional extra safety

# -----------------------------
# Helpers
# -----------------------------
def _normalize_email(x: str) -> str:
    return (x or "").strip().lower()

@st.cache_data
def load_roster(path: str) -> set[str]:
    df = pd.read_csv(path)
    if "email" not in df.columns:
        raise ValueError("Roster CSV must include a column named 'email'.")
    emails = {_normalize_email(e) for e in df["email"].dropna().tolist()}
    return {e for e in emails if e}  # remove blanks

def access_gate():
    # Hard cutoff
    today = date.today()
    if today > SEMESTER_END:
        st.error("This course app is no longer available (semester access has ended).")
        st.stop()

    # Load roster
    try:
        roster_emails = load_roster(ROSTER_PATH)
    except Exception as e:
        st.error("Roster file is missing or invalid. Please contact the instructor.")
        st.caption(f"Admin detail: {e}")
        st.stop()

    # Session state
    if "authorized" not in st.session_state:
        st.session_state.authorized = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""

    if st.session_state.authorized:
        return  # already signed in

    # Login UI
    st.title("Course App Login")
    email = st.text_input("Enter your SIUE email", value=st.session_state.user_email).strip()
    col1, col2 = st.columns([1, 2])
    with col1:
        login_clicked = st.button("Log in", use_container_width=True)
    with col2:
        st.caption("Access is limited to enrolled students during the semester.")

    if login_clicked:
        email_n = _normalize_email(email)

        # Basic checks
        if not email_n.endswith(ALLOWED_DOMAIN):
            st.error("Please use your SIUE email address.")
            st.stop()

        # Roster check
        if email_n not in roster_emails:
            st.error("Your email is not on the course roster. If you just added the class, contact the instructor.")
            st.stop()

        st.session_state.authorized = True
        st.session_state.user_email = email_n
        st.success("Login successful.")
        st.rerun()

# -----------------------------
# CALL THE GATE BEFORE THE APP
# -----------------------------
access_gate()

# If we got here, user is authorized and within semester dates.
# Your actual app starts below:
st.write(f"Welcome, {st.session_state.user_email}!")
# ... rest of your Streamlit app ...






import streamlit as st

st.set_page_config(
    page_title="Home — Intelligent Prompting",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📘 Intelligent Prompting: Using AI for Creative and Analytical Thinking")
st.header("Welcome")

st.markdown("""
Welcome to the course! This class is designed to help you learn how to communicate effectively with AI tools such as **ChatGPT, Claude, Gemini, and Copilot**—a skill that is becoming essential across many fields.

You may already be using AI for writing, studying, brainstorming, or problem-solving. In this course, you will move beyond casual use and learn **how to guide these tools intentionally**. We focus on **intelligent prompting**: writing clear, structured instructions that help AI produce useful, accurate, and appropriate responses.

This is an **interdisciplinary course**, which means students from **all majors** are welcome. Whether you are studying engineering, business, health sciences, social sciences, arts, or another field, you will learn how AI can support your academic and professional work. You will practice prompting through hands-on activities, real-world examples, and interactive modules inside this app.

Throughout the course, we emphasize **critical thinking and responsible AI use**. AI can be a powerful assistant, but it also has limitations. You will learn how to evaluate AI responses, recognize potential errors or bias, and use these tools ethically and transparently.

By the end of the course, you will develop your own **personal prompting practice**—one that helps you think more clearly, communicate more effectively, and collaborate responsibly with AI systems.

""")

st.markdown("---")

st.subheader("📬 Questions, Feedback, and Communication")

st.markdown("""
If you have **any questions**, need clarification at any point, or would like to share **feedback on how to make this course better**, please do not hesitate to reach out.

Your questions and suggestions are always welcome, and they help improve the course for everyone.
""")

st.markdown(
    "📧 **Email:** "
    "[sonal@siue.edu](mailto:sonal@siue.edu)"
)

st.markdown("---")

st.subheader("🚀 Getting Started")

st.markdown("""
To begin, review the **Course Overview and Introduction** to understand how the course is organized.  
When you are ready, continue to **Module 1** to start learning about generative AI and prompting.
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("📘 Go to Course Overview"):
        st.switch_page("pages/00_Course Overview.py")

with col2:
    if st.button("➡️ Go to Module 1"):
        st.switch_page("pages/01_Module 1.py")
