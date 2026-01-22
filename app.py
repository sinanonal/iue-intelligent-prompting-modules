import streamlit as st
import io
import csv
from datetime import datetime

# -----------------------------------------
#   TIER 1 — Foundations of Generative AI
#   MODULE 1 — Foundations of Generative AI
# -----------------------------------------

st.set_page_config(page_title="Module 1 — Foundations of Generative AI", layout="wide")

# ------------------ UTILITIES ------------------
def safe_strip(key: str) -> str:
    return str(st.session_state.get(key, "")).strip()

def word_count(text: str) -> int:
    return len([w for w in text.split() if w.strip()])

def build_csv_bytes():
    """Create a CSV of the student's Module 1 responses and return as bytes (Excel-friendly)."""
    name = safe_strip("student_name")
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
    name = safe_strip("student_name")
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
            help="Downloads your name and answers as a CSV file you can submit or keep."
        )
    else:
        st.info("Fill in your name and at least one answer to enable the download button.")

def goto_module_2_button():
    st.markdown("---")
    if st.button("➡️ Go to Module 2"):
        try:
            st.switch_page("pages/Module 2.py")  # if you later convert to multipage app
        except Exception:
            st.info("Module 2 will be available soon. (To enable navigation, create `pages/Module 2.py`.)")

# ------------------ HEADER ------------------
st.title("📘 Tier 1 — Foundations of Generative AI")
st.header("Module 1 — Foundations of Generative AI")
st.markdown("""
This module introduces the core ideas behind generative AI and large language models (LLMs).
Use the menu on the left to explore each subject in this module.
""")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Module 1 Subjects")

st.sidebar.markdown("**Student Info**")
st.sidebar.text_input("Your full name (for downloads):", key="student_name")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose a subject:",
    [
        "✅ Start Here (Checklist)",
        "🎧 Lecture Video / Voice Recording",
        "What generative AI is and how it works",
        "What LLMs can and cannot do",
        "Everyday uses of AI across different fields",
        "Introduction to tools like ChatGPT, Copilot, Claude, Gemini",
        "Prompting as a communication and thinking skill",
        "Clear vs. unclear instructions (real-world examples)",
        "🧪 Prompt Lab (ChatGPT Practice)",
        "📝 Reflection Assignment",
    ]
)

# =======================================================
# START PAGE: CHECKLIST (reduces “click-around and miss”)
# =======================================================
if page == "✅ Start Here (Checklist)":
    st.subheader("✅ Module 1 Checklist")

    st.markdown("""
Use this checklist to complete Module 1 in order.  
You can return here anytime to see what is still missing.
""")

    name = safe_strip("student_name")
    q1 = safe_strip("q1_intro")
    q2 = safe_strip("q2_slide")

    prompt_used = safe_strip("m1_prompt_used")
    ai_resp = safe_strip("m1_ai_response")
    prompt_ref = safe_strip("m1_prompt_reflection")

    refl = safe_strip("reflection_m1")
    refl_wc = word_count(refl)

    def status_line(done: bool, text: str):
        st.write(("✅ " if done else "⬜ ") + text)

    status_line(bool(name), "Enter your full name (left sidebar)")
    status_line(bool(q1 and q2), "Watch the video + answer Q1 and Q2")
    status_line(bool(prompt_used and ai_resp and prompt_ref), "Complete Prompt Lab (prompt + AI response + reflection)")
    status_line(150 <= refl_wc <= 250, "Write the 150–250 word Module Reflection")

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses")
    section_download_block()
    goto_module_2_button()

# =======================================================
# 1. LECTURE VIDEO + PDF + TRANSCRIPT + QUIZ + DOWNLOAD
# =======================================================
elif page == "🎧 Lecture Video / Voice Recording":
    st.subheader("🎧 Lecture for Module 1 — Foundations of Generative AI")

    # -------- PDF Notes --------
    st.markdown("### 📄 Downloadable PDF Notes")
    pdf_path = "notes/Intelligent_Prompting.pdf"  # adjust if your actual filename differs
    try:
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download Module 1 Notes (PDF)",
                data=pdf_file,
                file_name="Intelligent_Prompting.pdf",
                mime="application/pdf"
            )
    except Exception:
        st.warning(f"PDF notes not found. Add your file to `{pdf_path}` (or update the path in the code).")

    # -------- Video (YouTube or YuJa) --------
    st.markdown("### 📺 Video Lecture")
    st.video("https://siue.yuja.com/Dashboard/Permalink?authCode=167158588&b=14078175&linkType=video")

    # -------- Transcript --------
    st.markdown("---")
    with st.expander("📝 Lecture Transcript (click to open)", expanded=False):
        st.markdown("""
*Replace this placeholder with your real transcript after recording the lecture.*
""")

    # -------- Interactive Quiz (Form is smoother than multiple buttons) --------
    st.markdown("---")
    st.markdown("## 🧠 Interactive Video Questions")

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

    # -------- Download all answers so far --------
    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses")
    section_download_block()

    goto_module_2_button()

# =======================================================
# 2. SUBJECT: What Generative AI Is and How It Works
# =======================================================
elif page == "What generative AI is and how it works":
    st.subheader("📌 What generative AI is and how it works")

    st.markdown("""
### Lecture Reading
Generative AI refers to a type of artificial intelligence that **creates new content**
based on patterns learned from large datasets.

It typically works through:
1. **Training on large datasets** – learning language patterns, structures, styles  
2. **Predicting the next token/word** – it does not “think”; it predicts likely continuations  
3. **Generating responses** – probability-based generation produces natural-sounding text

Generative AI can be very useful, but it can also produce convincing errors.
""")

    st.markdown("### 🧪 Quick Activity: Turn a vague idea into a clear prompt")
    vague = st.text_input("Write a vague prompt idea (example: 'Explain AI'):")
    if st.button("Make it clearer"):
        if vague.strip():
            st.success(
                "Clearer version example:\n\n"
                f"“Explain **{vague.strip()}** to a first-year college student using 3 bullet points and one example. "
                "Keep it under 120 words.”"
            )
        else:
            st.warning("Please enter a vague prompt first.")

# =======================================================
# 3. SUBJECT: What LLMs Can and Cannot Do
# =======================================================
elif page == "What LLMs can and cannot do":
    st.subheader("📌 What large language models (LLMs) can and cannot do")

    st.markdown("""
### Lecture Reading
LLMs **can**: summarize, rewrite, explain, brainstorm ideas, and organize information.  
LLMs **cannot**: guarantee factual accuracy, access private databases, truly understand like a human, or make ethical decisions.
""")

    st.markdown("### 🧪 Interactive Check")
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
### Lecture Reading
AI is used widely:

- **Business** – reports, emails, marketing copy  
- **Nursing & Health** – simplified explanations, patient education  
- **Engineering** – concept breakdowns, documentation clarity  
- **Social Sciences** – theme extraction, analysis support  
- **Arts** – story ideas, style descriptions  
- **Education** – lesson planning, adapting materials
""")

    st.markdown("### 🧪 Quick Activity")
    field = st.text_input("Enter your major/field:")
    if st.button("Show an AI Use Case"):
        if field.strip():
            st.success(
                f"In **{field}**, AI could help by summarizing information, reorganizing content, "
                "generating alternatives, and improving clarity."
            )
        else:
            st.warning("Please enter your major.")

# =======================================================
# 5. SUBJECT: Introduction to Tools
# =======================================================
elif page == "Introduction to tools like ChatGPT, Copilot, Claude, Gemini":
    st.subheader("📌 Introduction to ChatGPT, Copilot, Claude, Gemini")

    st.markdown("""
### Lecture Reading
- **ChatGPT**: strong explanations, brainstorming, and writing support  
- **Claude**: often strong with long documents  
- **Gemini**: multimodal features and integrations  
- **Copilot**: Microsoft 365 workflow support  

Prompting skills transfer across tools.
""")

    st.markdown("### 🧪 Interactive Exercise")
    tool = st.selectbox("Choose a tool:", ["ChatGPT", "Claude", "Gemini", "Copilot"])
    st.info(f"You selected **{tool}**. Prompting principles are similar across tools.")

# =======================================================
# 6. SUBJECT: Prompting as Communication
# =======================================================
elif page == "Prompting as a communication and thinking skill":
    st.subheader("📌 Prompting as a communication and thinking skill")

    st.markdown("""
### Lecture Reading
Prompting is about clarity, structure, context, and constraints.
A good prompt often includes:
- what you want (task)
- who it’s for (audience)
- how to format it (output format)
- limits (length, tone, sources, etc.)
""")

    st.markdown("### 🧪 Interactive Exercise")
    unclear = st.text_input("Enter an unclear prompt:")
    if st.button("Rewrite Prompt Clearly"):
        if unclear.strip():
            st.success(
                "Clearer Version example:\n\n"
                f"“Rewrite the following at a 10th-grade reading level and summarize the key ideas in 4 bullets: {unclear}”"
            )
        else:
            st.warning("Enter an unclear prompt first.")

# =======================================================
# 7. SUBJECT: Clear vs Unclear Instructions
# =======================================================
elif page == "Clear vs. unclear instructions (real-world examples)":
    st.subheader("📌 Clear vs unclear instructions")

    st.markdown("""
### Lecture Reading
**Unclear:** “Explain stress.”  
**Clear:** “Explain **mechanical stress** with one everyday analogy, under 120 words.”
""")

    st.markdown("### 🧪 Interactive Exercise")
    raw = st.text_input("Enter a vague/unclear instruction:")
    if st.button("Improve Instruction"):
        if raw.strip():
            st.success(
                "Improved Instruction example:\n\n"
                f"“Explain **{raw}** in simple language using 3 bullet points and one example.”"
            )
        else:
            st.warning("Enter a vague instruction first.")

# =======================================================
# 8. PROMPT LAB (Option A — practice in ChatGPT, paste back)
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
    pr_text = safe_strip("m1_prompt_reflection")
    pr_wc = word_count(pr_text)
    st.caption(f"Prompt Lab reflection word count: {pr_wc} (aim ~50–120 words)")
    st.text_area(
        "What worked well? What would you change to make your prompt clearer or more specific?",
        key="m1_prompt_reflection",
        height=160,
        placeholder="Write 3–5 sentences..."
    )

    st.markdown("---")
    if st.button("Check Prompt Lab Completeness"):
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
    st.markdown("### ⬇️ Download Your Responses")
    section_download_block()

    goto_module_2_button()

# =======================================================
# 9. REFLECTION ASSIGNMENT
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
    if wc == 0:
        st.caption("Word count: 0 (target 150–250)")
    else:
        st.caption(f"Word count: {wc} (target 150–250)")

    if wc > 0 and (wc < 150 or wc > 250):
        st.warning("Your reflection is outside the 150–250 word range. Please revise.")

    if st.button("Preview Reflection"):
        if safe_strip("reflection_m1"):
            st.success("### Reflection Preview:")
            st.write(safe_strip("reflection_m1"))
        else:
            st.warning("Write a reflection to preview.")

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses")
    section_download_block()

    goto_module_2_button()
