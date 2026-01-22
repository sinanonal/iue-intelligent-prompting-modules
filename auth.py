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
    for k in [
        "authorized",
        "user_email",
        "current_page_path",
        "course_contents_choice",
        "course_overview_section",
        "student_full_name",
    ]:
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
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="stSidebarNavItems"] { display: none !important; }
        [data-testid="stSidebarNavSeparator"] { display: none !important; }
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

# ===== PAGE DISCOVERY / LABELS =====
def _label_from_filename(filename: str) -> str:
    """
    Examples:
      "0_Course Overview.py" -> "Course Overview"
      "_00_Module 1.py" -> "Module 1"
    """
    base = filename.replace(".py", "")
    base = base.replace("_", " ").strip()
    base = re.sub(r"^\d+\s*", "", base).strip()   # remove leading numeric prefix (after underscores become spaces)
    return base

def _sort_key(path: Path):
    """
    Sort by leading number even if filename begins with underscores.
    Examples:
      "0_Course Overview.py" -> 0
      "_00_Module 1.py" -> 0
      "12_Module 12.py" -> 12
    """
    m = re.match(r"^_*(\d+)_", path.name)
    n = int(m.group(1)) if m else 10_000
    return (n, path.name.lower())

@st.cache_data
def build_pages_index():
    """
    Returns an ordered mapping:
    Home, Course Overview, Module 1..13 (if present), then any remaining pages.
    """
    detected = {}

    # Always include Home
    detected["Home"] = "app.py"

    # Detect all .py files in /pages (INCLUDING those starting with "_")
    if PAGES_DIR.exists():
        for p in sorted(PAGES_DIR.glob("*.py"), key=_sort_key):
            # Skip only double-underscore utilities (optional rule)
            if p.name.startswith("__"):
                continue
            label = _label_from_filename(p.name)
            detected[label] = str(p).replace("\\", "/")

    # Reorder into your intended structure
    ordered = {}
    if "Home" in detected:
        ordered["Home"] = detected["Home"]

    if "Course Overview" in detected:
        ordered["Course Overview"] = detected["Course Overview"]

    for i in range(1, 14):
        k = f"Module {i}"
        if k in detected:
            ordered[k] = detected[k]

    for k, v in detected.items():
        if k in ordered:
            continue
        ordered[k] = v

    return ordered

# ===== PATH RESOLUTION (prevents "click -> back to Home") =====
def _canonicalize_filename(path: str) -> str:
    # compare by filename ignoring spaces/underscores and case
    name = Path(path).name.lower()
    name = re.sub(r"[\s_]+", "", name)
    return name

def resolve_current_path(page_path: str) -> str:
    """
    Convert a page_path passed by a page into the exact path that
    build_pages_index() knows about. Prevents default-to-Home loop.
    """
    pages = build_pages_index()
    vals = list(pages.values())

    # Exact match
    if page_path in vals:
        return page_path

    # Match by filename (case-insensitive)
    want = Path(page_path).name.lower()
    for v in vals:
        if Path(v).name.lower() == want:
            return v

    # Match by canonical filename (ignore spaces/underscores)
    want2 = _canonicalize_filename(page_path)
    for v in vals:
        if _canonicalize_filename(v) == want2:
            return v

    return page_path

def set_current_page(page_path: str):
    st.session_state["current_page_path"] = resolve_current_path(page_path)

# ===== SIDEBAR (Course Contents + Course Overview sub-navigation) =====
def render_course_sidebar():
    st.sidebar.markdown("## 📚 Course Contents")

    pages = build_pages_index()
    labels = list(pages.keys())

    current = st.session_state.get("current_page_path", "app.py")
    current = resolve_current_path(current)

    # Default selection = current page if found
    vals = list(pages.values())
    try:
        default_index = vals.index(current)
    except ValueError:
        default_index = 0

    choice = st.sidebar.radio(
        label="",
        options=labels,
        index=default_index,
        key="course_contents_choice",
        label_visibility="collapsed",
    )

    target = pages[choice]

    # Only navigate if the target is different (prevents loops)
    if resolve_current_path(target) != resolve_current_path(current):
        st.switch_page(target)

    # ---- Course Overview sub-navigation (only on the real Course Overview page)
    course_overview_path = pages.get("Course Overview", "")

    overview_section = st.session_state.get("course_overview_section", "✅ Start Here (Checklist)")
    student_full_name = st.session_state.get("student_full_name", "")

    if choice == "Course Overview" and resolve_current_path(current) == resolve_current_path(course_overview_path):
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Course Overview Navigation")

        st.sidebar.markdown("**Student Info**")
        st.sidebar.text_input(
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

# ===== ONE-LINER INIT FOR EVERY PAGE =====
def init_course_page(title: str, page_path: str):
    """
    Call at the TOP of every page.
    Returns the Course Overview selected section (only meaningful on Course Overview page).
    """
    apply_global_styles()
    require_access()
    set_current_page(page_path)
    render_top_bar(title)
    _, overview_section, _ = render_course_sidebar()
    return overview_section
