# frontend/pages/settings.py
import streamlit as st

def show():
    st.title("⚙️ Settings")

    st.header("User Preferences")
    theme = st.selectbox("Theme", ["Light", "Dark"])
    notifications = st.checkbox("Enable notifications", value=True)
    language = st.selectbox("Language", ["English", "Français", "العربية"])

    st.header("API Configuration")
    api_url = st.text_input("API Base URL", value="http://localhost:8000/api")

    st.header("Account")
    st.text_input("Username", value="user@example.com")
    st.text_input("Password", type="password")

    if st.button("Save Settings"):
        # You can store settings in st.session_state or a local JSON/config file
        st.success("Settings saved successfully!")