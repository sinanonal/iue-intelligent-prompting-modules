
import streamlit as st

# -----------------------------------------
#   TIER 1 — Foundations of Generative AI
#   MODULE 1 — Foundations of Generative AI
# -----------------------------------------

st.set_page_config(page_title="Module 1 — Foundations of Generative AI",
                   layout="wide")

# ---- Header ----
st.title("📘 Tier 1 — Foundations of Generative AI")
st.header("Module 1 — Foundations of Generative AI")

st.markdown("""
This module introduces the core ideas behind generative AI and large language models (LLMs).
Use the menu on the left to explore each subject in this module.
""")

# ---- Sidebar Navigation ----
st.sidebar.title("Module 1 Subjects")
page = st.sidebar.radio(
    "Choose a subject:",
    [
        "🎧 Lecture Video / Voice Recording",
        "What generative AI is and how it works",
        "What LLMs can and cannot do",
        "Everyday uses of AI across different fields",
        "Introduction to tools like ChatGPT, Copilot, Claude, Gemini",
        "Prompting as a communication and thinking skill",
        "Clear vs. unclear instructions (real-world examples)"
    ]
)

# ---- LECTURE SECTION ----
if page == "🎧 Lecture Video / Voice Recording":
    st.subheader("🎧 Lecture for Module 1 — Foundations of Generative AI")

    # -------- PDF Notes --------
    try:
        with open("notes/module1_notes.pdf", "rb") as pdf_file:
            st.download_button(
                label="📄 Download Module 1 PDF Notes",
                data=pdf_file,
                file_name="Module1_Notes.pdf",
                mime="application/pdf"
            )
    except:
        st.warning("PDF notes not found. Upload `notes/module1_notes.pdf` to enable downloads.")

    st.markdown("### 📺 Video Lecture")
    st.video("https://www.youtube.com/watch?v=JTxsNm9IdYU&list=PLsprmdocuVe8Tn23MlNkMkoS-cZAJb6gC&index=2")  # Replace with your link

    
    # -------- Transcript --------
    st.markdown("---")
    st.markdown("### 📝 Lecture Transcript")
    st.markdown("""
**Module 1 — Foundations of Generative AI (Transcript Placeholder)**  
You can paste your transcript here or generate one automatically 
after recording your lecture.
""")

    # -------- Quiz Questions --------
    st.markdown("---")
    st.markdown("### 🧠 Quick Knowledge Check")

    q1 = st.radio(
        "1. What does a large language model primarily do?",
        [
            "Understands meaning like a human",
            "Predicts the next most likely word based on patterns",
            "Searches the internet in real time"
        ]
    )
    if q1:
        if q1 == "Predicts the next most likely word based on patterns":
            st.success("Correct!")
        else:
            st.error("Not quite. Try again.")

    # -------- Navigation Button --------
    st.markdown("---")
    if st.button("➡️ Go to Module 2"):
        st.info("Module 2 will be available soon.")

# ---- SUBJECT PAGES ----
elif page == "What generative AI is and how it works":
    st.subheader("📌 What generative AI is and how it works")
    st.markdown("""
### Lecture Reading
Generative AI refers to a type of artificial intelligence that creates new content
based on patterns learned from large datasets.
""")


elif page == "What LLMs can and cannot do":
    st.subheader("📌 What large language models (LLMs) can and cannot do")
    st.markdown("""
### Lecture Reading
LLMs can generate text, summarize information, provide explanations,
and assist with reasoning — but they cannot guarantee accuracy.
""")


elif page == "Everyday uses of AI across different fields":
    st.subheader("📌 Everyday uses of AI across different fields")
    st.markdown("""
### Lecture Reading
Generative AI is used in business, engineering, healthcare,
education, design, and social sciences.
""")


elif page == "Introduction to tools like ChatGPT, Copilot, Claude, Gemini":
    st.subheader("📌 Introduction to AI Tools")
    st.markdown("""
### Lecture Reading
These tools differ in strengths, but prompting skills apply to all of them.
""")


elif page == "Prompting as a communication and thinking skill":
    st.subheader("📌 Prompting as communication and thinking skill")
    st.markdown("""
### Lecture Reading
Prompting requires clarity, structure, and context.
""")


elif page == "Clear vs. unclear instructions (real-world examples)":
    st.subheader("📌 Clear vs unclear instructions")
    st.markdown("""
### Lecture Reading
Clear prompts produce clear outputs.  
Examples across disciplines.
""")
