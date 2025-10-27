# frontend/pages/documents.py
import streamlit as st
import requests

API_BASE = "http://localhost:8000/api"

def show():
    st.title("📄 Documents")
    project_id = st.number_input("Sélectionnez le projet ID", min_value=1, value=1)
    
    # Fetch documents from API
    res = requests.get(f"{API_BASE}/documents/{project_id}")
    if res.status_code == 200:
        docs = res.json()
        for d in docs:
            st.write(f"- {d['name']} (Type: {d['doc_type']})")
    else:
        st.warning("Aucun document trouvé pour ce projet.")