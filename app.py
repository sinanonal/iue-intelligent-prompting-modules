
import streamlit as st
import io
import csv
from datetime import datetime

# -----------------------------------------
#   TIER 1 — Foundations of Generative AI
#   MODULE 1 — Foundations of Generative AI
# -----------------------------------------

st.set_page_config(page_title="Module 1 — Foundations of Generative AI",
                   layout="wide")

# ------------------ UTILITIES ------------------
def build_csv_bytes():
    """Create a CSV of the student's Module 1 responses and return as bytes."""
    name = st.session_state.get("student_name", "").strip()
    q1 = st.session_state.get("q1_intro", "").strip()
    q2 = st.session_state.get("q2_slide", "").strip()
    reflection = st.session_state.get("reflection_m1", "").strip()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Timestamp", "Q1: Intro", "Q2: Slide Observation", "Reflection"])
    writer.writerow([name, ts, q1, q2, reflection])
    return output.getvalue().encode("utf-8-sig")  # Excel-friendly

def section_download_block():
    """Reusable block to show a downloadable CSV if we have at least a name or any answers."""
    name = st.session_state.get("student_name", "").strip()
    q1 = st.session_state.get("q1_intro", "").strip()
    q2 = st.session_state.get("q2_slide", "").strip()
    reflection = st.session_state.get("reflection_m1", "").strip()

    # Only show the button if there is something to download
    if any([name, q1, q2, reflection]):
        csv_bytes = build_csv_bytes()
        file_label = f"Module1_Responses_{name.replace(' ', '_') or 'Student'}.csv"
        st.download_button(
            label="⬇️ Download My Module 1 Responses (CSV)",
            data=csv_bytes,
            file_name=file_label,
            mime="text/csv",
            help="Downloads your name and answers as a CSV file you can submit or keep."
        )
    else:
        st.info("Fill in your name and at least one answer to enable the download button.")

def goto_module_2_button():
    st.markdown("---")
    if st.button("➡️ Go to Module 2"):
        # If you convert to a multipage app with pages/Module 2.py, this will try to switch.
        try:
            # Example page path or page title (adjust to your exact filename or title)
            st.switch_page("pages/Module 2.py")
        except Exception:
            # Fallback if multipage isn't set up yet
            st.info("Module 2 will be available soon. (To enable direct navigation, create `pages/Module 2.py`.)")

# ------------------ HEADER ------------------
st.title("📘 Tier 1 — Foundations of Generative AI")
st.header("Module 1 — Foundations of Generative AI")
st.markdown("""
This module introduces the core ideas behind generative AI and large language models (LLMs).
Use the menu on the left to explore each subject in this module.
""")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Module 1 Subjects")

# NEW: capture student name globally so it’s available for downloads
st.sidebar.markdown("**Student Info**")
st.sidebar.text_input("Your full name (for downloads):", key="student_name")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose a subject:",
    [
        "🎧 Lecture Video / Voice Recording",
        "What generative AI is and how it works",
        "What LLMs can and cannot do",
        "Everyday uses of AI across different fields",
        "Introduction to tools like ChatGPT, Copilot, Claude, Gemini",
        "Prompting as a communication and thinking skill",
        "Clear vs. unclear instructions (real-world examples)",
        "📝 Reflection Assignment"
    ]
)

# =======================================================
# 1. LECTURE VIDEO + PDF + TRANSCRIPT + QUIZ + DOWNLOAD
# =======================================================
if page == "🎧 Lecture Video / Voice Recording":
    st.subheader("🎧 Lecture for Module 1 — Foundations of Generative AI")

    # -------- PDF Notes --------
    st.markdown("### 📄 Downloadable PDF Notes")
    try:
        with open("notes/Intelligent_Prompting.pdf", "rb") as pdf_file:
            st.download_button(
                label="Download Module 1 Notes",
                data=pdf_file,
                file_name="Intelligent_Prompting.pdf",
                mime="application/pdf"
            )
    except Exception:
        st.warning("PDF notes not found. Add your file to `notes/module1_notes.pdf`.")

    # -------- Video (YouTube or YuJa via iframe) --------
    st.markdown("### 📺 Video Lecture")
    # For YuJa, replace with your iframe embed URL:
    # st.components.v1.iframe("https://siue.yuja.com/Dashboard/Permalink?authCode=167158588&b=14078175&linkType=video", width=800, height=450)
    st.video("https://siue.yuja.com/Dashboard/Permalink?authCode=167158588&b=14078175&linkType=video")  # Replace with your URL, or switch to iframe above


    # -------- Transcript --------
    st.markdown("---")
    st.markdown("### 📝 Lecture Transcript")
    st.markdown("""
*Replace this placeholder with your real transcript after recording the lecture.*
""")

    # -------- Interactive Quiz (Your two questions) --------
    st.markdown("---")
    st.markdown("## 🧠 Interactive Video Quiz")

    st.markdown("### **1. Please briefly introduce yourself — your major, hometown, interests, etc.**")
    st.text_area("Your response:", key="q1_intro", height=120)
    if st.button("Submit Answer 1"):
        if st.session_state["q1_intro"].strip():
            st.success("Thank you for sharing your introduction! This helps the instructor get to know you.")
        else:
            st.warning("Please enter your introduction before submitting.")

    st.markdown("---")

    st.markdown("### **2. What did you notice in this slide?**")
    st.text_area("Your response:", key="q2_slide", height=120)
    if st.button("Submit Answer 2"):
        if st.session_state["q2_slide"].strip():
            st.success("Thank you! Your observation has been recorded.")
        else:
            st.warning("Please describe what you noticed before submitting.")

    # -------- Download all answers so far (Name + Q1 + Q2 + Reflection if present) --------
    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses")
    section_download_block()

    # -------- Navigation to Module 2 --------
    goto_module_2_button()

# =======================================================
# 2. SUBJECT: What Generative AI Is and How It Works
# =======================================================
elif page == "What generative AI is and how it works":
    st.subheader("📌 What generative AI is and how it works")

    st.markdown("""
### **Lecture Reading**
Generative AI refers to a type of artificial intelligence that *creates new content*
based on patterns learned from huge datasets.

It works through:
1. **Training on large datasets** – learning language patterns, structures, styles.
2. **Predicting the next word** – it does not think; it predicts likely continuations.
3. **Generating responses** – probability-based generation creates natural-sounding text.

Generative AI does **not** understand meaning. It imitates patterns extremely well.
""")

    st.markdown("### 🧪 Interactive Exercise")
    prompt = st.text_area("Write a simple question you'd ask an AI:")
    if st.button("Simulate AI Response"):
        if prompt.strip():
            st.success(
                f"Here is an example of how an AI *might* respond to:\n\n**{prompt}**\n\n"
                "AI Response: This response reflects patterns learned during training and not human understanding."
            )
        else:
            st.warning("Please enter a prompt.")

# =======================================================
# 3. SUBJECT: What LLMs Can and Cannot Do
# =======================================================
elif page == "What LLMs can and cannot do":
    st.subheader("📌 What large language models (LLMs) can and cannot do")

    st.markdown("""
### **Lecture Reading**
LLMs **can**: summarize, rewrite, explain, brainstorm ideas, and organize information.  
LLMs **cannot**: guarantee factual accuracy, access private databases, truly understand like a human, or make ethical decisions.
""")

    st.markdown("### 🧪 Interactive Exercise")
    choose = st.radio(
        "Which of the following is something an LLM **cannot** do?",
        [
            "Rewrite a paragraph",
            "Guarantee factual accuracy",
            "Summarize a long article"
        ],
        index=None
    )
    if st.button("Check Answer"):
        if choose is None:
            st.warning("Please choose an option.")
        elif choose == "Guarantee factual accuracy":
            st.success("Correct!")
        else:
            st.error("Incorrect. Try again.")

# =======================================================
# 4. SUBJECT: Everyday Uses of AI
# =======================================================
elif page == "Everyday uses of AI across different fields":
    st.subheader("📌 Everyday uses of AI across different fields")

    st.markdown("""
### **Lecture Reading**
AI is used widely:

**Business** – reports, emails, marketing copy  
**Nursing & Health** – simplified explanations, patient education  
**Engineering** – concept breakdowns, documentation clarity  
**Social Sciences** – theme extraction, analysis  
**Arts** – story ideas, style descriptions  
**Education** – lesson planning, adapting materials
""")

    st.markdown("### 🧪 Interactive Exercise")
    field = st.text_input("Enter your major/field:")
    if st.button("Show an AI Use Case"):
        if field.strip():
            st.success(
                f"In **{field}**, AI could help by generating summaries, reorganizing information, "
                "and offering creative alternatives."
            )
        else:
            st.warning("Please enter your major.")

# =======================================================
# 5. SUBJECT: Introduction to Tools
# =======================================================
elif page == "Introduction to tools like ChatGPT, Copilot, Claude, Gemini":
    st.subheader("📌 Introduction to ChatGPT, Copilot, Claude, Gemini")

    st.markdown("""
### **Lecture Reading**
- **ChatGPT**: great explanations, creativity  
- **Claude**: long documents, safety  
- **Gemini**: multimodal, strong integrations  
- **Copilot**: Microsoft 365 workflow support  

Prompting skills transfer across ALL models.
""")

    st.markdown("### 🧪 Interactive Exercise")
    tool = st.selectbox("Choose a tool to learn about:", ["ChatGPT", "Claude", "Gemini", "Copilot"])
    st.info(f"You selected **{tool}**. This tool can help you generate text, answer questions, and assist with tasks.")

# =======================================================
# 6. SUBJECT: Prompting as Communication
# =======================================================
elif page == "Prompting as a communication and thinking skill":
    st.subheader("📌 Prompting as a communication and thinking skill")

    st.markdown("""
### **Lecture Reading**
Prompting is about clarity, structure, context, and constraints.
Designing a good prompt improves your own thinking and communication.
""")

    st.markdown("### 🧪 Interactive Exercise")
    unclear = st.text_input("Enter an unclear prompt:")
    if st.button("Rewrite Prompt Clearly"):
        if unclear.strip():
            st.success(
                "Clearer Version:\n"
                f"'Rewrite the following text at a 10th-grade reading level and summarize the key ideas: {unclear}'"
            )
        else:
            st.warning("Enter an unclear prompt first.")

# =======================================================
# 7. SUBJECT: Clear vs Unclear Instructions
# =======================================================
elif page == "Clear vs. unclear instructions (real-world examples)":
    st.subheader("📌 Clear vs unclear instructions")

    st.markdown("""
### **Lecture Reading**
**Unclear:** "Explain stress."  
**Clear:** "Explain mechanical stress with one everyday analogy, under 120 words."
""")

    st.markdown("### 🧪 Interactive Exercise")
    raw = st.text_input("Enter a vague/unclear instruction:")
    if st.button("Improve Instruction"):
        if raw.strip():
            st.success(
                "Improved Instruction:\n"
                f"'Explain {raw} in simple language, using 3 bullet points and an example.'"
            )
        else:
            st.warning("Enter a vague instruction first.")

# =======================================================
# 8. REFLECTION ASSIGNMENT (feeds into CSV download)
# =======================================================
elif page == "📝 Reflection Assignment":
    st.subheader("📝 Module 1 Reflection")

    st.markdown("""
Submit a 150–250 word reflection:
- What did you learn?
- How could generative AI help in your major?
- What questions do you still have?
""")

    # Keep the last typed reflection in session for CSV
    reflection = st.text_area("Write your reflection here:", height=200, key="reflection_m1")

    if st.button("Preview Reflection"):
        if st.session_state["reflection_m1"].strip():
            st.success("### Reflection Preview:")
            st.write(st.session_state["reflection_m1"])
        else:
            st.warning("Write a reflection to preview.")

    # Download responses from here too (so students don’t have to go back to the lecture page)
    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses")
    section_download_block()

    # Add the Module 2 button here as well
    goto_module_2_button()
