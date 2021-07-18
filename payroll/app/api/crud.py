# payroll/app/api/crud.py

import re
from os.path import splitext

from fastapi.datastructures import UploadFile

from app.models.tortoise import TimeReport

# extendable file types and const naming convention

FILE_EXT = {".csv"}
NAMING_CONVENTION = re.compile("time-report-\\d+")


async def process_file(csv_file: UploadFile):
    """
    Main file processing handler

    Args:
        csv_file (SpooledTemporaryFile): [description]

    Returns:
        int: [description]
    """
    print(f"Processing {csv_file.filename} complete!")


async def generate_report_service():
    """
    Report generator handler

    Returns:
        dict: [description]
    """
    # logic to generate report
    print("Report Generated!")


async def validate_file(file_with_ext: str, content_type: str) -> tuple:
    """
    File validator

    Args:
        file_with_ext (str): [description]
        content_type (str): [description]

    Returns:
        int: [description]
    """

    ERRORS = {}

    (name, ext) = (splitext(file_with_ext)[0], splitext(file_with_ext)[-1])

    is_valid_type = content_type == "text/csv" and ext in FILE_EXT
    if not is_valid_type:
        ERRORS["INVALID_TYPE"] = (
            f"Error: {file_with_ext} is not a valid text/csv file. "
            f"This API only supports text/csv files."
        )

    is_valid_name = bool(NAMING_CONVENTION.search(name))
    if not is_valid_name:
        ERRORS["INVALID_NAME"] = (
            f"Error: {file_with_ext} does not have the right naming convention. "
            f"This API only supports CSV files with strict `time-report-[0-9]+` "
            f"based naming where the digits represent the report ID."
        )
    file_id = int(name.split("-")[2]) if is_valid_type and is_valid_name else 0

    # check if file_id alreayd in database
    file_in_db = file_id != 0 and await TimeReport.filter(id=file_id).exists()
    if file_in_db:
        ERRORS["DUPLICATE_REPORT"] = f"Error: {file_with_ext} already exists in DB."

    print(
        (
            f"Validate file: {name}, {ext}, {is_valid_name}, {is_valid_type}, "
            f"{file_id}, {file_in_db}"
        )
    )

    return (file_id, ERRORS)
