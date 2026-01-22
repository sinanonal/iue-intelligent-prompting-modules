# ==========================================================
# pages/00_Course_Overview.py
# Course Overview checklist updates ONLY after explicit student actions
# (NO Module 1 checklist shown here)
# ==========================================================
import streamlit as st
import io
import csv
from datetime import datetime

st.set_page_config(
    page_title="Course Overview & Introduction",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ UTILITIES ------------------
def safe_strip(key: str) -> str:
    return str(st.session_state.get(key, "")).strip()

def init_flag(key: str, default: bool = False):
    if key not in st.session_state:
        st.session_state[key] = default

def build_overview_csv_bytes():
    """Downloadable CSV for Course Overview page (includes completion flags + answers)."""
    name = safe_strip("student_name")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ov_q1 = safe_strip("ov_q1")
    ov_q2 = safe_strip("ov_q2")
    ov_reflection = safe_strip("ov_reflection")

    subjects_ack = st.session_state.get("overview_subjects_completed", False)
    syllabus_ack = st.session_state.get("overview_syllabus_completed", False)
    video_ack = st.session_state.get("overview_video_completed", False)
    reflection_ack = st.session_state.get("overview_reflection_completed", False)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Name", "Timestamp",
        "Reviewed Subjects", "Opened Syllabus", "Overview Video Completed", "Intro Reflection Completed",
        "Overview Q1", "Overview Q2", "Intro Reflection Text"
    ])
    writer.writerow([
        name, ts,
        subjects_ack, syllabus_ack, video_ack, reflection_ack,
        ov_q1, ov_q2, ov_reflection
    ])
    return output.getvalue().encode("utf-8-sig")

def overview_download_block():
    """Show download if student has name and/or any content/flags."""
    name = safe_strip("student_name")
    has_any = any([
        name,
        safe_strip("ov_q1"),
        safe_strip("ov_q2"),
        safe_strip("ov_reflection"),
        st.session_state.get("overview_subjects_completed", False),
        st.session_state.get("overview_syllabus_completed", False),
        st.session_state.get("overview_video_completed", False),
        st.session_state.get("overview_reflection_completed", False),
    ])
    if has_any:
        csv_bytes = build_overview_csv_bytes()
        file_label = f"CourseOverview_Responses_{name.replace(' ', '_') or 'Student'}.csv"
        st.download_button(
            label="⬇️ Download My Course Overview Responses (CSV)",
            data=csv_bytes,
            file_name=file_label,
            mime="text/csv",
            help="Download your name, completion status, and responses as a CSV file."
        )
    else:
        st.info("Enter your name and complete at least one item to enable the download button.")

# ------------------ FLAGS (explicit completion) ------------------
init_flag("overview_subjects_completed", False)
init_flag("overview_syllabus_completed", False)
init_flag("overview_video_completed", False)
init_flag("overview_reflection_completed", False)

# ------------------ HEADER ------------------
st.title("📘 Course Overview & Introduction")
st.markdown("""
Use the left sidebar to go through each section.  
Your **Start Here checklist** updates only after you complete the required action in each section.
""")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Course Overview Navigation")
st.sidebar.markdown("**Student Info**")
st.sidebar.text_input("Your full name (used for downloads):", key="student_name")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose a section:",
    [
        "✅ Start Here (Checklist)",
        "📌 Course Subjects (At a Glance)",
        "📄 Download Course Syllabus",
        "🎥 Course Overview Video + Questions",
        "📝 Introduction Reflection",
    ]
)

# =======================================================
# 1) CHECKLIST (ONLY course overview items)
# =======================================================
if page == "✅ Start Here (Checklist)":
    st.subheader("✅ Getting Started Checklist")

    st.markdown("""
Complete these items in order. After finishing, download your responses if required by your instructor/LMS.
""")

    def status_line(done: bool, text: str):
        st.write(("✅ " if done else "⬜ ") + text)

    status_line(bool(safe_strip("student_name")), "Enter your full name (left sidebar)")
    status_line(st.session_state["overview_subjects_completed"], "Review course subjects and click “I reviewed”")
    status_line(st.session_state["overview_syllabus_completed"], "Open the syllabus and click “I opened”")
    status_line(st.session_state["overview_video_completed"], "Watch overview video + submit Q1 and Q2")
    status_line(st.session_state["overview_reflection_completed"], "Write the introduction reflection and mark complete")

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Course Overview Responses")
    overview_download_block()

    st.markdown("---")
    st.subheader("🚀 Continue")
    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/01_Module_1.py", label="➡️ Go to Module 1")
    with col2:
        st.page_link("app.py", label="🏠 Back to Home")

# =======================================================
# 2) COURSE SUBJECTS (requires explicit acknowledgement)
# =======================================================
elif page == "📌 Course Subjects (At a Glance)":
    st.subheader("📌 Course Subjects (At a Glance)")

    st.markdown("""
- Foundations of generative AI and large language models (LLMs)  
- How AI interprets prompts (intent, structure, context)  
- Core prompting patterns and prompt refinement  
- Verification and error-checking strategies  
- Responsible and ethical use in academic and professional settings  
- Applications across disciplines  
""")

    st.markdown("---")
    if st.button("✅ I reviewed the course subjects"):
        st.session_state["overview_subjects_completed"] = True
        st.success("Marked complete. You can revisit this section anytime.")

    st.markdown("---")
    st.page_link("pages/01_Module_1.py", label="➡️ Go to Module 1")

# =======================================================
# 3) SYLLABUS DOWNLOAD (requires explicit acknowledgement)
# =======================================================
elif page == "📄 Download Course Syllabus":
    st.subheader("📄 Download Course Syllabus")

    syllabus_path = "notes/Syllabus.docx"
    try:
        with open(syllabus_path, "rb") as f:
            st.download_button(
                label="Download Syllabus (DOCX)",
                data=f,
                file_name="Syllabus.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    except Exception:
        st.warning(f"Could not find `{syllabus_path}`. Make sure it exists in the `notes/` folder.")

    st.markdown("---")
    st.caption("After opening the file, click below to mark this step complete.")
    if st.button("✅ I opened and reviewed the syllabus"):
        st.session_state["overview_syllabus_completed"] = True
        st.success("Syllabus step marked complete.")

    st.markdown("---")
    st.page_link("pages/01_Module_1.py", label="➡️ Go to Module 1")

# =======================================================
# 4) OVERVIEW VIDEO + QUESTIONS (flag set only on successful submit)
# =======================================================
elif page == "🎥 Course Overview Video + Questions":
    st.subheader("🎥 Course Overview Video")

    # Replace with your actual overview video URL (YuJa/YouTube)
    st.video("PASTE_YOUR_COURSE_OVERVIEW_VIDEO_LINK_HERE")

    st.markdown("---")
    st.subheader("🧠 Quick Questions")

    with st.form("overview_video_form"):
        st.markdown("### 1) What is one thing you hope to learn in this course?")
        st.text_area("Your response:", key="ov_q1", height=120)

        st.markdown("### 2) What is one concern or question you have about using AI in coursework?")
        st.text_area("Your response:", key="ov_q2", height=120)

        submitted = st.form_submit_button("Submit Overview Questions")

    if submitted:
        if safe_strip("ov_q1") and safe_strip("ov_q2"):
            st.session_state["overview_video_completed"] = True
            st.success("Thank you! Your responses have been recorded and this step is marked complete.")
        else:
            st.warning("Please answer both questions before submitting.")

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses")
    overview_download_block()

    st.markdown("---")
    st.page_link("pages/01_Module_1.py", label="➡️ Go to Module 1")

# =======================================================
# 5) INTRO REFLECTION (requires explicit mark complete)
# =======================================================
elif page == "📝 Introduction Reflection":
    st.subheader("📝 Introduction Reflection")

    st.markdown("""
Write a short reflection (about **100–150 words**):
- How do you expect AI tools to help you in your major or future work?
- What does “responsible use” mean to you in this course?
""")

    st.text_area("Write your reflection here:", key="ov_reflection", height=220)

    st.markdown("---")
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("✅ Mark Reflection Complete"):
            if safe_strip("ov_reflection"):
                st.session_state["overview_reflection_completed"] = True
                st.success("Reflection marked complete. You can revise anytime if needed.")
            else:
                st.warning("Please write your reflection before marking it complete.")

    with col2:
        st.markdown("### ⬇️ Download Your Responses")
        overview_download_block()

    st.markdown("---")
    st.page_link("pages/01_Module_1.py", label="➡️ Go to Module 1")
