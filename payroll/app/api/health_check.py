# payroll/app/api/health_check.py


from fastapi import APIRouter, Depends, status
from app.config import get_settings, Settings


router = APIRouter()


@router.get("/v1/health", status_code=status.HTTP_200_OK, description="Health check")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "status": "live",
        "environment": settings.environment,
        "testing": settings.testing,
    }
