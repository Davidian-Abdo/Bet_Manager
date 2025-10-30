from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from backend.api.router import api_router
from backend.websocket.manager import manager
from backend.websocket.dwg_sync import handle_dwg_message
from backend.websocket.notifications import send_notification
from backend.core.logging_config import logger
import logging
logging.basicConfig(level=logging.DEBUG)
app = FastAPI(
    title="BET Manager API",
    description="Backend API for Bureaux d'Études Marocains en Génie Civil",
    version="1.0",
)

# CORS middleware to allow frontend connections
origins = [
    "http://localhost:8501",  # Streamlit frontend
    "http://localhost",
    # Add production domains
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(api_router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "BET Manager API is running"}

# WebSocket for DWG real-time collaboration
@app.websocket("/ws/projects/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: int):
    await manager.connect(project_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await handle_dwg_message(project_id, websocket, data)
    except Exception:
        pass
    finally:
        manager.disconnect(project_id, websocket)

# Optional: WebSocket for notifications
@app.websocket("/ws/notifications/{project_id}")
async def notifications_endpoint(websocket: WebSocket, project_id: int):
    await manager.connect(project_id, websocket)
    try:
        while True:
            # Keep connection alive for push notifications
            await websocket.receive_text()
    except Exception:
        pass
    finally:
        manager.disconnect(project_id, websocket)