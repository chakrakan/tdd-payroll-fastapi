# project/app/api/generate_report.py


from fastapi import APIRouter, status, BackgroundTasks

from app.api.crud import generate_report_service


router = APIRouter()


@router.get(
    "/v1/report",
    status_code=status.HTTP_200_OK,
    description="Route to retrieve JSON data for all TimeReport data uploaded",
)
async def generate_report(background_task: BackgroundTasks):
    """Endpoint to retrieve and generate a report for all employees and for all
    time periods uploaded thus far to the system.

    Returns:
        [type]: [description]
    """
    background_task.add_task(generate_report_service)
