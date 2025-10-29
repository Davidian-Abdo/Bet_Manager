import streamlit as st
from pages import dashboard, projects, documents, analytics, settings, login

# Configure page
st.set_page_config(page_title="BET Manager", layout="wide")

# Check authentication
if "token" not in st.session_state:
    login.show()
else:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ("Dashboard", "Projects", "Documents", "Analytics", "Settings")
    )

    if page == "Dashboard":
        dashboard.show()
    elif page == "Projects":
        projects.show()
    elif page == "Documents":
        documents.show()
    elif page == "Analytics":
        analytics.show()
    elif page == "Settings":
        settings.show()
