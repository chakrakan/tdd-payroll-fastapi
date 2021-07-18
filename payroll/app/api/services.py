# payroll/app/api/crud.py

from decimal import Decimal
import re
from os.path import splitext
from datetime import datetime

from fastapi.datastructures import UploadFile

from app.models.tortoise import TimeReport

# extendable file types and const naming convention

FILE_EXT = {".csv"}
NAMING_CONVENTION = re.compile("time-report-\\d+$")


async def process_file(uploaded_file: UploadFile):
    """
    Main file processing handler

    Args:
        csv_file (SpooledTemporaryFile): [description]

    Returns:
        int: [description]
    """
    csv_byte_literal = await uploaded_file.read()
    data = csv_byte_literal.decode("utf-8").splitlines()
    list_of_report_objs = []
    if len(data) > 1:
        for line in data[1:]:
            data_row = line.split(",")
            date_obj = datetime.strptime(data_row[0], "%d/%m/%y")
            list_of_report_objs.append(
                TimeReport(
                    date=date_obj,
                    hours_worked=Decimal(data_row[1]),
                    employee_id=int(data_row[2], job_group=data_row[3]),
                )
            )

        await TimeReport.bulk_create(list_of_report_objs)
    else:
        print(f"{uploaded_file.filename} has 0 data rows. Abort processing")

    await uploaded_file.close()
    print(f"Processing {uploaded_file.filename} complete!")


async def generate_report_service():
    """
    Report generator handler, can be extended in the future
    if the GET request supports time_periods to limit querying entire DB

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
            f"Validate file: {content_type}, {name}, {ext}, {is_valid_name}, "
            f"{is_valid_type}, {file_id}, {file_in_db}"
        )
    )

    return (file_id, ERRORS)
