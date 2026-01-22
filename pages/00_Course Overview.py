# ==========================================================
# pages/00_Course_Overview.py  (Option A: explicit completion flags)
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
    """Downloadable CSV for Course Overview page (student intro + questions + reflection)."""
    name = safe_strip("student_name")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ov_q1 = safe_strip("ov_q1")
    ov_q2 = safe_strip("ov_q2")
    ov_reflection = safe_strip("ov_reflection")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Timestamp", "Overview Q1", "Overview Q2", "Intro Reflection"])
    writer.writerow([name, ts, ov_q1, ov_q2, ov_reflection])
    return output.getvalue().encode("utf-8-sig")

def overview_download_block():
    name = safe_strip("student_name")
    has_any = any([name, safe_strip("ov_q1"), safe_strip("ov_q2"), safe_strip("ov_reflection")])
    if has_any:
        csv_bytes = build_overview_csv_bytes()
        file_label = f"CourseOverview_Responses_{name.replace(' ', '_') or 'Student'}.csv"
        st.download_button(
            label="⬇️ Download My Course Overview Responses (CSV)",
            data=csv_bytes,
            file_name=file_label,
            mime="text/csv",
            help="Download your name and answers as a CSV file you can submit or keep."
        )
    else:
        st.info("Enter your name and at least one answer to enable the download button.")

# ------------------ SESSION FLAGS (Option A) ------------------
# Course Overview flags
init_flag("overview_video_completed", False)
init_flag("overview_reflection_completed", False)

# Module 1 flags (set inside Module 1 page)
init_flag("m1_video_questions_completed", False)
init_flag("m1_prompt_lab_completed", False)
init_flag("m1_reflection_completed", False)

# ------------------ HEADER ------------------
st.title("📘 Course Overview & Introduction")
st.markdown("""
This page helps you get started:
- Review the course subjects
- Download the syllabus
- Watch the course overview video
- Answer two quick questions and write a brief reflection  
Then continue to **Module 1**.
""")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Course Navigation")
st.sidebar.markdown("**Student Info**")
st.sidebar.text_input("Your full name (used for downloads):", key="student_name")

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
# 1) CHECKLIST (uses explicit completion flags)
# =======================================================
if page == "✅ Start Here (Checklist)":
    st.subheader("✅ Getting Started Checklist")

    def status_line(done: bool, text: str):
        st.write(("✅ " if done else "⬜ ") + text)

    status_line(bool(safe_strip("student_name")), "Enter your full name (left sidebar)")
    status_line(True, "Review course subjects (At a Glance)")
    status_line(True, "Download and skim the syllabus")
    status_line(st.session_state.get("overview_video_completed", False), "Watch the course overview video + submit Q1 and Q2")
    status_line(st.session_state.get("overview_reflection_completed", False), "Write the introduction reflection")

    st.markdown("---")
    st.subheader("✅ Module 1 Progress (auto-updated as you complete Module 1)")
    status_line(st.session_state.get("m1_video_questions_completed", False), "Module 1: Video Questions submitted (Q1 + Q2)")
    status_line(st.session_state.get("m1_prompt_lab_completed", False), "Module 1: Prompt Lab complete (prompt + AI response + reflection)")
    status_line(st.session_state.get("m1_reflection_completed", False), "Module 1: Reflection complete (within required word range)")

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Course Overview Responses")
    overview_download_block()

    st.markdown("---")
    st.markdown("### 🚀 Continue")
    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/01_Module_1.py", label="➡️ Go to Module 1")
    with col2:
        st.page_link("app.py", label="🏠 Back to Home")

# =======================================================
# 2) SUBJECTS
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
    st.page_link("pages/01_Module_1.py", label="➡️ Go to Module 1")

# =======================================================
# 3) SYLLABUS DOWNLOAD
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
    st.page_link("pages/01_Module_1.py", label="➡️ Go to Module 1")

# =======================================================
# 4) OVERVIEW VIDEO + QUESTIONS (sets flag only on successful submit)
# =======================================================
elif page == "🎥 Course Overview Video + Questions":
    st.subheader("🎥 Course Overview Video")

    # Replace with your actual overview video link (YuJa permalink or YouTube)
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
            st.success("Thank you! Your responses have been recorded.")
        else:
            st.warning("Please answer both questions before submitting.")

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses")
    overview_download_block()

    st.markdown("---")
    st.page_link("pages/01_Module_1.py", label="➡️ Go to Module 1")

# =======================================================
# 5) INTRO REFLECTION (sets flag only when student explicitly submits/marks complete)
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
        if st.button("Mark Reflection Complete"):
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
