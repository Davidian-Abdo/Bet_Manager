import streamlit as st
from utils.api_client import fetch_projects, fetch_project, create_project, update_project, delete_project

def show():
    st.title("📋 Gestion des Projets")
    
    if "token" not in st.session_state:
        st.error("Veuillez vous connecter pour accéder aux projets")
        return
    
    # Tab interface for different views
    tab1, tab2, tab3 = st.tabs(["📊 Liste des Projets", "➕ Nouveau Projet", "🔍 Détails du Projet"])
    
    with tab1:
        show_projects_list()
    
    with tab2:
        show_new_project_form()
    
    with tab3:
        show_project_details()

def show_projects_list():
    st.subheader("Liste des Projets")
    
    projects = fetch_projects()
    
    if not projects:
        st.info("Aucun projet trouvé. Créez votre premier projet!")
        return
    
    # Projects table
    for project in projects:
        with st.expander(f"🏗️ {project.get('name', 'Sans nom')} - {project.get('status', 'N/A')}"):
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.write(f"**Client:** {project.get('client', 'N/A')}")
                st.write(f"**Description:** {project.get('description', 'Aucune description')}")
            
            with col2:
                st.write(f"**Budget:** ${project.get('budget', 0):,}")
                st.write(f"**Progression:** {project.get('progress', 0)}%")
                st.progress(project.get('progress', 0) / 100)
            
            with col3:
                if st.button("📝 Éditer", key=f"edit_{project['id']}"):
                    st.session_state.editing_project = project['id']
                    st.rerun()
                
                if st.button("🗑️ Supprimer", key=f"delete_{project['id']}"):
                    if delete_project(project['id']):
                        st.success("Projet supprimé!")
                        st.rerun()

def show_new_project_form():
    st.subheader("Créer un Nouveau Projet")
    
    with st.form("new_project_form"):
        name = st.text_input("Nom du Projet*", placeholder="Pont Hassan II")
        client = st.text_input("Client*", placeholder="Ministère des Travaux Publics")
        description = st.text_area("Description", placeholder="Description du projet...")
        
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("Budget ($)*", min_value=0, value=100000)
            start_date = st.date_input("Date de Début")
        with col2:
            deadline = st.date_input("Échéance")
            status = st.selectbox("Statut", ["planning", "active", "on_hold", "completed"])
        
        if st.form_submit_button("🚀 Créer le Projet"):
            if name and client:
                project_data = {
                    "name": name,
                    "client": client,
                    "description": description,
                    "budget": budget,
                    "start_date": start_date.isoformat() if start_date else None,
                    "deadline": deadline.isoformat() if deadline else None,
                    "status": status
                }
                
                result = create_project(project_data)
                if result:
                    st.success("Projet créé avec succès!")
                    st.rerun()
            else:
                st.error("Veuillez remplir les champs obligatoires (*)")

def show_project_details():
    st.subheader("Détails du Projet")
    
    project_id = st.number_input("ID du Projet", min_value=1, value=1, key="project_details_id")
    
    if st.button("Charger les Détails", key="load_project_details"):
        project = fetch_project(project_id)
        
        if project:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Nom:** {project.get('name')}")
                st.write(f"**Client:** {project.get('client')}")
                st.write(f"**Statut:** {project.get('status')}")
                st.write(f"**Progression:** {project.get('progress', 0)}%")
                st.progress(project.get('progress', 0) / 100)
            
            with col2:
                st.write(f"**Budget:** ${project.get('budget', 0):,}")
                st.write(f"**Date de Début:** {project.get('start_date', 'N/A')}")
                st.write(f"**Échéance:** {project.get('deadline', 'N/A')}")
                st.write(f"**Créé le:** {project.get('created_at', 'N/A')}")
            
            st.write(f"**Description:** {project.get('description', 'Aucune description')}")
        else:
            st.error("Projet non trouvé")