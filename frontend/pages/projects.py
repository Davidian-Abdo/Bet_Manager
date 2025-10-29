# frontend/pages/projects.py
import streamlit as st
import streamlit.components.v1 as components
from utils import api_client  # ✅ use your shared API client (not a separate class instance)

def show():
    st.title("🏗️ Projets")
    st.markdown("Liste des projets et détails de phasage.")

    # Ensure user is logged in
    if "user" not in st.session_state:
        st.warning("Veuillez d'abord vous connecter.")
        st.stop()

    project_id = st.number_input("Sélectionnez le projet ID", min_value=1, value=1)
    user_id = st.session_state["user"].get("id")

    # ✅ Use the shared api_client functions
    projects = api_client.fetch_projects()

    if projects:
        project_names = {p["id"]: p["name"] for p in projects}
        selected_name = project_names.get(project_id, "N/A")
        st.write(f"Projet sélectionné : **{selected_name}**")
    else:
        st.info("Aucun projet disponible ou erreur de chargement.")

    # ✅ Safely embed your DWGViewer Streamlit component
    try:
        dwg_viewer = components.declare_component(
            "dwg_viewer",
            path="frontend/components/DWGViewer/build"
        )
        dwg_viewer(projectId=project_id, userId=user_id)
    except Exception as e:
        st.error(f"Erreur lors du chargement du visualiseur DWG : {e}")
