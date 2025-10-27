# backend/websocket/dwg_sync.py
from fastapi import WebSocket
from .manager import manager

async def handle_dwg_message(project_id: int, websocket: WebSocket, message: dict):
    # Broadcast drawing commands to all connected clients except sender
    await manager.broadcast(project_id, message)