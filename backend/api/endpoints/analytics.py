# backend/api/endpoints/analytics.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.analytics_service import get_project_kpis, get_team_performance
from api.dependencies import get_db_session

router = APIRouter()

@router.get("/projects")
def api_project_kpis(db: Session = Depends(get_db_session)):
    return get_project_kpis(db)

@router.get("/team")
def api_team_performance(db: Session = Depends(get_db_session)):
    return get_team_performance(db)