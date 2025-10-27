# frontend/pages/dashboard.py
import streamlit as st
import streamlit.components.v1 as components

def show():
    st.title("📊 Tableau de bord")
    st.markdown("Vue générale des projets et performances de l'équipe.")

    # Embed ProjectDashboard TS component
    project_dashboard = components.declare_component(
        "project_dashboard",
        path="frontend/components/ProjectDashboard/build"
    )
    project_dashboard()