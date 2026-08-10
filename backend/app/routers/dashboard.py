from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db_dependency, get_current_user_dependency
from app.models.user import User
from app.services.dashboard_service import get_dashboard_metrics

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/status")
def read_dashboard_status():
    return {"status": "ok", "message": "AI Ticket Resolution Platform is running"}


@router.get("/metrics")
def read_dashboard_metrics(
    db: Session = Depends(get_db_dependency),
    current_user: User = Depends(get_current_user_dependency),
):
    return get_dashboard_metrics(db, current_user)
