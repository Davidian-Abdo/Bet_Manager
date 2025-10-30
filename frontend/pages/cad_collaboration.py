import streamlit as st
import streamlit.components.v1 as components
import os
import json
from utils.api_client import get_backend_url

def show():
    st.title("🖊️ Collaboration CAD en Temps Réel")
    
    if "token" not in st.session_state:
        st.error("Veuillez vous connecter pour accéder à la collaboration CAD")
        return
    
    # User info
    user_info = st.session_state.get('user', {})
    user_name = user_info.get('name', 'Utilisateur')
    user_role = user_info.get('role', 'viewer')
    
    st.sidebar.subheader("Paramètres CAD")
    project_id = st.sidebar.number_input("ID du Projet", min_value=1, value=1)
    
    # Build path to React components
    current_dir = os.path.dirname(os.path.abspath(__file__))
    react_build_path = os.path.join(current_dir, "..", "react-components", "build")
    
    if not os.path.exists(react_build_path):
        st.error("""
        ❌ Composants React non trouvés. 
        
        **Solution:** Les composants React doivent être construits avant le déploiement.
        Contactez l'administrateur pour régler ce problème.
        """)
        
        # Fallback: Show a simplified CAD interface
        show_fallback_cad_interface(project_id, user_name, user_role)
        return
    
    # Check if build was successful
    index_path = os.path.join(react_build_path, "index.html")
    static_path = os.path.join(react_build_path, "static")
    
    if not os.path.exists(index_path) or not os.path.exists(static_path):
        st.warning("Build React incomplet. Affichage de l'interface de secours...")
        show_fallback_cad_interface(project_id, user_name, user_role)
        return
    
    # Load and embed React app
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Prepare configuration
        backend_url = get_backend_url()
        config = {
            "projectId": project_id,
            "token": st.session_state.token,
            "backendUrl": backend_url,
            "userRole": user_role,
            "userName": user_name
        }
        
        # Fix asset paths for Streamlit embedding
        html_content = html_content.replace('href="/static/', 'href="./static/')
        html_content = html_content.replace('src="/static/', 'src="./static/')
        
        # Inject configuration
        script_tag = f"""
        <script>
            window.STREAMLIT_CONFIG = {json.dumps(config)};
        </script>
        """
        html_content = html_content.replace("</head>", f"{script_tag}</head>")
        
        # Success message
        st.success("✅ Composants React chargés avec succès!")
        
        # Embed React app
        components.html(html_content, height=700, scrolling=False)
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des composants React: {e}")
        show_fallback_cad_interface(project_id, user_name, user_role)

def show_fallback_cad_interface(project_id: int, user_name: str, user_role: str):
    """Fallback CAD interface when React components aren't available"""
    st.warning("🔧 Interface CAD de secours activée")
    
    st.subheader("Contrôle d'Accès")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**👤 Utilisateur:** {user_name}")
        st.info(f"**🎯 Rôle:** {user_role}")
    
    with col2:
        has_access = st.checkbox("Accès Édition", value=user_role in ['admin', 'engineer'])
        if has_access:
            st.success("🟢 Mode Édition Activé")
        else:
            st.info("🔴 Mode Observation")
    
    st.subheader("Outils de Dessin")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✏️ Ligne", disabled=not has_access):
            st.session_state.last_action = "Ligne ajoutée"
    
    with col2:
        if st.button("⭕ Cercle", disabled=not has_access):
            st.session_state.last_action = "Cercle ajouté"
    
    with col3:
        if st.button("⬛ Rectangle", disabled=not has_access):
            st.session_state.last_action = "Rectangle ajouté"
    
    # Drawing area simulation
    st.subheader("Zone de Dessin")
    st.markdown("""
    <div style='border: 2px solid #ccc; height: 400px; background: #f8f9fa; 
                display: flex; align-items: center; justify-content: center; 
                border-radius: 8px; margin: 10px 0;'>
        <div style='text-align: center; color: #666;'>
            <h3>🖊️ Zone de Dessin CAD</h3>
            <p>Interface de dessin interactive</p>
            <p><em>Composants React requis pour les fonctionnalités avancées</em></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Last action
    if 'last_action' in st.session_state:
        st.info(f"**Dernière action:** {st.session_state.last_action}")

if __name__ == "__main__":
    show()