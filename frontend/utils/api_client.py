import os
import requests
import streamlit as st
from typing import Any, Dict, Optional, List

# ==============================
# ⚙️ CONFIGURATION
# ==============================

# Allow override via environment variable
BACKEND_URL = (
    st.secrets.get("BACKEND_UR", None)
    or os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
)

# Token management using Streamlit session state
def get_headers() -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    token = st.session_state.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


# ==============================
# 🔐 AUTHENTICATION
# ==============================

def login(email: str, password: str) -> bool:
    """Authenticate user and store JWT token in session state."""
    try:
        res = requests.post(
            f"{BACKEND_URL}/auth/login",
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if res.status_code == 200:
            data = res.json()
            st.session_state["access_token"] = data["access_token"]
            st.session_state["user"] = data.get("user")
            return True
        else:
            st.error(res.json().get("detail", "Login failed"))
            return False
    except Exception as e:
        st.error(f"Login error: {e}")
        return False


def logout():
    """Clear session tokens."""
    for key in ["access_token", "user"]:
        if key in st.session_state:
            del st.session_state[key]


# ==============================
# 🧩 GENERIC REQUEST HANDLERS
# ==============================

def get(endpoint: str, params: Optional[dict] = None) -> Any:
    try:
        res = requests.get(f"{BACKEND_URL}{endpoint}", headers=get_headers(), params=params)
        res.raise_for_status()
        return res.json()
    except requests.HTTPError as e:
        st.error(f"GET {endpoint} failed: {e.response.text}")
    except Exception as e:
        st.error(f"GET {endpoint} error: {e}")
    return None


def post(endpoint: str, payload: dict) -> Any:
    try:
        res = requests.post(f"{BACKEND_URL}{endpoint}", headers=get_headers(), json=payload)
        res.raise_for_status()
        return res.json()
    except requests.HTTPError as e:
        st.error(f"POST {endpoint} failed: {e.response.text}")
    except Exception as e:
        st.error(f"POST {endpoint} error: {e}")
    return None


def put(endpoint: str, payload: dict) -> Any:
    try:
        res = requests.put(f"{BACKEND_URL}{endpoint}", headers=get_headers(), json=payload)
        res.raise_for_status()
        return res.json()
    except requests.HTTPError as e:
        st.error(f"PUT {endpoint} failed: {e.response.text}")
    except Exception as e:
        st.error(f"PUT {endpoint} error: {e}")
    return None


def delete(endpoint: str) -> Any:
    try:
        res = requests.delete(f"{BACKEND_URL}{endpoint}", headers=get_headers())
        res.raise_for_status()
        return {"detail": "Deleted successfully"}
    except requests.HTTPError as e:
        st.error(f"DELETE {endpoint} failed: {e.response.text}")
    except Exception as e:
        st.error(f"DELETE {endpoint} error: {e}")
    return None


# ==============================
# 🧠 SPECIFIC API HELPERS
# ==============================

# --- USERS ---
def fetch_users() -> List[Dict[str, Any]]:
    return get("/users/")


def create_user(data: Dict[str, Any]) -> Any:
    return post("/users/", data)


# --- PROJECTS ---
def fetch_projects() -> List[Dict[str, Any]]:
    return get("/projects/")


def fetch_project(project_id: int) -> Dict[str, Any]:
    return get(f"/projects/{project_id}")


def create_project(data: Dict[str, Any]) -> Any:
    return post("/projects/", data)


def update_project(project_id: int, data: Dict[str, Any]) -> Any:
    return put(f"/projects/{project_id}", data)


def delete_project(project_id: int) -> Any:
    return delete(f"/projects/{project_id}")


# --- DOCUMENTS ---
def fetch_documents() -> List[Dict[str, Any]]:
    return get("/documents/")


def upload_document(data: Dict[str, Any]) -> Any:
    return post("/documents/", data)


# --- ANALYTICS ---
def fetch_project_kpis(project_id: int) -> Dict[str, Any]:
    return get(f"/analytics/project/{project_id}")


def fetch_team_performance() -> List[Dict[str, Any]]:
    return get("/analytics/team-performance")


# --- TASKS ---
def fetch_tasks(project_id: int) -> List[Dict[str, Any]]:
    return get(f"/tasks/?project_id={project_id}")


def create_task(data: Dict[str, Any]) -> Any:
    return post("/tasks/", data)
