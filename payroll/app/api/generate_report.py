# payroll/app/api/generate_report.py


from fastapi import APIRouter, Response, status

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
    messages = {"NO_DATA": 404, "INTERNAL_ERROR": 500, "INVALID_DATA": 409}
    (REPORT, ERRORS) = await generate_report_service()
    message = REPORT
    if len(ERRORS) > 0:
        keys = list(ERRORS.keys())
        response.status_code = messages[keys[0]]
        # message in our UploadReponseSchema is a Union of dict and str so we can simply
        # pass ERRORS dict
        message = ERRORS
    return message
