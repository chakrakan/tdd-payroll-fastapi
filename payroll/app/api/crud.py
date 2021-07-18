# payroll/app/api/crud.py

import re
from os.path import splitext

from fastapi.datastructures import UploadFile

# from app.models.tortoise import TimeReport

# extendable file types and const naming convention

FILE_EXT = {".csv"}
NAMING_CONVENTION = re.compile("time-report-\\d+")

ERRORS = {
    "DUPLICATE_REPORT": "Error: Duplicate report",
}


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


async def validate_file(file_with_ext: str, content_type: str) -> int:
    """
    File validator

    Args:
        file_with_ext (str): [description]
        content_type (str): [description]

    Returns:
        int: [description]
    """
    (name, ext) = (splitext(file_with_ext)[0], splitext(file_with_ext)[-1])
    is_valid_type = content_type == "text/csv" and ext in FILE_EXT
    is_valid_name = bool(NAMING_CONVENTION.search(name))
    file_id = int(name.split("-")[2]) if is_valid_type and is_valid_name else 0

    print(f"Validate file: {name}, {ext}, {is_valid_name}, {is_valid_type}, {file_id}")

    return file_id
