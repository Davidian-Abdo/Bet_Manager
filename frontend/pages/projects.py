# frontend/pages/projects.py
import streamlit as st
import streamlit.components.v1 as components

def show():
    st.title("🏗️ Projets")
    st.markdown("Liste des projets et détails de phasage.")

    # Embed DWGViewer component for selected project
    project_id = st.number_input("Sélectionnez le projet ID", min_value=1, value=1)
    user_id = st.session_state["user"].get("id")

    dwg_viewer = components.declare_component(
        "dwg_viewer",
        path="frontend/components/DWGViewer/build"
    )
    dwg_viewer(projectId=project_id, userId=user_id)