
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
        "Clear vs. unclear instructions (real-world examples)",
        "📝 Reflection Assignment"
    ]
)

# =======================================================
# 1. LECTURE VIDEO + PDF + TRANSCRIPT
# =======================================================
if page == "🎧 Lecture Video / Voice Recording":
    st.subheader("🎧 Lecture for Module 1 — Foundations of Generative AI")

    # PDF NOTES
    st.markdown("### 📄 Downloadable PDF Notes")
    try:
        with open("notes/Intelligent_Prompting.pdf","rb") as pdf_file:
            st.download_button(
                label="Download Module 1 Notes",
                data=pdf_file,
                file_name="Intelligent_Prompting.pdf",
                mime="application/pdf"
            )
    except:
        st.warning("PDF notes not found. Add your file to `notes/Intelligent_Prompting.pdf`.")

    # VIDEO
    st.markdown("### 📺 Video Lecture")
    st.video("https://siue.yuja.com/Dashboard/Permalink?authCode=167158588&b=14078175&linkType=video")

    
    # TRANSCRIPT
    st.markdown("---")
    st.markdown("### 📝 Lecture Transcript")
    st.markdown("""
*Replace this placeholder with your real transcript after recording the lecture.*
""")

# ===== YuJa-style Interactive Quiz Questions =====
st.markdown("---")
st.markdown("## 🧠 Interactive Video Quiz")

# Question 1
st.markdown("### **1. Please briefly introduce yourself — your major, hometown, interests, etc.**")
intro_answer = st.text_area("Your response:", key="q1_intro", height=120)

if st.button("Submit Answer 1"):
    if intro_answer.strip():
        st.success("Thank you for sharing your introduction! This helps the instructor get to know you.")
    else:
        st.warning("Please enter your introduction before submitting.")

st.markdown("---")

# Question 2
st.markdown("### **2. What did you notice in this slide?**")
slide_answer = st.text_area("Your response:", key="q2_slide", height=120)

if st.button("Submit Answer 2"):
    if slide_answer.strip():
        st.success("Thank you! Your observation has been recorded.")
    else:
        st.warning("Please describe what you noticed before submitting.")

  
    # QUIZ
    st.markdown("---")
    st.markdown("### 🧠 Quick Knowledge Check")
    q1 = st.radio(
        "1. Generative AI produces content by…",
        [
            "Understanding meaning like a human",
            "Predicting the next likely word based on patterns",
            "Searching the internet live for information"
        ]
    )
    if q1:
        if q1 == "Predicting the next likely word based on patterns":
            st.success("Correct!")
        else:
            st.error("Not quite. Try again.")

    # NAVIGATION BUTTON
    st.markdown("---")
    if st.button("➡️ Go to Module 2"):
        st.info("Module 2 will be available soon.")


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
1. **Training on large datasets**  
   It learns language patterns, structures, writing styles, etc.
2. **Predicting the next word**  
   It does not think—it predicts.
3. **Generating responses based on probability**  
   This creates natural-sounding text.

Generative AI does **not** understand meaning.  
It imitates patterns extremely well.
""")

    # INTERACTIVE EXERCISE
    st.markdown("### 🧪 Interactive Exercise")
    prompt = st.text_area("Write a simple question you'd ask an AI:")

    if st.button("Simulate AI Response"):
        if prompt.strip():
            st.success(f"Here is an example of how an AI *might* respond to:\n\n**{prompt}**\n\nAI Response: This response reflects patterns learned during training and not human understanding.")
        else:
            st.warning("Please enter a prompt.")


# =======================================================
# 3. SUBJECT: What LLMs Can and Cannot Do
# =======================================================
elif page == "What LLMs can and cannot do":
    st.subheader("📌 What large language models (LLMs) can and cannot do")

    st.markdown("""
### **Lecture Reading**
LLMs **can**:
- Summarize  
- Rewrite  
- Explain  
- Generate ideas  
- Organize information  

LLMs **cannot**:
- Guarantee factual accuracy  
- Access private databases  
- Understand like a human  
- Make ethical decisions  
""")

    st.markdown("### 🧪 Interactive Exercise")
    choose = st.radio(
        "Which of the following is something an LLM **cannot** do?",
        [
            "Rewrite a paragraph",
            "Guarantee factual accuracy",
            "Summarize a long article"
        ]
    )
    if choose:
        if choose == "Guarantee factual accuracy":
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
AI is used everywhere:

#### Business
Reports, emails, marketing copy  
#### Nursing & Health
Simplified explanations, patient education  
#### Engineering
Concept breakdowns, documentation clarity  
#### Social Sciences
Theme extraction, analysis  
#### Arts
Story ideas, style descriptions  
""")

    st.markdown("### 🧪 Interactive Exercise")
    field = st.text_input("Enter your major/field:")
    if st.button("Show an AI Use Case"):
        if field.strip():
            st.success(f"In **{field}**, AI could help by generating summaries, reorganizing information, and offering creative alternatives.")
        else:
            st.warning("Please enter your major.")


# =======================================================
# 5. SUBJECT: Introduction to Tools
# =======================================================
elif page == "Introduction to tools like ChatGPT, Copilot, Claude, Gemini":
    st.subheader("📌 Introduction to ChatGPT, Copilot, Claude, Gemini")

    st.markdown("""
### **Lecture Reading**
Every tool has different strengths:

- **ChatGPT**: great explanations, creativity  
- **Claude**: long documents, safety  
- **Gemini**: multimodal, strong integrations  
- **Copilot**: excellent Microsoft 365 workflow support  

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
Prompting is about:

- Clarity  
- Structure  
- Context  
- Constraints  

When you design a good prompt, you're actually improving your own thinking.
""")

    st.markdown("### 🧪 Interactive Exercise")
    unclear = st.text_input("Enter an unclear prompt:")
    if st.button("Rewrite Prompt Clearly"):
        if unclear.strip():
            st.success(f"Clearer Version:\n'Rewrite the following text at a 10th-grade reading level and summarize the key ideas: {unclear}'")
        else:
            st.warning("Enter an unclear prompt first.")


# =======================================================
# 7. SUBJECT: Clear vs Unclear Instructions
# =======================================================
elif page == "Clear vs. unclear instructions (real-world examples)":
    st.subheader("📌 Clear vs unclear instructions")

    st.markdown("""
### **Lecture Reading**
**Unclear:**  
"Explain stress."

**Clear:**  
"Explain mechanical stress with one everyday analogy, under 120 words."
""")

    st.markdown("### 🧪 Interactive Exercise")
    raw = st.text_input("Enter a vague/unclear instruction:")
    if st.button("Improve Instruction"):
        if raw.strip():
            st.success(f"Improved Instruction:\n'Explain {raw} in simple language, using 3 bullet points and an example.'")
        else:
            st.warning("Enter a vague instruction first.")


# =======================================================
# 8. REFLECTION ASSIGNMENT
# =======================================================
elif page == "📝 Reflection Assignment":
    st.subheader("📝 Module 1 Reflection")

    st.markdown("""
Submit a 150–250 word reflection:
- What did you learn?
- How could generative AI help in your major?
- What questions do you still have?
""")

    reflection = st.text_area("Write your reflection here:", height=200)

    if st.button("Preview Reflection"):
        if reflection.strip():
            st.success("### Reflection Preview:")
            st.write(reflection)
        else:
            st.warning("Write a reflection to preview.")
