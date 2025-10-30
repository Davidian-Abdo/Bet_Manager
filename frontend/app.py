import streamlit as st
import requests
from pages import dashboard, projects, documents, analytics, settings, login

# Configure page
st.set_page_config(page_title="BET Manager", layout="wide")

def validate_token(token: str) -> bool:
    """Validate if the token is still valid with the backend"""
    try:
        backend_url = st.secrets.get("BACKEND_URL", "http://localhost:8000")
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{backend_url}/api/users/me",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            # Store user info in session state
            st.session_state.user = response.json()
            return True
        else:
            # Token is invalid
            st.session_state.token = None
            st.session_state.user = None
            return False
            
    except requests.exceptions.RequestException:
        # Backend connection failed
        st.error("⚠️ Cannot connect to backend service. Please check if the server is running.")
        return False
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return False

def check_backend_connection() -> bool:
    """Check if backend is reachable"""
    try:
        backend_url = st.secrets.get("BACKEND_URL", "http://localhost:8000")
        response = requests.get(f"{backend_url}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def show_connection_status():
    """Show backend connection status in sidebar"""
    if check_backend_connection():
        st.sidebar.success("✅ Backend connected")
    else:
        st.sidebar.error("❌ Backend disconnected")

# Main authentication logic
def main():
    # Initialize session state
    if "user" not in st.session_state:
        st.session_state.user = None
    
    # Show connection status
    show_connection_status()
    
    # Check if user is properly authenticated
    is_authenticated = False
    
    if "token" in st.session_state and st.session_state.token:
        # Validate the existing token
        is_authenticated = validate_token(st.session_state.token)
    else:
        # No token exists
        is_authenticated = False
    
    # Show appropriate page
    if not is_authenticated:
        login.show()
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio(
            "Go to",
            ("Dashboard", "Projects", "Documents", "Analytics", "Settings")
        )

        if page == "Dashboard":
            dashboard.show()
        elif page == "Projects":
            projects.show()
        elif page == "Documents":
            documents.show()
        elif page == "Analytics":
            analytics.show()
        elif page == "Settings":
            settings.show()

if __name__ == "__main__":
    main()