import streamlit as st
from utils.api_client import login  # Use your existing api_client

def show():
    st.title("🔐 Login to BET Manager")
    
    # If already logged in, redirect to main app
    if "token" in st.session_state and st.session_state.token:
        st.success("Already logged in! Redirecting...")
        st.rerun()
        return
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="admin@betmanager.com")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Login")
                
                if submitted:
                    if not email or not password:
                        st.error("Please enter both email and password")
                        return
                    
                    # Use your existing login function
                    if login(email, password):
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Login failed. Check your credentials.")
        
        with col2:
            st.info("**Demo Credentials**")
            st.code("Email: admin@betmanager.com\nPassword: admin123")
            
            # Test connection button
            from utils.api_client import BACKEND_URL
            import requests
            
            if st.button("Test Backend Connection"):
                try:
                    response = requests.get(f"{BACKEND_URL}/docs", timeout=5)
                    if response.status_code == 200:
                        st.success("✅ Backend is reachable!")
                    else:
                        st.error(f"Backend returned status: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Connection failed: {e}")