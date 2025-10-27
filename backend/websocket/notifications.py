# backend/websocket/notifications.py
from fastapi import WebSocket
from .manager import manager

async def send_notification(project_id: int, content: str, type_: str = "info"):
    message = {"type": "notification", "content": content, "level": type_}
    await manager.broadcast(project_id, message)