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

# Draw: global styles + login gate + top bar + Course Contents sidebar
init_course_page("Module 1 — Foundations", "pages/01_Module_1.py")

# ------------------ UTILITIES ------------------
def safe_strip(key: str) -> str:
    return str(st.session_state.get(key, "")).strip()

def word_count(text: str) -> int:
    return len([w for w in text.split() if w.strip()])

def build_csv_bytes():
    """Create a CSV of the student's Module 1 responses and return as bytes (Excel-friendly)."""
    name = safe_strip("student_full_name")  # comes from Course Overview sidebar
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Video quiz
    q1 = safe_strip("q1_intro")
    q2 = safe_strip("q2_slide")

    # Prompt Lab
    m1_prompt_used = safe_strip("m1_prompt_used")
    m1_ai_response = safe_strip("m1_ai_response")
    m1_prompt_reflection = safe_strip("m1_prompt_reflection")

    # Module reflection
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
    """Show a downloadable CSV if we have at least a name or any answers."""
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
            help="Downloads your name and answers as a CSV file you can submit or keep.",
            use_container_width=True
        )
    else:
        st.info("Enter your name in Course Overview (sidebar) and complete at least one item to enable downloads.")

def goto_module_2_button():
    st.markdown("---")
    if st.button("➡️ Go to Module 2", use_container_width=True):
        # Try common filenames so it won't break if you named it differently
        candidates = [
            "pages/02_Module_2.py",
            "pages/02_Module 2.py",
            "pages/Module 2.py",
            "pages/02_Module_2_.py",
        ]
        for path in candidates:
            try:
                st.switch_page(path)
                return
            except Exception:
                pass
        st.info("Module 2 file was not found. Create it (recommended name: `pages/02_Module_2.py`).")

def render_mcq_block(section_id: str, questions: list[dict]):
    """Render 3 MCQs for a section."""
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

    if st.button("Check Answers", key=f"m1_{section_id}_mcq_check"):
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

# ------------------ HEADER ------------------
st.title("📘 Tier 1 — Foundations of Generative AI")
st.header("Module 1 — Foundations of Generative AI")
st.markdown("""
This module introduces the core ideas behind generative AI and large language models (LLMs).
Use the menu on the left to explore each subject in this module.
""")

# ------------------ MODULE 1 NAV (SECONDARY SIDEBAR MENU) ------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### Module 1 Navigation")

sidebar_pages = [
    "✅ Start Here (Checklist)",
    "🎧 Lecture Video / Voice Recording",
    "📖 Readings (Chapter Sections 1–11)",
    "🧪 Prompt Lab (ChatGPT Practice)",
    "📝 Reflection Assignment",
]

page = st.sidebar.radio("Choose a page:", sidebar_pages, key="m1_nav")

# ------------------ READING CONTENT ------------------
READINGS = {
    "1. Introduction: Entering the Era of Intelligent Assistance": {
        "id": "s1_intro",
        "text": """
### Reading
Over the past few years, artificial intelligence has shifted from a specialized research domain to a practical tool used across industries, classrooms, and everyday life. Students now encounter AI not in abstract discussions about the future, but in concrete forms such as writing assistants, recommendation engines, chatbots, and automated tutoring systems. Among these tools, generative AI has had the greatest impact. These systems do not simply categorize information; they produce new content, generate explanations, and help learners explore unfamiliar subjects with remarkable fluency. As a result, the ability to understand and communicate with these systems—through clear, strategic prompting—has emerged as an essential academic and professional skill.

This chapter provides the foundational knowledge you need before learning specific prompting techniques in later modules. It explains what generative AI is, how large language models work, what they can and cannot do, and why your instructions matter so much. Although AI often appears intelligent, its behavior is driven by patterns rather than genuine understanding. Recognizing this distinction will help you use AI responsibly and effectively.

Because this course is interdisciplinary, the examples in this chapter draw from fields such as engineering, business, the arts, psychology, and health sciences. Regardless of your major, the concepts you encounter here will provide a base from which you can build advanced prompting skills in the weeks ahead.
""",
        "mcq": [
            {
                "q": "What is the main reason generative AI has had a strong impact compared to many other AI tools?",
                "options": [
                    "It can access private databases and real-time systems by default",
                    "It produces new content and explanations, not just categories or labels",
                    "It replaces the need for learning in academic settings",
                    "It guarantees accurate and unbiased information"
                ],
                "answer": "It produces new content and explanations, not just categories or labels"
            },
            {
                "q": "According to the reading, what skill is becoming essential for academic and professional work?",
                "options": [
                    "Writing code for AI models from scratch",
                    "Clear, strategic prompting to communicate with AI systems",
                    "Memorizing AI definitions and terminology",
                    "Avoiding AI tools in all coursework"
                ],
                "answer": "Clear, strategic prompting to communicate with AI systems"
            },
            {
                "q": "Why does the chapter emphasize that AI behavior is driven by patterns rather than genuine understanding?",
                "options": [
                    "To show that AI is always wrong",
                    "To help students use AI responsibly and interpret output correctly",
                    "To discourage interdisciplinary use of AI",
                    "To argue that AI cannot produce fluent language"
                ],
                "answer": "To help students use AI responsibly and interpret output correctly"
            }
        ]
    },

    # NOTE: Keep the rest of your READINGS dict exactly as you already have it.
    # I am not repeating sections 2–11 here to keep this message manageable.
    # Paste your existing sections 2–11 right below this comment.
}

# =======================================================
# START PAGE: CHECKLIST
# =======================================================
if page == "✅ Start Here (Checklist)":
    st.subheader("✅ Module 1 Checklist")

    st.markdown("""
Use this checklist to complete Module 1 in order. After completing the Module assignments, download your responses and submit the file on Blackboard.  
You can return here anytime to see what is still missing.
""")

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
    st.markdown("### ⬇️ Download Your Responses (Video Questions + Prompt Lab + Reflection)")
    section_download_block()
    goto_module_2_button()

# =======================================================
# LECTURE VIDEO PAGE
# =======================================================
elif page == "🎧 Lecture Video / Voice Recording":
    st.subheader("🎧 Lecture for Module 1 — Foundations of Generative AI")

    st.markdown("### 📄 Downloadable PDF Notes")
    pdf_path = "notes/Intelligent_Prompting.pdf"  # adjust if needed
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
    with st.expander("📝 Lecture Transcript (click to open)", expanded=False):
        st.markdown("*Replace this placeholder with your real transcript after recording the lecture.*")

    st.markdown("---")
    st.markdown("## 🧠 Video Questions")

    with st.form("video_questions_form"):
        st.markdown("### **1) Please briefly introduce yourself — your major, hometown, interests, etc.**")
        st.text_area("Your response:", key="q1_intro", height=120)

        st.markdown("### **2) What did you notice in this slide?**")
        st.text_area("Your response:", key="q2_slide", height=120)

        submitted = st.form_submit_button("Submit Video Questions")

    if submitted:
        if safe_strip("q1_intro") and safe_strip("q2_slide"):
            st.success("Thank you! Your responses have been recorded.")
        else:
            st.warning("Please answer both questions before submitting.")

    goto_module_2_button()

# =======================================================
# READINGS PAGE
# =======================================================
elif page == "📖 Readings (Chapter Sections 1–11)":
    st.subheader("📖 Module 1 Readings (Sections 1–11)")

    if len(READINGS) == 1:
        st.info("Paste your remaining reading sections (2–11) into the READINGS dict to enable the dropdown.")
    else:
        st.markdown("""
Use the dropdown to select a reading section.  
Each section includes **3 multiple-choice questions** to check understanding.
""")
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
**Goal:** Practice writing clear prompts and reflecting on what improved.

**What to submit in this app:**
1) The prompt you used  
2) The AI response  
3) A short reflection (3–5 sentences)
""")

    st.markdown("### Step 1 — Open ChatGPT")
    try:
        st.link_button("Open ChatGPT", "https://chat.openai.com/")
    except Exception:
        st.markdown("Open ChatGPT: https://chat.openai.com/")

    st.markdown("---")
    st.markdown("### Step 2 — Choose ONE prompt below and run it in ChatGPT")

    prompt_choice = st.radio(
        "Pick a prompt to copy into ChatGPT:",
        [
            "Option A — Explain Generative AI (clarity + constraints)",
            "Option B — Verification Habit (check what to verify)",
            "Option C — Improve a vague prompt (before/after)"
        ],
        index=0
    )

    if prompt_choice.startswith("Option A"):
        suggested_prompt = (
            "Explain **generative AI** to a first-year college student in my major (**[your major]**). "
            "Use: (1) 3 bullet points, (2) 1 real example in my field, and (3) one limitation of LLMs. "
            "Keep it under 180 words."
        )
    elif prompt_choice.startswith("Option B"):
        suggested_prompt = (
            "I will paste a short claim about AI. Tell me: "
            "(1) what parts might be incorrect or oversimplified, "
            "(2) what I should verify, and "
            "(3) where I could verify it (types of sources). "
            "Keep it under 150 words.\n\nClaim: [paste your claim here]"
        )
    else:
        suggested_prompt = (
            "Here is a vague prompt I wrote: “[paste it here]”.\n\n"
            "1) Rewrite it to be clear and specific (include constraints and output format).\n"
            "2) Explain what you changed and why.\n"
            "3) Provide 2 alternative versions for different audiences."
        )

    st.text_area(
        "Suggested prompt (copy this into ChatGPT, then customize it):",
        value=suggested_prompt,
        height=170
    )

    st.markdown("---")
    st.markdown("### Step 3 — Paste your work here")

    st.text_area(
        "✅ Paste the exact prompt you used in ChatGPT:",
        key="m1_prompt_used",
        height=140,
        placeholder="Paste your final prompt here..."
    )

    st.text_area(
        "✅ Paste the AI response you received:",
        key="m1_ai_response",
        height=220,
        placeholder="Paste the AI response here..."
    )

    st.markdown("---")
    st.markdown("### Step 4 — Reflection (3–5 sentences)")
    st.caption("Aim for ~50–120 words.")
    st.text_area(
        "What worked well? What would you change to make your prompt clearer or more specific?",
        key="m1_prompt_reflection",
        height=160,
        placeholder="Write 3–5 sentences..."
    )

    pr_wc = word_count(safe_strip("m1_prompt_reflection"))
    st.caption(f"Prompt Lab reflection word count: {pr_wc}")

    st.markdown("---")
    if st.button("Check Prompt Lab Completeness", key="m1_promptlab_check", use_container_width=True):
        missing = []
        if not safe_strip("m1_prompt_used"):
            missing.append("your prompt")
        if not safe_strip("m1_ai_response"):
            missing.append("the AI response")
        if not safe_strip("m1_prompt_reflection"):
            missing.append("your reflection")
        if missing:
            st.warning("Please add: " + ", ".join(missing) + ".")
        else:
            st.success("Prompt Lab looks complete. You can download your responses below.")

    st.markdown("---")
    section_download_block()
    goto_module_2_button()

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

    if st.button("Preview Reflection", key="m1_reflection_preview", use_container_width=True):
        if safe_strip("reflection_m1"):
            st.success("### Reflection Preview:")
            st.write(safe_strip("reflection_m1"))
        else:
            st.warning("Write a reflection to preview.")

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses (Video Questions + Prompt Lab + Reflection)")
    section_download_block()
    goto_module_2_button()
