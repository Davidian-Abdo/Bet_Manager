# frontend/pages/documents.py
import streamlit as st
from frontend.utils.api_client import APIClient

api = APIClient(base_url="http://localhost:8000/api")

def show():
    st.title("📄 Documents")
    project_id = st.number_input("Sélectionnez le projet ID", min_value=1, value=1)

    docs = api._get(f"documents/{project_id}")
    if docs:
        for d in docs:
            st.write(f"- {d['name']} (Type: {d['doc_type']})")
    else:
        st.warning("Aucun document trouvé pour ce projet.")