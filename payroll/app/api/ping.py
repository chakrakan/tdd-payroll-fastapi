# payroll/app/api/ping.py


from fastapi import APIRouter, Depends
from app.config import get_settings, Settings


router = APIRouter()


@router.get("/v1/ping", status_code=200, description="Health check")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
