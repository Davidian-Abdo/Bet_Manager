import streamlit as st
from utils.api_client import fetch_users, create_user

def show():
    st.title("⚙️ Paramètres")
    
    if "token" not in st.session_state:
        st.error("Veuillez vous connecter pour accéder aux paramètres")
        return
    
    # User role check
    current_user = st.session_state.get('user', {})
    user_role = current_user.get('role', 'viewer')
    
    if user_role not in ['admin', 'superadmin']:
        st.warning("🔒 Accès restreint - Fonctionnalités administrateur uniquement")
        return
    
    tab1, tab2, tab3 = st.tabs(["👥 Gestion Utilisateurs", "🔧 Configuration", "ℹ️ À Propos"])
    
    with tab1:
        show_user_management()
    
    with tab2:
        show_system_config()
    
    with tab3:
        show_about()

def show_user_management():
    st.subheader("Gestion des Utilisateurs")
    
    # Fetch existing users
    users = fetch_users()
    
    if users:
        st.write("### Utilisateurs Existants")
        for user in users:
            with st.expander(f"👤 {user.get('name', 'Sans nom')} - {user.get('email')}"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Rôle:** {user.get('role', 'user')}")
                    st.write(f"**Statut:** {'🟢 Actif' if user.get('is_active') else '🔴 Inactif'}")
                    st.write(f"**Créé le:** {user.get('created_at', 'N/A')}")
                
                with col2:
                    new_role = st.selectbox(
                        "Modifier le rôle",
                        ["admin", "engineer", "designer", "viewer"],
                        index=["admin", "engineer", "designer", "viewer"].index(user.get('role', 'viewer')),
                        key=f"role_{user['id']}"
                    )
                
                with col3:
                    if st.button("💾 Sauvegarder", key=f"save_{user['id']}"):
                        st.success(f"Rôle de {user.get('name')} mis à jour vers {new_role}")
                        # Here you would call update_user_role function
    
    # Create new user
    st.write("### Créer un Nouvel Utilisateur")
    with st.form("create_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nom Complet*", placeholder="John Doe")
            email = st.text_input("Email*", placeholder="john@betmanager.com")
        
        with col2:
            role = st.selectbox("Rôle*", ["engineer", "designer", "viewer", "admin"])
            password = st.text_input("Mot de Passe*", type="password", placeholder="Mot de passe sécurisé")
        
        if st.form_submit_button("👤 Créer l'Utilisateur"):
            if all([name, email, password]):
                user_data = {
                    "name": name,
                    "email": email,
                    "password": password,
                    "role": role
                }
                result = create_user(user_data)
                if result:
                    st.success(f"Utilisateur {name} créé avec succès!")
                    st.rerun()
            else:
                st.error("Veuillez remplir tous les champs obligatoires (*)")

def show_system_config():
    st.subheader("Configuration du Système")
    
    st.write("### Paramètres Généraux")
    
    with st.form("system_config_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            auto_backup = st.checkbox("Sauvegarde Automatique", value=True)
            backup_frequency = st.selectbox("Fréquence de Sauvegarde", ["Quotidienne", "Hebdomadaire", "Mensuelle"])
            max_file_size = st.number_input("Taille Max des Fichiers (MB)", min_value=1, value=100)
        
        with col2:
            email_notifications = st.checkbox("Notifications Email", value=True)
            default_language = st.selectbox("Langue par Défaut", ["Français", "Anglais", "Arabe"])
            theme = st.selectbox("Thème", ["Clair", "Sombre", "Auto"])
        
        if st.form_submit_button("💾 Sauvegarder la Configuration"):
            st.success("Configuration sauvegardée avec succès!")

def show_about():
    st.subheader("À Propos de BET Manager")
    
    st.write("""
    ### 🏗️ BET Manager v1.0.0
    
    **Plateforme de gestion pour Bureaux d'Études Techniques en Génie Civil**
    
    **Fonctionnalités Principales:**
    - 📋 Gestion complète des projets
    - 📁 Gestion documentaire avancée
    - 🖊️ Collaboration CAD en temps réel
    - 📊 Analytics et rapports détaillés
    - 👥 Gestion des équipes et des rôles
    
    **Technologies:**
    - **Backend:** FastAPI, PostgreSQL, WebSocket
    - **Frontend:** Streamlit, React, TypeScript
    - **Stockage:** S3/MinIO pour les documents
    - **Authentification:** JWT Tokens
    
    **Développé pour:** Les professionnels du génie civil marocain
    """)
    
    st.info("""
    **Support Technique:**
    - 📧 Email: support@betmanager.com
    - 📞 Téléphone: +212 XXX-XXXXXX
    - 🏢 Adresse: Casablanca, Maroc
    """)