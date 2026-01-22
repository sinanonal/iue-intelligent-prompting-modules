import streamlit as st
import auth

st.set_page_config(page_title="Submit Assignments", layout="wide")
auth.require_identity(require_email=False)

st.title("Submit Assignments — Module 1")

st.markdown("### Module 1 Reflection (text submission)")
reflection = st.text_area(
    "Write your reflection (150–250 words)",
    height=200,
    placeholder="What did you learn from the readings? What surprised you? What will you try next?"
)

if st.button("Submit reflection", type="primary"):
    if not reflection.strip():
        st.error("Please write something before submitting.")
    else:
        auth.save_text_submission(reflection, assignment_key="module1_reflection", filename="reflection.txt")
        st.success("Reflection submitted.")

st.divider()

st.markdown("### Optional file upload")
f = st.file_uploader("Upload a file (optional)", type=["pdf", "docx", "txt", "png", "jpg", "csv"])

if st.button("Submit uploaded file"):
    if not f:
        st.error("Please choose a file first.")
    else:
        auth.save_uploaded_file(f, assignment_key="module1_upload")
        st.success("File submitted.")
