from fastapi import APIRouter

from app.config import settings
from app.db.factory import get_active_db_mode
from app.models.domain import HealthOut

router = APIRouter(tags=["health"])


@router.get("/api/health", response_model=HealthOut)
def health() -> HealthOut:
    return HealthOut(ai_mode=settings.ai_mode, db_mode=get_active_db_mode())
