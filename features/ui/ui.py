import streamlit as st
import os

def render_ui():
    st.set_page_config(
        page_title="Personal Health Record",
        page_icon="❤️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Display the logo
    logo_path = "assets/logo.svg"
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=100)

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Introduction", "Input Form", "Visualization", "Analytics", "Reports", "Recommendations"])

    return page
