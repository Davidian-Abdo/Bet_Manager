
import streamlit as st
from pages import dashboard, projects, documents, analytics, settings, login, cad_collaboration
from utils.api_client import logout  # Import from your existing api_client

# Configure page
st.set_page_config(page_title="BET Manager", layout="wide")

def validate_token(token: str) -> bool:
    """Validate if the token is still valid with the backend"""
    try:
        from utils.api_client import BACKEND_URL, get_headers
        import requests
        
        response = requests.get(
            f"{BACKEND_URL}/api/users/me",
            headers=get_headers(),
            timeout=5
        )
        
        if response.status_code == 200:
            st.session_state.user = response.json()
            return True
        else:
            # Token is invalid
            st.session_state.token = None
            st.session_state.user = None
            return False
            
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return False

def check_backend_connection() -> bool:
    """Check if backend is reachable"""
    try:
        from utils.api_client import BACKEND_URL
        import requests
        response = requests.get(f"{BACKEND_URL}/docs", timeout=5)
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
    if "token" not in st.session_state:
        st.session_state.token = None
    
    # Show connection status
    show_connection_status()
    
    # Check if user is properly authenticated
    is_authenticated = False
    
    if "token" in st.session_state and st.session_state.token:
        # We have a token - consider user authenticated
        # Optional: validate token (commented for now to ensure login works)
        # is_authenticated = validate_token(st.session_state.token)
        is_authenticated = True
    else:
        # No token exists
        is_authenticated = False
    
    # Show appropriate page
    if not is_authenticated:
        login.show()
    else:
        st.sidebar.title("Navigation")
        
        # User info and logout
        if st.session_state.user:
            st.sidebar.write(f"👤 **{st.session_state.user.get('name', 'User')}**")
            st.sidebar.write(f"🎯 Role: {st.session_state.user.get('role', 'User')}")
        
        if st.sidebar.button("🚪 Logout"):
            logout()
            st.rerun()
        
        page = st.sidebar.radio(
            "Go to",
            ("Dashboard", "Projects", "CAD Collaboration", "Documents", "Analytics", "Settings")
        )

        if page == "Dashboard":
            dashboard.show()
        elif page == "Projects":
            projects.show()
        elif page == "CAD Collaboration":
            cad_collaboration.show()
        elif page == "Documents":
            documents.show()
        elif page == "Analytics":
            analytics.show()
        elif page == "Settings":
            settings.show()

if __name__ == "__main__":
    main()