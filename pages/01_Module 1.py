import streamlit as st
import io
import csv
from datetime import datetime

from auth import init_course_page

st.set_page_config(
    page_title="Module 1 — Foundations of Generative AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# IMPORTANT: must match your real filename exactly
init_course_page("Module 1 — Foundations", "pages/01_Module 1.py")

# ------------------ UTILITIES ------------------
def safe_strip(key: str) -> str:
    return str(st.session_state.get(key, "")).strip()

def word_count(text: str) -> int:
    return len([w for w in text.split() if w.strip()])

def build_csv_bytes():
    name = safe_strip("student_full_name")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    q1 = safe_strip("q1_intro")
    q2 = safe_strip("q2_slide")

    m1_prompt_used = safe_strip("m1_prompt_used")
    m1_ai_response = safe_strip("m1_ai_response")
    m1_prompt_reflection = safe_strip("m1_prompt_reflection")

    reflection = safe_strip("reflection_m1")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Name", "Timestamp",
        "Q1: Intro", "Q2: Slide Observation",
        "Prompt Lab: Prompt Used", "Prompt Lab: AI Response", "Prompt Lab: Reflection",
        "Module Reflection"
    ])
    writer.writerow([
        name, ts,
        q1, q2,
        m1_prompt_used, m1_ai_response, m1_prompt_reflection,
        reflection
    ])
    return output.getvalue().encode("utf-8-sig")

def section_download_block():
    name = safe_strip("student_full_name")
    has_any = any([
        name,
        safe_strip("q1_intro"),
        safe_strip("q2_slide"),
        safe_strip("m1_prompt_used"),
        safe_strip("m1_ai_response"),
        safe_strip("m1_prompt_reflection"),
        safe_strip("reflection_m1"),
    ])

    if has_any:
        csv_bytes = build_csv_bytes()
        file_label = f"Module1_Responses_{name.replace(' ', '_') or 'Student'}.csv"
        st.download_button(
            label="⬇️ Download My Module 1 Responses (CSV)",
            data=csv_bytes,
            file_name=file_label,
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("Enter your name in Course Overview (sidebar) and complete at least one item to enable downloads.")

# ------------------ HEADER ------------------
st.title("📘 Tier 1 — Foundations of Generative AI")
st.header("Module 1 — Foundations of Generative AI")
st.markdown("""
Use the menu on the left to explore each subject in this module.
""")

# ------------------ MODULE 1 NAV (secondary sidebar menu) ------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### Module 1 Navigation")

sidebar_pages = [
    "✅ Start Here (Checklist)",
    "🎧 Lecture Video / Voice Recording",
    "📖 Readings (Chapter Sections)",
    "🧪 Prompt Lab (ChatGPT Practice)",
    "📝 Reflection Assignment",
]
page = st.sidebar.radio("Choose a page:", sidebar_pages, key="m1_nav")

# ------------------ READINGS (keep short here; paste your full 1–11 dict if you want) ------------------
READINGS = {
    "1. Introduction: Entering the Era of Intelligent Assistance": {
        "id": "s1_intro",
        "text": """
### Reading
Generative AI has become a practical tool used across fields. It can generate new content and explanations.
Because it generates plausible text rather than verified truth, students must learn to prompt clearly and evaluate output.
""",
        "mcq": [
            {
                "q": "Generative AI is different from many traditional AI systems because it can:",
                "options": [
                    "Only classify and label data",
                    "Create new content and explanations",
                    "Guarantee perfect factual accuracy",
                    "Access private databases by default",
                ],
                "answer": "Create new content and explanations",
            },
            {
                "q": "Why is critical evaluation important when using AI?",
                "options": [
                    "Because AI output can sound confident but be incorrect",
                    "Because AI refuses to answer questions",
                    "Because AI always gives citations",
                    "Because AI never makes mistakes",
                ],
                "answer": "Because AI output can sound confident but be incorrect",
            },
            {
                "q": "What skill is emphasized in this course?",
                "options": [
                    "Clear, strategic prompting",
                    "Avoiding AI completely",
                    "Building AI models from scratch",
                    "Memorizing definitions only",
                ],
                "answer": "Clear, strategic prompting",
            },
        ],
    },
}

def render_mcq_block(section_id: str, questions: list[dict]):
    st.markdown("### 🧠 Check Your Understanding (3 Questions)")
    selected = []
    for i, item in enumerate(questions, start=1):
        key = f"m1_{section_id}_mcq_{i}"
        choice = st.radio(
            f"{i}) {item['q']}",
            item["options"],
            index=None,
            key=key
        )
        selected.append(choice)

    if st.button("Check Answers", key=f"m1_{section_id}_mcq_check", use_container_width=True):
        correct = 0
        for i, item in enumerate(questions):
            if selected[i] == item["answer"]:
                correct += 1
        if correct == len(questions):
            st.success("✅ Excellent! You answered all questions correctly.")
        else:
            st.warning(f"You answered {correct}/{len(questions)} correctly. Review the reading and try again.")

def render_reading_section(title: str, body: str, section_id: str, questions: list[dict]):
    st.subheader(title)
    st.markdown(body)
    render_mcq_block(section_id, questions)
    st.markdown("---")

# =======================================================
# CHECKLIST
# =======================================================
if page == "✅ Start Here (Checklist)":
    st.subheader("✅ Module 1 Checklist")

    name = safe_strip("student_full_name")
    q1 = safe_strip("q1_intro")
    q2 = safe_strip("q2_slide")

    prompt_used = safe_strip("m1_prompt_used")
    ai_resp = safe_strip("m1_ai_response")
    prompt_ref = safe_strip("m1_prompt_reflection")

    refl = safe_strip("reflection_m1")
    refl_wc = word_count(refl)

    def status_line(done: bool, text: str):
        st.write(("✅ " if done else "⬜ ") + text)

    status_line(bool(name), "Enter your full name (Course Overview sidebar)")
    status_line(bool(q1 and q2), "Watch the video + answer Q1 and Q2")
    status_line(bool(prompt_used and ai_resp and prompt_ref), "Complete Prompt Lab (prompt + AI response + reflection)")
    status_line(150 <= refl_wc <= 250, "Write the 150–250 word Module Reflection")

    st.markdown("---")
    section_download_block()

# =======================================================
# LECTURE VIDEO
# =======================================================
elif page == "🎧 Lecture Video / Voice Recording":
    st.subheader("🎧 Lecture for Module 1 — Foundations of Generative AI")

    st.markdown("### 📄 Downloadable PDF Notes")
    pdf_path = "notes/Intelligent_Prompting.pdf"
    try:
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download Module 1 Notes (PDF)",
                data=pdf_file,
                file_name="Intelligent_Prompting.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    except Exception:
        st.warning(f"PDF notes not found. Add your file to `{pdf_path}` (or update the path in the code).")

    st.markdown("### 📺 Video Lecture")
    st.video("https://siue.yuja.com/Dashboard/Permalink?authCode=167158588&b=14078175&linkType=video")

    st.markdown("---")
    st.markdown("## 🧠 Video Questions")

    with st.form("video_questions_form"):
        st.markdown("### 1) Please briefly introduce yourself — your major, hometown, interests, etc.")
        st.text_area("Your response:", key="q1_intro", height=120)

        st.markdown("### 2) What did you notice in this slide?")
        st.text_area("Your response:", key="q2_slide", height=120)

        submitted = st.form_submit_button("Submit Video Questions")

    if submitted:
        if safe_strip("q1_intro") and safe_strip("q2_slide"):
            st.success("Thank you! Your responses have been recorded.")
        else:
            st.warning("Please answer both questions before submitting.")

    st.markdown("---")
    section_download_block()

# =======================================================
# READINGS
# =======================================================
elif page == "📖 Readings (Chapter Sections)":
    st.subheader("📖 Module 1 Readings")

    section_title = st.selectbox("Choose a reading section:", list(READINGS.keys()))
    section = READINGS[section_title]

    render_reading_section(
        title=section_title,
        body=section["text"],
        section_id=section["id"],
        questions=section["mcq"]
    )

# =======================================================
# PROMPT LAB
# =======================================================
elif page == "🧪 Prompt Lab (ChatGPT Practice)":
    st.subheader("🧪 Prompt Lab — Practice in ChatGPT (Module 1)")

    st.markdown("""
**Submit here:**
1) The prompt you used  
2) The AI response  
3) A short reflection (3–5 sentences)
""")

    st.text_area("✅ Paste the exact prompt you used in ChatGPT:", key="m1_prompt_used", height=140)
    st.text_area("✅ Paste the AI response you received:", key="m1_ai_response", height=220)
    st.text_area("Reflection (3–5 sentences):", key="m1_prompt_reflection", height=160)

    st.markdown("---")
    section_download_block()

# =======================================================
# REFLECTION ASSIGNMENT
# =======================================================
elif page == "📝 Reflection Assignment":
    st.subheader("📝 Module 1 Reflection")

    st.markdown("""
Submit a **150–250 word** reflection:
- What did you learn?
- How could generative AI help in your major?
- What questions do you still have?
""")

    st.text_area("Write your reflection here:", height=220, key="reflection_m1")

    wc = word_count(safe_strip("reflection_m1"))
    st.caption(f"Word count: {wc} (target 150–250)")
    if wc > 0 and (wc < 150 or wc > 250):
        st.warning("Your reflection is outside the 150–250 word range. Please revise.")

    st.markdown("---")
    section_download_block()
