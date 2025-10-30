import streamlit as st
from utils import api_client

def show():
    st.title("🔐 BET Manager Login")

    st.markdown("Connectez-vous à votre espace BET Manager.")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if not email or not password:
            st.warning("Veuillez remplir tous les champs.")
            return

        with st.spinner("Connexion en cours..."):
            success = api_client.login(email, password)

        if success:
            st.success("✅ Connexion réussie !")
            st.experimental_rerun()
        else:
            st.error("❌ Échec de la connexion. Vérifiez vos identifiants.")
