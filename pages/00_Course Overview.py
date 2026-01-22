# ==========================================================
# pages/00_Course_Overview_and_Introduction.py
# (Place this file inside your Streamlit app's /pages folder)
# ==========================================================

import streamlit as st
import io
import csv
from datetime import datetime

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Course Overview & Introduction", layout="wide")

# ------------------ UTILITIES ------------------
def safe_strip(key: str) -> str:
    return str(st.session_state.get(key, "")).strip()

def build_overview_csv_bytes():
    """Create a CSV of the student's Course Overview responses and return as bytes."""
    name = safe_strip("student_name")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Overview video questions
    ov_q1 = safe_strip("ov_q1")
    ov_q2 = safe_strip("ov_q2")

    # Intro reflection (short)
    ov_reflection = safe_strip("ov_reflection")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Timestamp", "Overview Q1", "Overview Q2", "Intro Reflection"])
    writer.writerow([name, ts, ov_q1, ov_q2, ov_reflection])
    return output.getvalue().encode("utf-8-sig")

def overview_download_block():
    name = safe_strip("student_name")
    has_any = any([
        name,
        safe_strip("ov_q1"),
        safe_strip("ov_q2"),
        safe_strip("ov_reflection"),
    ])

    if has_any:
        csv_bytes = build_overview_csv_bytes()
        file_label = f"CourseOverview_Responses_{name.replace(' ', '_') or 'Student'}.csv"
        st.download_button(
            label="⬇️ Download My Course Overview Responses (CSV)",
            data=csv_bytes,
            file_name=file_label,
            mime="text/csv",
            help="Downloads your name and answers as a CSV file you can submit or keep."
        )
    else:
        st.info("Fill in your name and at least one answer to enable the download button.")

def goto_module_1_button():
    st.markdown("---")
    if st.button("➡️ Go to Module 1"):
        try:
            # Adjust the exact filename to match your Module 1 page file in /pages
            # Examples:
            # st.switch_page("pages/01_Module_1.py")
            # st.switch_page("pages/Module 1.py")
            st.switch_page("pages/01_Module_1.py")
        except Exception:
            st.info("Module 1 page was not found. Make sure your Module 1 file exists in `/pages` and update the path here.")

# ------------------ HEADER ------------------
st.title("📘 Intelligent Prompting Course")
st.header("Course Overview & Introduction")

st.markdown("""
Welcome to the course. This page helps you get started:
- Review the course subjects (at a glance)
- Download the course syllabus
- Watch the course overview video
- Answer two short questions and write a brief reflection
Then you can proceed to **Module 1**.
""")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Course Navigation")

st.sidebar.markdown("**Student Info**")
st.sidebar.text_input("Your full name (for downloads):", key="student_name")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose a section:",
    [
        "✅ Start Here (Checklist)",
        "📌 Course Subjects (At a Glance)",
        "📄 Download Course Syllabus",
        "🎥 Course Overview Video",
        "📝 Introduction Reflection",
    ]
)

# =======================================================
# 1) START HERE (CHECKLIST)
# =======================================================
if page == "✅ Start Here (Checklist)":
    st.subheader("✅ Getting Started Checklist")

    name = safe_strip("student_name")
    q1 = safe_strip("ov_q1")
    q2 = safe_strip("ov_q2")
    refl = safe_strip("ov_reflection")

    def status_line(done: bool, text: str):
        st.write(("✅ " if done else "⬜ ") + text)

    status_line(bool(name), "Enter your full name (left sidebar)")
    status_line(True, "Review course subjects (At a Glance)")
    status_line(True, "Download and skim the syllabus")
    status_line(bool(q1 and q2), "Watch the overview video + answer Q1 and Q2")
    status_line(bool(refl), "Write a brief introduction reflection")

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses")
    overview_download_block()

    goto_module_1_button()

# =======================================================
# 2) COURSE SUBJECTS (AS IS)
# =======================================================
elif page == "📌 Course Subjects (At a Glance)":
    st.subheader("📌 Course Subjects (At a Glance)")

    # Replace this list with your exact course subject list “as is”
    # (I’m putting a placeholder structure you can paste into directly.)
    st.markdown("""
### Topics you will learn in this course
- Foundations of generative AI and large language models (LLMs)
- How models interpret prompts (intent, structure, context)
- Core prompting patterns and prompt refinement
- Verification and error-checking strategies
- Multimodal prompting (text + images, later modules if used)
- Responsible and ethical use in academic and professional work
- Real-world applications across disciplines
""")

    st.info("If you paste your full official course subject list, I can format it here exactly as you want (bullets, numbered list, or weekly view).")

    goto_module_1_button()

# =======================================================
# 3) DOWNLOAD COURSE SYLLABUS
# =======================================================
elif page == "📄 Download Course Syllabus":
    st.subheader("📄 Download Course Syllabus")

    # Put your syllabus PDF or DOCX under /notes (or any folder you prefer)
    # Example paths:
    # syllabus_path = "notes/Course_Syllabus.pdf"
    # syllabus_path = "notes/Syllabus.docx"
    syllabus_path = "notes/Syllabus.docx"  # change if needed

    st.markdown("Click below to download the syllabus.")

    try:
        with open(syllabus_path, "rb") as f:
            # Use an appropriate filename extension for what you upload
            st.download_button(
                label="Download Course Syllabus",
                data=f,
                file_name=syllabus_path.split("/")[-1],
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    except Exception:
        st.warning(
            f"Syllabus file not found at `{syllabus_path}`.\n\n"
            "Fix: Put your syllabus file in that location or update `syllabus_path` in the code."
        )

    goto_module_1_button()

# =======================================================
# 4) COURSE OVERVIEW VIDEO + 2 QUESTIONS
# =======================================================
elif page == "🎥 Course Overview Video":
    st.subheader("🎥 Course Overview Video")

    # Replace with your YuJa or YouTube link
    st.video("https://siue.yuja.com/")  # <-- replace with your actual course overview video permalink

    st.markdown("---")
    st.markdown("## 🧠 Overview Video Questions")

    with st.form("overview_video_form"):
        st.markdown("### 1) What is one thing you hope to learn in this course?")
        st.text_area("Your response:", key="ov_q1", height=120)

        st.markdown("### 2) What is one concern or question you have about using AI in coursework?")
        st.text_area("Your response:", key="ov_q2", height=120)

        submitted = st.form_submit_button("Submit Overview Questions")

    if submitted:
        if safe_strip("ov_q1") and safe_strip("ov_q2"):
            st.success("Thank you! Your responses have been recorded.")
        else:
            st.warning("Please answer both questions before submitting.")

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses")
    overview_download_block()

    goto_module_1_button()

# =======================================================
# 5) INTRODUCTION REFLECTION
# =======================================================
elif page == "📝 Introduction Reflection":
    st.subheader("📝 Introduction Reflection")

    st.markdown("""
Write a short reflection (about 100–150 words):
- How do you expect AI tools to help you in your major or future work?
- What does “responsible use” mean to you in this course?
""")

    st.text_area("Write your reflection here:", key="ov_reflection", height=220)

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses")
    overview_download_block()

    goto_module_1_button()
