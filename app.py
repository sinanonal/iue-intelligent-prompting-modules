import streamlit as st
from auth import require_access, render_top_bar

require_access()
render_top_bar("Home Page")



import streamlit as st

st.set_page_config(
    page_title="Home — Intelligent Prompting",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📘 Intelligent Prompting: Using AI for Creative and Analytical Thinking")
st.header("Welcome")

st.markdown("""
Welcome to the course! This class is designed to help you learn how to communicate effectively with AI tools such as **ChatGPT, Claude, Gemini, and Copilot**—a skill that is becoming essential across many fields.

You may already be using AI for writing, studying, brainstorming, or problem-solving. In this course, you will move beyond casual use and learn **how to guide these tools intentionally**. We focus on **intelligent prompting**: writing clear, structured instructions that help AI produce useful, accurate, and appropriate responses.

This is an **interdisciplinary course**, which means students from **all majors** are welcome. Whether you are studying engineering, business, health sciences, social sciences, arts, or another field, you will learn how AI can support your academic and professional work. You will practice prompting through hands-on activities, real-world examples, and interactive modules inside this app.

Throughout the course, we emphasize **critical thinking and responsible AI use**. AI can be a powerful assistant, but it also has limitations. You will learn how to evaluate AI responses, recognize potential errors or bias, and use these tools ethically and transparently.

By the end of the course, you will develop your own **personal prompting practice**—one that helps you think more clearly, communicate more effectively, and collaborate responsibly with AI systems.

""")

st.markdown("---")

st.subheader("📬 Questions, Feedback, and Communication")

st.markdown("""
If you have **any questions**, need clarification at any point, or would like to share **feedback on how to make this course better**, please do not hesitate to reach out.

Your questions and suggestions are always welcome, and they help improve the course for everyone.
""")

st.markdown(
    "📧 **Email:** "
    "[sonal@siue.edu](mailto:sonal@siue.edu)"
)

st.markdown("---")

st.subheader("🚀 Getting Started")

st.markdown("""
To begin, review the **Course Overview and Introduction** to understand how the course is organized.  
When you are ready, continue to **Module 1** to start learning about generative AI and prompting.
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("📘 Go to Course Overview"):
        st.switch_page("pages/00_Course Overview.py")

with col2:
    if st.button("➡️ Go to Module 1"):
        st.switch_page("pages/01_Module 1.py")
