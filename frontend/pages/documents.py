# frontend/pages/documents.py
import streamlit as st
from utils.api_client import get, post, put, delete  # use centralized API client

def show():
    st.title("📄 Documents")

    # Get current user
    user = st.session_state.get("user", {})
    
    # Project selection
    project_id = st.number_input(
        "Sélectionnez le projet ID", 
        min_value=1, 
        value=1
    )

    # Fetch documents dynamically from backend
    docs = get(f"/documents/?project_id={project_id}")  # backend URL is handled inside api_client.py
    if docs:
        st.subheader("Documents disponibles")
        for d in docs:
            st.write(f"- {d['name']} (Type: {d['doc_type']})")
    else:
        st.warning("Aucun document trouvé pour ce projet.")

    # Optional: upload new document
    uploaded_file = st.file_uploader("Téléverser un document", type=["pdf", "dwg"])
    if uploaded_file:
        file_data = uploaded_file.read()
        payload = {
            "project_id": project_id,
            "name": uploaded_file.name,
            "doc_type": uploaded_file.type,
            "content": file_data.decode("latin1")  # store as string for simple test, adjust for backend
        }
        result = post("/documents/", payload)
        if result:
            st.success(f"{uploaded_file.name} téléversé avec succès !")
            st.experimental_rerun()
        else:
            st.error("Erreur lors du téléversement du document."
