# backend/services/collaboration_service.py
from typing import Dict
from threading import Lock

# In-memory store for DWG session states
dwg_sessions: Dict[int, dict] = {}  # project_id -> session state
session_lock = Lock()

def init_dwg_session(project_id: int):
    with session_lock:
        if project_id not in dwg_sessions:
            dwg_sessions[project_id] = {
                "layers": {},
                "users": [],
                "commands": []
            }
    return dwg_sessions[project_id]

def add_user_to_session(project_id: int, user_id: int):
    with session_lock:
        session = dwg_sessions.get(project_id)
        if session and user_id not in session["users"]:
            session["users"].append(user_id)

def remove_user_from_session(project_id: int, user_id: int):
    with session_lock:
        session = dwg_sessions.get(project_id)
        if session and user_id in session["users"]:
            session["users"].remove(user_id)

def update_dwg_commands(project_id: int, commands: list):
    with session_lock:
        session = dwg_sessions.get(project_id)
        if session:
            session["commands"].extend(commands)

def get_dwg_state(project_id: int):
    with session_lock:
        return dwg_sessions.get(project_id, {})