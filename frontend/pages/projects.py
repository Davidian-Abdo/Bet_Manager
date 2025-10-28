# frontend/pages/projects.py
import streamlit as st
import streamlit.components.v1 as components
from frontend.utils.api_client import APIClient

api = APIClient(base_url="http://localhost:8000/api")

def show():
    st.title("🏗️ Projets")
    st.markdown("Liste des projets et détails de phasage.")

    project_id = st.number_input("Sélectionnez le projet ID", min_value=1, value=1)
    user_id = st.session_state["user"].get("id")

    # Fetch projects list (optional, could be used for dropdown instead of numeric input)
    projects = api.get_projects()
    if projects:
        project_names = {p["id"]: p["name"] for p in projects}
        selected_name = project_names.get(project_id, "N/A")
        st.write(f"Projet sélectionné: {selected_name}")

    # Embed DWGViewer TS component
    dwg_viewer = components.declare_component(
        "dwg_viewer",
        path="frontend/components/DWGViewer/build"
    )
    dwg_viewer(projectId=project_id, userId=user_id)