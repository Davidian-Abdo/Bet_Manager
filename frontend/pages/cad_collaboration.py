import streamlit as st
import streamlit.components.v1 as components
import os
import json

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
        
        **Pour construire les composants React:**
        ```bash
        cd frontend\\react-components
        npm install
        npm run build
        ```
        """)
        return
    
    # Check if build was successful
    index_path = os.path.join(react_build_path, "index.html")
    static_path = os.path.join(react_build_path, "static")
    
    if not os.path.exists(index_path) or not os.path.exists(static_path):
        st.error("""
        ❌ Build React incomplet.
        
        Le dossier build existe mais les fichiers nécessaires sont manquants.
        Essayez de reconstruire:
        ```bash
        cd frontend\\react-components
        npm run build
        ```
        """)
        return
    
    # Read the built React app
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier React: {e}")
        return
    
    # Prepare configuration
    backend_url = st.secrets.get("BACKEND_URL", "http://localhost:8000")
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
    
    # Display current configuration
    with st.expander("🔧 Configuration Actuelle"):
        st.json(config)
    
    # Embed React app
    components.html(html_content, height=700, scrolling=False)

if __name__ == "__main__":
    show()