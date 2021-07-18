# payroll/app/api/upload.py

from os.path import splitext
from fastapi import APIRouter, File, UploadFile, status, BackgroundTasks, Response
from app.api.crud import process_file, FILE_EXT
from app.models.pydantic import UploadResponseSchema


router = APIRouter()


@router.post(
    "/v1/upload",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UploadResponseSchema,
    tags=["upload"],
    description="Route to upload payroll CSV file",
)
async def upload_csv(
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
    message = f"{csv_file.filename} upload accepted and is being processed!"

    ext = splitext(csv_file.filename)[-1]

    # file MIME type must be csv
    if csv_file.content_type != "text/csv" and ext not in FILE_EXT:
        response.status_code = status.HTTP_409_CONFLICT
        message = (
            f"{csv_file.filename} is not a valid text/csv file."
            f"This API only supports text/csv files!"
        )

    # if valid csv, check if DB already has existing ID

    # begin processing in the background to add to DB if not prev conditions
    background_tasks.add_task(process_file, csv_file.file)
    return message
