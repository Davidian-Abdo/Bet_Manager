import streamlit as st
from frontend.utils.api_client import APIClient

api = APIClient(base_url="http://localhost:8000/api")

def show():
    st.title("BET Manager Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        data = {"username": username, "password": password}
        response = api._post("auth/login", data)  # Use centralized API client
        if response:
            token = response.get("access_token")
            st.session_state["token"] = token
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")
