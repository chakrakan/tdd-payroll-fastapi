# payroll/app/api/generate_report.py


from fastapi import APIRouter, status, Response
from app.api.services import generate_report_service


router = APIRouter()


@router.get(
    "/v1/report",
    status_code=status.HTTP_200_OK,
    tags=["Generate Report"],
    description="Route to retrieve JSON data for all TimeReport data uploaded",
)
async def generate_report(response: Response):
    """
    Endpoint to retrieve and generate a report for all employees and for all
    time periods uploaded thus far to the system.
    If attempted to generate prior to uploading any CSVs return 404 code.
    Otherwise, if attempting to upload duplicate data with different file naming
    then return 409 conflict if a particular worker goes over 12hrs/day of work hours.

    Returns:
        [type]: [description]
    """
    (REPORT, ERRORS) = await generate_report_service()
    message = REPORT
    if len(ERRORS) > 0:
        response.status_code = (
            status.HTTP_404_NOT_FOUND
            if "NO_DATA" in ERRORS.keys()
            else status.HTTP_409_CONFLICT
        )
        # message in our UploadReponseSchema is a Union of dict and str so we can simply
        # pass ERRORS dict
        message = ERRORS
    return message
