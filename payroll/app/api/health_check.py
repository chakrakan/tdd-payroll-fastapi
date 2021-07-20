# payroll/app/api/health_check.py


from fastapi import APIRouter, Depends, status

from app.config import Settings, get_settings

router = APIRouter()


@router.get(
    "/v1/health",
    status_code=status.HTTP_200_OK,
    tags=["Health Check"],
    description="Health check",
)
async def health_check(settings: Settings = Depends(get_settings)):
    return {
        "status": "live",
        "environment": settings.environment,
        "testing": settings.testing,
    }
