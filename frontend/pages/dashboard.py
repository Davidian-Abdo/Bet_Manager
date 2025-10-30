import streamlit as st
from utils.api_client import fetch_projects, fetch_team_performance, fetch_project_kpis
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show():
    st.title("🏠 Tableau de Bord BET Manager")
    
    # Welcome message
    if st.session_state.get('user'):
        user_name = st.session_state.user.get('name', 'Utilisateur')
        user_role = st.session_state.user.get('role', 'Utilisateur')
        st.success(f"👋 Bienvenue, **{user_name}**! (*{user_role}*)")
    
    # Refresh section
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("📊 Aperçu des Performances")
    with col2:
        if st.button("🔄 Actualiser les Données", use_container_width=True):
            st.rerun()
    
    try:
        # Fetch data from backend
        projects = fetch_projects() or []
        team_performance = fetch_team_performance() or []
        
        # Display key metrics
        st.subheader("🎯 Indicateurs Clés")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_projects = len(projects)
            st.metric("Projets Totaux", total_projects)
        
        with col2:
            completed = len([p for p in projects if p.get('status') in ['completed', 'terminé']])
            st.metric("Projets Terminés", completed)
        
        with col3:
            active = len([p for p in projects if p.get('status') in ['active', 'actif', 'en_cours']])
            st.metric("En Cours", active)
        
        with col4:
            delayed = len([p for p in projects if p.get('status') in ['delayed', 'en_retard']])
            st.metric("En Retard", delayed, delta=f"-{delayed}" if delayed > 0 else None)
        
        # Budget and progress overview
        if projects:
            total_budget = sum(p.get('budget', 0) for p in projects)
            avg_progress = sum(p.get('progress', 0) for p in projects) / len(projects)
            total_team = len(set([p.get('manager_id') for p in projects if p.get('manager_id')]))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Budget Total", f"${total_budget:,}")
            with col2:
                st.metric("Progression Moyenne", f"{avg_progress:.1f}%")
            with col3:
                st.metric("Membres d'Équipe", total_team)
        
        # Recent projects section
        st.subheader("📋 Projets Récents")
        if projects:
            # Display last 5 projects in a nice format
            for i, project in enumerate(projects[:5]):
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.write(f"### 🏗️ {project.get('name', 'Projet sans nom')}")
                        st.write(f"**Client:** {project.get('client', 'Non spécifié')}")
                        if project.get('description'):
                            st.write(f"*{project.get('description')}*")
                    
                    with col2:
                        progress = project.get('progress', 0)
                        st.write(f"**Progression:** {progress}%")
                        st.progress(progress / 100)
                        
                        status = project.get('status', 'inconnu')
                        status_emoji = {
                            'completed': '✅', 
                            'active': '🟡', 
                            'delayed': '🔴',
                            'planning': '📅'
                        }.get(status, '❓')
                        st.write(f"**Statut:** {status_emoji} {status}")
                    
                    with col3:
                        st.write(f"**Budget:** ${project.get('budget', 0):,}")
                        if st.button("Voir Détails", key=f"view_{i}", use_container_width=True):
                            st.session_state.selected_project = project.get('id')
                            st.switch_page("pages/projects.py")
                    
                    st.divider()
        else:
            st.info("🎉 Aucun projet trouvé. Créez votre premier projet pour commencer!")
        
        # Charts and analytics
        st.subheader("📈 Analytics")
        
        if projects:
            # Project status chart
            col1, col2 = st.columns(2)
            
            with col1:
                status_data = {}
                for project in projects:
                    status = project.get('status', 'unknown')
                    status_data[status] = status_data.get(status, 0) + 1
                
                if status_data:
                    fig = px.pie(
                        values=list(status_data.values()),
                        names=list(status_data.keys()),
                        title="Répartition des Statuts de Projet",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Budget distribution
                budget_data = []
                for project in projects[:10]:  # Limit to top 10 for readability
                    budget_data.append({
                        'Projet': project.get('name', 'Sans nom')[:20],
                        'Budget': project.get('budget', 0)
                    })
                
                if budget_data:
                    df = pd.DataFrame(budget_data)
                    fig = px.bar(
                        df, 
                        x='Projet', 
                        y='Budget',
                        title="Budget par Projet (Top 10)",
                        color='Budget'
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
        
        # Team performance
        st.subheader("👥 Performance de l'Équipe")
        if team_performance:
            team_df = pd.DataFrame(team_performance)
            fig = px.bar(
                team_df, 
                x='user_name', 
                y='completed_tasks',
                title="Tâches Complétées par Membre",
                color='completed_tasks',
                labels={'user_name': 'Membre', 'completed_tasks': 'Tâches Complétées'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Aucune donnée de performance d'équipe disponible pour le moment.")
        
        # Quick actions
        st.subheader("🚀 Actions Rapides")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📋 Créer Projet", use_container_width=True, help="Créer un nouveau projet"):
                st.switch_page("pages/projects.py")
        
        with col2:
            if st.button("📤 Upload Fichier", use_container_width=True, help="Uploader un document"):
                st.switch_page("pages/documents.py")
        
        with col3:
            if st.button("🖊️ Collaboration", use_container_width=True, help="Ouvrir la collaboration CAD"):
                st.switch_page("pages/cad_collaboration.py")
        
        with col4:
            if st.button("📊 Rapports", use_container_width=True, help="Voir les analytics détaillés"):
                st.switch_page("pages/analytics.py")
                
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {str(e)}")
        show_sample_dashboard()

def show_sample_dashboard():
    """Show sample dashboard when API is not available"""
    st.warning("🔧 Mode démo activé - Données d'exemple")
    
    # Sample metrics
    st.subheader("🎯 Indicateurs Clés (Exemple)")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Projets Totaux", "12", "2")
    with col2: st.metric("Projets Terminés", "8", "1")
    with col3: st.metric("En Cours", "3", "0")
    with col4: st.metric("En Retard", "1", "-1")
    
    # Sample projects
    st.subheader("📋 Projets Récents (Exemple)")
    sample_projects = [
        {"name": "Pont Hassan II", "client": "Ministère TP", "progress": 85, "status": "active", "budget": 500000},
        {"name": "Route Nationale 1", "client": "Département Routes", "progress": 100, "status": "completed", "budget": 300000},
        {"name": "Bâtiment Administratif", "client": "Ville de Casablanca", "progress": 45, "status": "active", "budget": 200000},
    ]
    
    for project in sample_projects:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{project['name']}**")
                st.write(f"Client: {project['client']}")
            with col2:
                st.progress(project['progress'] / 100)
                st.write(f"Progression: {project['progress']}%")
            with col3:
                st.write(f"Budget: ${project['budget']:,}")
            st.divider()
    
    # Quick actions
    st.subheader("🚀 Actions Rapides")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Nouveau Projet (Demo)", use_container_width=True):
            st.info("Fonctionnalité de création de projet")
    with col2:
        if st.button("📤 Upload Document (Demo)", use_container_width=True):
            st.info("Fonctionnalité d'upload de document")
    with col3:
        if st.button("🖊️ CAD (Demo)", use_container_width=True):
            st.switch_page("pages/cad_collaboration.py")

if __name__ == "__main__":
    show()