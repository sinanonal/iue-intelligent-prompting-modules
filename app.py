
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

# ---- Sidebar navigation ----
st.sidebar.title("Module 1 Subjects")
page = st.sidebar.radio(
    "Choose a subject:",
    [
        "What generative AI is and how it works",
        "What LLMs can and cannot do",
        "Everyday uses of AI across different fields",
        "Introduction to tools like ChatGPT, Copilot, Claude, Gemini",
        "Prompting as a communication and thinking skill",
        "Clear vs. unclear instructions (real-world examples)"
    ]
)

# ---- Subject Pages ----

# 1 — What generative AI is and how it works
if page == "What generative AI is and how it works":
    st.subheader("📌 What generative AI is and how it works")

    st.markdown("""
### **Lecture Reading**
Generative AI refers to a type of artificial intelligence that *creates new content* based on patterns it has learned from large amounts of data.  
This content can include text, images, summaries, explanations, stories, analyses, or even code.

Large models like ChatGPT do not “think” or “understand.”  
Instead, they predict the next most likely word, sentence, or structure based on their training data.

Generative AI works through:
1. **Training on massive datasets**  
   The AI learns patterns from textbooks, articles, public websites, conversations, and more.
2. **Pattern prediction**  
   When you type a prompt, the model predicts the most likely response.
3. **Continuous refinement**  
   Models improve over time based on updates and new training methods.

Although generative AI appears intelligent, its behavior is pattern-based—not conscious or self-aware.
""")

# 2 — What LLMs can and cannot do
elif page == "What LLMs can and cannot do":
    st.subheader("📌 What large language models (LLMs) can and cannot do")

    st.markdown("""
### **Lecture Reading**
LLMs excel at:
- Producing clear explanations  
- Summarizing long text  
- Brainstorming ideas  
- Rewriting or editing text  
- Generating creative content  
- Breaking down complex concepts  
- Assisting with analysis and planning  

However, LLMs **cannot**:
- Guarantee factual accuracy  
- Understand information the way humans do  
- Access real-time private databases  
- Verify the truth of every statement  
- Replace expert judgment  
- Make moral or ethical decisions  

A key skill in this course is learning how to **work with these strengths and limitations**.
""")

# 3 — Everyday uses across fields
elif page == "Everyday uses of AI across different fields":
    st.subheader("📌 Everyday uses of AI across different fields")

    st.markdown("""
### **Lecture Reading**
Generative AI is used across nearly every discipline:

#### **Business**
- Writing emails or reports  
- Market analysis summaries  
- Customer message drafting  

#### **Engineering**
- High-level explanations of concepts  
- Brainstorming design alternatives  
- Document summarization  

#### **Healthcare & Nursing**
- Simplifying medical explanations  
- Patient education materials  
- Research article summaries  

#### **Psychology & Social Sciences**
- Theme extraction from interviews  
- Scenario generation  
- Survey response analysis  

#### **Arts and Media**
- Creative brainstorming  
- Story generation  
- Style descriptions  

#### **Education**
- Lesson planning  
- Creating examples at different levels  
- Adapting material for diverse learners  

LLMs can support—but not replace—expert knowledge in every field.
""")

# 4 — Introduction to tools
elif page == "Introduction to tools like ChatGPT, Copilot, Claude, Gemini":
    st.subheader("📌 Introduction to tools like ChatGPT, Copilot, Claude, Gemini")

    st.markdown("""
### **Lecture Reading**
There are many types of generative AI tools. The most common include:

#### **ChatGPT (OpenAI)**
Known for:
- Conversational ability  
- Explanation clarity  
- Creativity  
- Writing assistance  

#### **Claude (Anthropic)**
Known for:
- Long document handling  
- Safety considerations  
- Clear reasoning  

#### **Gemini (Google)**
Known for:
- Web-connected responses  
- Multimodal capabilities  
- Integration with Google workspace tools  

#### **Microsoft Copilot**
Known for:
- Integration with Microsoft 365  
- Practical productivity support  
- Document, email, and presentation generation  

Each tool is slightly different, but the prompting principles in this course work across all of them.
""")

# 5 — Prompting as communication
elif page == "Prompting as a communication and thinking skill":
    st.subheader("📌 Prompting as a communication and thinking skill")

    st.markdown("""
### **Lecture Reading**
Prompting is not just typing something into a box.  
It is a form of **communication** and **structured thinking**.

Good prompting requires:
- Clear instructions  
- Defined goals  
- Context  
- Constraints  
- Desired format  

In many ways, prompting helps you:
- Think more clearly  
- Break down complex problems  
- Organize your own ideas  
- Practice concise communication  

You will learn prompting patterns that allow you to give AI more precise and useful instructions.
""")

# 6 — Clear vs unclear instructions
elif page == "Clear vs. unclear instructions (real-world examples)":
    st.subheader("📌 Clear vs. unclear instructions")

    st.markdown("""
### **Lecture Reading**
LLMs respond differently depending on how clearly you communicate.

#### **Unclear prompt example:**  
“Explain this better.”

#### **Clear prompt example:**  
“Rewrite the following paragraph at a 10th-grade reading level and highlight the three main ideas.”

#### **Unclear:**  
“Tell me about photosynthesis.”

#### **Clear:**  
“Explain photosynthesis in 4 steps, using plain language, and give one example relevant to agriculture.”

#### **Examples Across Majors**

- **Nursing:**  
  *Unclear:* “Explain diabetes.”  
  *Clear:* “Explain Type 2 diabetes to a patient with no medical background using friendly, simple language.”

- **Business:**  
  *Unclear:* “Help with marketing.”  
  *Clear:* “Generate three marketing messages targeting 25–40-year-old customers interested in fitness technology.”

- **Engineering:**  
  *Unclear:* “Explain stress.”  
  *Clear:* “Explain mechanical stress with one everyday analogy and keep the explanation under 120 words.”

The clearer your instructions, the better the output.
""")
