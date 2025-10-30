import streamlit as st
from utils.api_client import fetch_projects, fetch_team_performance  # Use your api_client

def show():
    st.title("🏠 Tableau de Bord")
    
    # Welcome message
    if st.session_state.get('user'):
        user_name = st.session_state.user.get('name', 'Utilisateur')
        st.success(f"Bienvenue, **{user_name}**!")
    
    # Refresh button
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.subheader("Aperçu des Performances")
    
    with col4:
        if st.button("🔄 Actualiser"):
            st.rerun()
    
    # Fetch data using your api_client
    try:
        projects = fetch_projects() or []
        team_performance = fetch_team_performance() or []
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Projets Actifs", len(projects))
        
        with col2:
            completed = len([p for p in projects if p.get('status') == 'completed'])
            st.metric("Projets Terminés", completed)
        
        with col3:
            active = len([p for p in projects if p.get('status') == 'active'])
            st.metric("En Cours", active)
        
        with col4:
            delayed = len([p for p in projects if p.get('status') == 'delayed'])
            st.metric("En Retard", delayed, delta=-delayed)
        
        # Recent projects
        st.subheader("Projets Récents")
        if projects:
            for project in projects[:5]:  # Show last 5 projects
                with st.expander(f"📋 {project.get('name', 'Unnamed Project')}"):
                    st.write(f"**Statut:** {project.get('status', 'N/A')}")
                    st.write(f"**Progression:** {project.get('progress', 0)}%")
                    st.write(f"**Budget:** ${project.get('budget', 0):,}")
        
        # Quick actions
        st.subheader("Actions Rapides")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Nouveau Projet", use_container_width=True):
                st.switch_page("pages/projects.py")
        
        with col2:
            if st.button("📤 Upload Document", use_container_width=True):
                st.switch_page("pages/documents.py")
        
        with col3:
            if st.button("📊 Analytics", use_container_width=True):
                st.switch_page("pages/analytics.py")
                
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        st.info("Mode démo activé - données d'exemple")
        
        # Demo data
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Projets Actifs", "8")
        with col2: st.metric("Projets Terminés", "12")
        with col3: st.metric("En Cours", "5")
        with col4: st.metric("En Retard", "2")