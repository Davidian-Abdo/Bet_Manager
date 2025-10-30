import streamlit as st
import pandas as pd
from utils.api_client import fetch_documents, upload_document
from datetime import datetime

def show():
    st.title("📁 Gestion des Documents")
    
    if "token" not in st.session_state:
        st.error("Veuillez vous connecter pour accéder aux documents")
        return
    
    tab1, tab2 = st.tabs(["📋 Documents Existants", "📤 Uploader Document"])
    
    with tab1:
        show_existing_documents()
    
    with tab2:
        show_upload_form()

def show_existing_documents():
    st.subheader("Documents du Projet")
    
    documents = fetch_documents()
    
    if not documents:
        st.info("Aucun document trouvé. Uploader votre premier document!")
        return
    
    # Display documents in a nice format
    for doc in documents:
        with st.expander(f"📄 {doc.get('name', 'Document sans nom')}"):
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.write(f"**Type:** {doc.get('file_type', 'N/A')}")
                st.write(f"**Taille:** {doc.get('file_size', 0)} bytes")
                st.write(f"**Description:** {doc.get('description', 'Aucune description')}")
            
            with col2:
                st.write(f"**Projet:** {doc.get('project_name', 'N/A')}")
                st.write(f"**Uploadé le:** {doc.get('uploaded_at', 'N/A')}")
                st.write(f"**Par:** {doc.get('uploaded_by', 'Utilisateur inconnu')}")
            
            with col3:
                if st.button("📥 Télécharger", key=f"download_{doc['id']}"):
                    st.info("Fonctionnalité de téléchargement à implémenter")
                
                if st.button("👁️ Voir", key=f"view_{doc['id']}"):
                    st.info("Visionneuse de document à implémenter")

def show_upload_form():
    st.subheader("Uploader un Nouveau Document")
    
    with st.form("upload_document_form"):
        # Project selection
        from utils.api_client import fetch_projects
        projects = fetch_projects() or []
        project_options = {p['id']: p['name'] for p in projects}
        
        selected_project = st.selectbox(
            "Projet*",
            options=list(project_options.keys()),
            format_func=lambda x: project_options.get(x, "Sélectionner un projet")
        )
        
        # Document details
        doc_name = st.text_input("Nom du Document*", placeholder="Plan_architectural_v1.dwg")
        description = st.text_area("Description", placeholder="Description du document...")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choisir le fichier*",
            type=['dwg', 'pdf', 'doc', 'docx', 'xlsx', 'jpg', 'png'],
            help="Formats supportés: DWG, PDF, DOC, DOCX, XLSX, JPG, PNG"
        )
        
        if st.form_submit_button("📤 Uploader le Document"):
            if not all([selected_project, doc_name, uploaded_file]):
                st.error("Veuillez remplir tous les champs obligatoires (*)")
                return
            
            # Prepare document data
            document_data = {
                "name": doc_name,
                "description": description,
                "project_id": selected_project,
                "file_type": uploaded_file.type,
                "file_size": len(uploaded_file.getvalue())
            }
            
            # Here you would typically send the file to your backend
            # For now, we'll just show a success message
            st.success(f"Document '{doc_name}' prêt à être uploadé!")
            st.info("Intégration avec le stockage backend à compléter")
            
            # Reset form
            st.rerun()