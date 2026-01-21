import streamlit as st

# ------------------------------
#   WEEK 1 – STREAMLIT APP
# ------------------------------

st.set_page_config(page_title="Week 1 – Intelligent Prompting", layout="wide")

# ---- HEADER ----
st.title("📘 Week 1: Introduction to Generative AI")
st.markdown("""
Welcome to **Intelligent Prompting: Using AI for Creative and Analytical Thinking**.  
This Week 1 module helps you understand what generative AI is and how we will use it throughout this course.

Use the left sidebar to navigate the Week 1 sections.
""")

# ---- SIDEBAR NAV ----
st.sidebar.title("Week 1 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["📖 Overview", "🤖 What Is Generative AI?", "🧪 Interactive Activity", "📝 Reflection Assignment"]
)

# ---- OVERVIEW PAGE ----
if page == "📖 Overview":
    st.header("📖 Week 1 Overview")
    st.markdown("""
### What You Will Learn This Week
- What generative AI and large language models (LLMs) are  
- How AI interprets text inputs  
- Why prompting is a communication skill  
- Examples of AI use across different majors  
- How this course works (structure, assignments, expectations)

---

### Why This Course Is Interdisciplinary
Students from **all majors** are welcome — no programming or AI experience needed.
Examples across:
- Business  
- Engineering  
- Nursing & Health  
- Psychology & Social Sciences  
- Art, Music, Design  
- Education & Humanities  

Everyone will design prompts relevant to *their own discipline*.

---

### This Week's Deliverables
- Complete the **Interactive AI Activity**  
- Write the **Week 1 Reflection** (150–250 words)
""")

# ---- GENERATIVE AI PAGE ----
elif page == "🤖 What Is Generative AI?":
    st.header("🤖 What Is Generative AI?")
    st.markdown("""
Generative AI models—such as ChatGPT, Claude, Gemini, and Copilot—are systems that produce text, images, summaries, analyses, creative ideas, and more based on your instructions.

### 🧠 Key Ideas for Week 1
- LLMs generate the *next most probable word* based on patterns learned from large datasets.
- They do **not** think, understand, or verify facts.
- Clear instructions = better output.
- Prompting is more like giving instructions to a collaborator, not a search engine.

### 💡 Examples Across Majors
- **Nursing:** Simplify a medical explanation for a patient.  
- **Engineering:** Get a high-level comparison of two design approaches.  
- **Psychology:** Identify themes in a mock interview.  
- **Business:** Generate different audience‑specific marketing messages.  
- **Art:** Brainstorm new project ideas or aesthetics.  
- **Education:** Adapt content for different grade levels.

This week focuses on basics, not technical depth.
""")

# ---- INTERACTIVE ACTIVITY ----
elif page == "🧪 Interactive Activity":
    st.header("🧪 Week 1 Interactive AI Activity")
    st.markdown("""
### Try Your First Prompt
Type a simple prompt below to see how an LLM *might* respond.

*(Note: This is a simulated response environment — no API keys needed.)*
""")

    user_prompt = st.text_area("✏️ Enter a simple prompt:", height=100)

    if st.button("Generate Simulated Response"):
        if user_prompt.strip() == "":
            st.warning("Please enter a prompt first.")
        else:
            # Simple simulation of an AI-style response
            simulated_response = f"""
**Simulated AI Response:**

You asked:  
*{user_prompt}*

Here is an example of how an AI might respond:

- It analyzes your instruction.
- It identifies the key task.
- It produces a structured, clear answer.
- It uses patterns learned during training but does not verify facts.

This is only a demonstration.  
In later weeks, you’ll learn how to make responses more accurate, structured, and useful.
"""
            st.success(simulated_response)

# ---- REFLECTION PAGE ----
elif page == "📝 Reflection Assignment":
    st.header("📝 Week 1 Reflection Assignment")
    st.markdown("""
### Submit Your Week 1 Reflection (150–250 words)

**Reflection Prompt:**  
Describe your current understanding of generative AI and how you think it may be useful in *your major* or future career.  
What questions or concerns do you still have?

Paste your reflection below to preview it (you will paste it into Canvas/Blackboard for submission).
""")

    reflection_text = st.text_area("✏️ Your Reflection:", height=200)

    if st.button("Preview My Reflection"):
        if reflection_text.strip() == "":
            st.warning("Please write your reflection first.")
        else:
            st.success("Here is your reflection preview:")
            st.write(reflection_text)
