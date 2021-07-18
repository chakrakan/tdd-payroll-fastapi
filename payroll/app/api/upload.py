# payroll/app/api/upload.py

from fastapi import APIRouter, File, UploadFile, status, BackgroundTasks, Response
from app.api.crud import process_file, validate_file
from app.models.pydantic import UploadResponseSchema


router = APIRouter()


@router.post(
    "/v1/upload",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UploadResponseSchema,
    tags=["Upload Report"],
    description="Route to upload payroll CSV file",
)
async def upload_report(
    background_tasks: BackgroundTasks,
    response: Response,
    csv_file: UploadFile = File(...),
):
    """
    Endpoint to upload file. UploadFile type creates a background task to process
    the file as spooled memory to read and process efficiently.

    Args:
        background_tasks (BackgroundTasks): [description]
        response (Response): [description]
        csv_file (UploadFile, optional): [description]. Defaults to File(...).

    Returns:
        [type]: [description]
    """
    message = f"Accepted: {csv_file.filename} upload accepted and is being processed!"
    (file_id, ERRORS) = await validate_file(csv_file.filename, csv_file.content_type)

    if file_id == 0 or len(ERRORS) > 0:
        response.status_code = status.HTTP_409_CONFLICT
        # all errors begin with Error: and end in new line
        message = ERRORS
    else:
        background_tasks.add_task(process_file, csv_file)

    return UploadResponseSchema(file_id=file_id, message=message)
