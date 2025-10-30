# frontend/pages/login.py
import streamlit as st
import requests

def show():
    st.title("🔐 Login to BET Manager")
    
    # Check backend connection first
    backend_url = st.secrets.get("BACKEND_URL", "http://localhost:8000")
    
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
                    
                    # Attempt login
                    try:
                        response = requests.post(
                            f"{backend_url}/api/auth/login",
                            json={"email": email, "password": password},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            token_data = response.json()
                            st.session_state.token = token_data["access_token"]
                            st.success("Login successful! Redirecting...")
                            st.rerun()
                        else:
                            st.error(f"Login failed: Invalid credentials or server error")
                            
                    except requests.exceptions.RequestException:
                        st.error("❌ Cannot connect to backend service. Please check:")
                        st.write(f"- Backend URL: `{backend_url}`")
                        st.write("- Is the backend server running?")
                        st.write("- Is ngrok tunnel active (if using ngrok)?")
                    except Exception as e:
                        st.error(f"Unexpected error: {e}")
        
        with col2:
            st.info("**Demo Credentials**")
            st.code("Email: admin@betmanager.com\nPassword: admin123")
            
            # Test connection button
            if st.button("Test Backend Connection"):
                try:
                    response = requests.get(f"{backend_url}/docs", timeout=5)
                    if response.status_code == 200:
                        st.success("✅ Backend is reachable!")
                    else:
                        st.error(f"Backend returned status: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Connection failed: {e}")