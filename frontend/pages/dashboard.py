# frontend/pages/dashboard.py
import streamlit as st
import streamlit.components.v1 as components

def show():
    st.title("📊 Tableau de bord")
    st.markdown("Vue générale des projets et performances de l'équipe.")

    # Project selection (optional, you can later replace with dropdown)
    project_id = st.number_input("Sélectionnez le projet ID", min_value=1, value=1)

    # Get token from session state
    token = st.session_state.get("access_token", "")

    # Get backend URL from Streamlit secrets
    backend_url = st.secrets.get("BACKEND_URL", "http://127.0.0.1:8000")

    # Embed ProjectDashboard TS component
    project_dashboard = components.declare_component(
        "project_dashboard",
        path="frontend/components/ProjectDashboard/build"
    )

    # Pass all required props to the TS component
    project_dashboard(
        projectId=project_id,
        token=token,
        backendUrl=backend_url
    )
