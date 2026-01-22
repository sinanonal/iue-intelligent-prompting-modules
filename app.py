import streamlit as st
import auth
from content import COURSE_TITLE, WELCOME_MESSAGE

st.set_page_config(page_title=COURSE_TITLE, layout="wide")

# Show identity panel on the home page too (doesn't block home)
auth.render_identity_sidebar(require_email=False)

st.title(COURSE_TITLE)
st.markdown(WELCOME_MESSAGE)

st.markdown("### Navigation")
st.write("Use the left menu to open Course Overview and the modules.")
