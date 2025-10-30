from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Optional
import json
from datetime import datetime

class CADAccessManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.current_editor: Dict[str, Optional[str]] = {}  # project_id -> user_id
        self.editor_requests: Dict[str, Dict] = {}  # project_id -> request_data
        self.user_data: Dict[str, Dict] = {}
    
    async def connect(self, project_id: str, user_id: str, user_name: str, role: str, websocket: WebSocket):
        await websocket.accept()
        
        connection_id = f"{project_id}_{user_id}"
        self.active_connections[connection_id] = websocket
        self.user_data[user_id] = {
            "user_name": user_name,
            "role": role,
            "project_id": project_id
        }
        
        # Send current access status to the connecting user
        current_editor_id = self.current_editor.get(project_id)
        current_editor_name = None
        if current_editor_id:
            current_editor_name = self.user_data.get(current_editor_id, {}).get("user_name")
        
        await websocket.send_json({
            "type": "access_status",
            "data": {
                "current_editor": current_editor_name,
                "has_access": current_editor_id == user_id,
                "can_request": role in ["admin", "engineer"]
            }
        })
        
        # Notify other users in the project about new viewer
        await self.broadcast_user_joined(project_id, user_id)
    
    async def disconnect(self, project_id: str, user_id: str):
        connection_id = f"{project_id}_{user_id}"
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        # If the disconnected user was the editor, release access
        if self.current_editor.get(project_id) == user_id:
            self.current_editor[project_id] = None
            await self.broadcast_access_released(project_id, user_id)
    
    async def request_access(self, project_id: str, user_id: str):
        """User requests to become the editor"""
        user_info = self.user_data.get(user_id, {})
        
        if user_info.get("role") not in ["admin", "engineer"]:
            await self.send_to_user(project_id, user_id, {
                "type": "access_denied",
                "data": {"reason": "Insufficient permissions"}
            })
            return
        
        # Store the request
        self.editor_requests[project_id] = {
            "user_id": user_id,
            "user_name": user_info.get("user_name"),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Notify admins about the request
        await self.broadcast_to_admins(project_id, {
            "type": "access_requested",
            "data": {
                "user_id": user_id,
                "user_name": user_info.get("user_name"),
                "timestamp": datetime.utcnow().isoformat()
            }
        })
        
        await self.send_to_user(project_id, user_id, {
            "type": "access_requested",
            "data": {"message": "Access request sent to administrators"}
        })
    
    async def grant_access(self, project_id: str, target_user_id: str, admin_user_id: str):
        """Admin grants access to a user"""
        admin_info = self.user_data.get(admin_user_id, {})
        if admin_info.get("role") != "admin":
            return
        
        # Release current editor if any
        current_editor = self.current_editor.get(project_id)
        if current_editor:
            await self.send_to_user(project_id, current_editor, {
                "type": "access_revoked",
                "data": {"reason": "Access granted to another user"}
            })
        
        # Grant access to new user
        self.current_editor[project_id] = target_user_id
        self.editor_requests.pop(project_id, None)
        
        # Notify the new editor
        await self.send_to_user(project_id, target_user_id, {
            "type": "access_granted",
            "data": {"granted_by": admin_info.get("user_name")}
        })
        
        # Notify all users
        await self.broadcast_access_granted(project_id, target_user_id)
    
    async def release_access(self, project_id: str, user_id: str):
        """Editor voluntarily releases access"""
        if self.current_editor.get(project_id) == user_id:
            self.current_editor[project_id] = None
            await self.broadcast_access_released(project_id, user_id)
    
    async def broadcast_drawing_update(self, project_id: str, drawing_data: dict, user_id: str):
        """Broadcast drawing updates from the current editor"""
        if self.current_editor.get(project_id) == user_id:
            message = {
                "type": "drawing_update",
                "data": drawing_data
            }
            await self.broadcast_to_project(project_id, message, exclude_user=user_id)
    
    async def send_to_user(self, project_id: str, user_id: str, message: dict):
        connection_id = f"{project_id}_{user_id}"
        if connection_id in self.active_connections:
            await self.active_connections[connection_id].send_json(message)
    
    async def broadcast_to_project(self, project_id: str, message: dict, exclude_user: str = None):
        for connection_id, websocket in self.active_connections.items():
            if project_id in connection_id:
                user_id = connection_id.split("_")[1]
                if user_id != exclude_user:
                    await websocket.send_json(message)
    
    async def broadcast_to_admins(self, project_id: str, message: dict):
        for user_id, user_info in self.user_data.items():
            if user_info.get("role") == "admin" and user_info.get("project_id") == project_id:
                await self.send_to_user(project_id, user_id, message)
    
    async def broadcast_user_joined(self, project_id: str, user_id: str):
        user_info = self.user_data.get(user_id, {})
        await self.broadcast_to_project(project_id, {
            "type": "user_joined",
            "data": {
                "user_id": user_id,
                "user_name": user_info.get("user_name"),
                "role": user_info.get("role")
            }
        }, exclude_user=user_id)
    
    async def broadcast_access_granted(self, project_id: str, user_id: str):
        user_info = self.user_data.get(user_id, {})
        await self.broadcast_to_project(project_id, {
            "type": "access_granted",
            "data": {
                "user_id": user_id,
                "user_name": user_info.get("user_name")
            }
        })
    
    async def broadcast_access_released(self, project_id: str, user_id: str):
        user_info = self.user_data.get(user_id, {})
        await self.broadcast_to_project(project_id, {
            "type": "access_released",
            "data": {
                "user_id": user_id,
                "user_name": user_info.get("user_name")
            }
        })

cad_access_manager = CADAccessManager()