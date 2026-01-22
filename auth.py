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

# ===== AUTO-DETECT PAGES + LABELS =====
def _label_from_filename(filename: str) -> str:
    # e.g., "01_Module_1.py" -> "Module 1"
    base = filename.replace(".py", "")
    base = base.replace("_", " ").strip()
    base = re.sub(r"^\d+\s*", "", base)  # remove leading numeric prefix
    return base

def _sort_key(path: Path):
    m = re.match(r"^(\d+)_", path.name)
    return (int(m.group(1)) if m else 10_000, path.name.lower())

@st.cache_data
def build_pages_index():
    """
    Returns an ORDERED dict-like mapping:
    Home, Course Overview, Module 1..13, then any other pages.
    """
    detected = {}

    # Always include Home
    detected["Home"] = "app.py"

    # Detect pages from /pages
    if PAGES_DIR.exists():
        for p in sorted(PAGES_DIR.glob("*.py"), key=_sort_key):
            if p.name.startswith("_"):
                continue
            label = _label_from_filename(p.name)
            detected[label] = str(p).replace("\\", "/")

    # Re-order to match your intended structure
    ordered = {}

    # 1) Home
    if "Home" in detected:
        ordered["Home"] = detected["Home"]

    # 2) Course Overview (if present)
    if "Course Overview" in detected:
        ordered["Course Overview"] = detected["Course Overview"]

    # 3) Modules 1..13 (if present)
    for i in range(1, 14):
        key = f"Module {i}"
        if key in detected:
            ordered[key] = detected[key]

    # 4) Any remaining pages (keep stable order)
    for k, v in detected.items():
        if k in ordered:
            continue
        ordered[k] = v

    return ordered

# ===== SIDEBAR (Course Contents + Course Overview sub-navigation) =====
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

    # Main navigation (this is the "click sidebar button" behavior)
    choice = st.sidebar.radio(
        label="",
        options=labels,
        index=default_index,
        key="course_contents_choice",
        label_visibility="collapsed",
    )

    # If user selects something else, navigate immediately
    target = pages[choice]
    if target != current:
        st.switch_page(target)

    # ---- Course Overview sub-navigation: show ONLY when Course Overview is selected AND current page is Course Overview
    # This ensures it appears right under the Course Overview selection, and not on other pages.
    overview_section = st.session_state.get("course_overview_section", "✅ Start Here (Checklist)")
    student_full_name = st.session_state.get("student_full_name", "")

    if choice == "Course Overview" and ("Course Overview" in current):
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Course Overview Navigation")

        st.sidebar.markdown("**Student Info**")
        student_full_name = st.sidebar.text_input(
            "Your full name (used for downloads):",
            key="student_full_name",
            placeholder="Type your name here..."
        )

        st.sidebar.markdown("**Choose a section:**")
        overview_section = st.sidebar.radio(
            label="",
            options=[
                "✅ Start Here (Checklist)",
                "📌 Course Subjects (At a Glance)",
                "📄 Download Course Syllabus",
                "🎥 Course Overview Video + Questions",
                "📝 Introduction Reflection",
            ],
            key="course_overview_section",
            label_visibility="collapsed",
        )

    return choice, overview_section, student_full_name

# ===== ONE CALL TO SET CURRENT PAGE (for highlighting) =====
def set_current_page(page_path: str):
    st.session_state["current_page_path"] = page_path

# ===== OPTIONAL: ONE-LINER INIT FOR EVERY PAGE =====
def init_course_page(title: str, page_path: str):
    """
    Call this at the TOP of every page.
    On Course Overview page, capture the return values to decide what content to show.
    """
    apply_global_styles()
    require_access()
    set_current_page(page_path)
    render_top_bar(title)

    choice, overview_section, student_full_name = render_course_sidebar()
    return overview_section
