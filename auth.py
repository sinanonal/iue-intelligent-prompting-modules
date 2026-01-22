import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path
import re

# ===== SETTINGS =====
SEMESTER_END = date(2026, 5, 15)
ROSTER_PATH = "roster.csv"
ALLOWED_DOMAIN = "@siue.edu"

PAGES_DIR = Path("pages")

# ===== HELPERS =====
def _norm_email(x: str) -> str:
    return (x or "").strip().lower()

@st.cache_data
def _load_roster(path: str) -> set[str]:
    df = pd.read_csv(path)
    if "email" not in df.columns:
        raise ValueError("Roster CSV must include a column named 'email'.")
    return {_norm_email(e) for e in df["email"].dropna()}

def logout():
    for k in ["authorized", "user_email", "current_page_path"]:
        st.session_state.pop(k, None)
    st.rerun()

def require_access():
    if date.today() > SEMESTER_END:
        st.error("This course app is no longer available (semester access has ended).")
        st.stop()

    st.session_state.setdefault("authorized", False)
    st.session_state.setdefault("user_email", "")

    if st.session_state["authorized"]:
        return

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

    st.stop()

# ===== GLOBAL UI FIX: HIDE STREAMLIT DEFAULT NAV =====
def apply_global_styles():
    # This hides Streamlit's built-in multipage nav (the "app / Module 1 / View more" list)
    # We use multiple selectors to handle different Streamlit versions.
    st.markdown(
        """
        <style>
        /* Streamlit built-in page nav container */
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="stSidebarNavItems"] { display: none !important; }
        [data-testid="stSidebarNavSeparator"] { display: none !important; }

        /* Some versions render a navigation region in the sidebar */
        section[data-testid="stSidebar"] nav { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

# ===== TOP BAR =====
def render_top_bar(title: str):
    col_left, col_right = st.columns([6, 2])

    with col_left:
        st.markdown(f"### {title}")

    with col_right:
        st.markdown(
            f"<div style='text-align:right; font-size:0.85em;'>"
            f"Signed in as <b>{st.session_state.get('user_email','')}</b>"
            f"</div>",
            unsafe_allow_html=True
        )
        if st.button("Log out", use_container_width=True):
            logout()

    st.divider()

# ===== AUTO-DETECT PAGES + HIGHLIGHT CURRENT =====
def _label_from_filename(filename: str) -> str:
    # e.g., "01_Module_1.py" -> "Module 1"
    base = filename.replace(".py", "")
    base = base.replace("_", " ").strip()

    # remove leading numeric prefix like "01 " or "00 "
    base = re.sub(r"^\d+\s*", "", base)

    # normalize common labels
    base = base.replace("Course Overview", "Course Overview")

    return base

def _sort_key(path: Path):
    # Sort by leading number if present, else push to bottom
    m = re.match(r"^(\d+)_", path.name)
    return (int(m.group(1)) if m else 10_000, path.name.lower())

@st.cache_data
def build_pages_index():
    pages = {"Home": "app.py"}

    if PAGES_DIR.exists():
        for p in sorted(PAGES_DIR.glob("*.py"), key=_sort_key):
            if p.name.startswith("_"):
                continue
            label = _label_from_filename(p.name)
            pages[label] = str(p).replace("\\", "/")  # safe on Windows too

    return pages

def render_course_sidebar():
    st.sidebar.markdown("## 📚 Course Contents")

    pages = build_pages_index()
    labels = list(pages.keys())

    current = st.session_state.get("current_page_path", "app.py")

    # default selection = current page
    try:
        default_index = list(pages.values()).index(current)
    except ValueError:
        default_index = 0

    choice = st.sidebar.radio(
        "Navigate to:",
        labels,
        index=default_index,
        label_visibility="collapsed"
    )

    # Navigate immediately when a different choice is made
    target = pages[choice]
    if target != current:
        st.switch_page(target)

# ===== ONE CALL TO SET CURRENT PAGE (for highlighting) =====
def set_current_page(page_path: str):
    st.session_state["current_page_path"] = page_path

# ===== OPTIONAL: ONE-LINER INIT FOR EVERY PAGE =====
def init_course_page(title: str, page_path: str):
    apply_global_styles()
    require_access()
    set_current_page(page_path)
    render_top_bar(title)
    render_course_sidebar()
