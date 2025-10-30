import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.api_client import fetch_project_kpis, fetch_team_performance, fetch_projects

def show():
    st.title("📊 Analytics & Rapports")
    
    if "token" not in st.session_state:
        st.error("Veuillez vous connecter pour accéder aux analytics")
        return
    
    # Fetch data
    projects = fetch_projects() or []
    team_performance = fetch_team_performance() or []
    
    # Display KPIs
    st.header("📈 Indicateurs Clés de Performance")
    
    if projects:
        total_budget = sum(p.get('budget', 0) for p in projects)
        avg_progress = sum(p.get('progress', 0) for p in projects) / len(projects)
        completed_projects = len([p for p in projects if p.get('status') == 'completed'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Budget Total", f"${total_budget:,}")
        with col2: st.metric("Progression Moyenne", f"{avg_progress:.1f}%")
        with col3: st.metric("Projets Terminés", completed_projects)
        with col4: st.metric("Taux de Réussite", f"{(completed_projects/len(projects)*100):.1f}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Répartition des Projets par Statut")
        if projects:
            status_counts = pd.DataFrame([
                {"Statut": p.get('status', 'unknown'), "Count": 1} 
                for p in projects
            ]).groupby('Statut').count().reset_index()
            
            fig = px.pie(status_counts, values='Count', names='Statut', 
                         title="Distribution des Statuts de Projet")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée de projet disponible")
    
    with col2:
        st.subheader("💰 Budget par Projet")
        if projects:
            budget_data = pd.DataFrame([
                {"Projet": p.get('name', 'Unknown'), "Budget": p.get('budget', 0)}
                for p in projects
            ])
            fig = px.bar(budget_data, x='Projet', y='Budget', 
                        title="Budget par Projet", color='Budget')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée de budget disponible")
    
    # Team Performance
    st.subheader("👥 Performance de l'Équipe")
    if team_performance:
        team_df = pd.DataFrame(team_performance)
        fig = px.bar(team_df, x='user_name', y='completed_tasks', 
                    title="Tâches Complétées par Membre", color='completed_tasks')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée de performance d'équipe disponible")
    
    # Project-specific analytics
    st.subheader("🔍 Analytics par Projet")
    if projects:
        project_options = {p['id']: p['name'] for p in projects}
        selected_project = st.selectbox(
            "Sélectionner un Projet",
            options=list(project_options.keys()),
            format_func=lambda x: project_options[x]
        )
        
        if selected_project:
            kpis = fetch_project_kpis(selected_project)
            if kpis:
                col1, col2, col3 = st.columns(3)
                with col1: st.metric("Progression", f"{kpis.get('progress', 0)}%")
                with col2: st.metric("Budget Utilisé", f"${kpis.get('budget_used', 0):,}")
                with col3: st.metric("Tâches Complétées", kpis.get('completed_tasks', 0))
            else:
                st.warning("Aucune donnée KPI disponible pour ce projet")

def create_sample_chart():
    """Create sample chart when no data is available"""
    st.info("Affichage des données d'exemple (mode démo)")
    
    # Sample data
    sample_data = pd.DataFrame({
        'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai'],
        'Progression': [25, 45, 60, 75, 90],
        'Budget': [100000, 250000, 450000, 600000, 750000]
    })
    
    fig = px.line(sample_data, x='Mois', y='Progression', 
                  title="Progression Mensuelle (Exemple)")
    st.plotly_chart(fig, use_container_width=True)