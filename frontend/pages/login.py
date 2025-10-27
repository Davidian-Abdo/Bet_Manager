import streamlit as st
import requests
from frontend.utils.config import API_BASE_URL

def show_login():
    st.title("BET Manager Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        payload = {"username": username, "password": password}
        # Use OAuth2PasswordRequestForm format
        data = {"username": username, "password": password}
        response = requests.post(f"{API_BASE_URL}/auth/login", data=data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            st.session_state["token"] = token
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")