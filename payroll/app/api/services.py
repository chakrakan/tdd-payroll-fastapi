# payroll/app/api/crud.py

from decimal import Decimal
import re
from os.path import splitext
from datetime import datetime
from fastapi.datastructures import UploadFile

from app.models.tortoise import Employee, JobGroup, TimeReport

# extendable file types and const naming convention

FILE_EXT = {".csv"}
NAMING_CONVENTION = re.compile("time-report-\\d+$")


async def process_file(uploaded_file: UploadFile, file_id: int):
    """
    Main file processing handler

    Args:
        csv_file (SpooledTemporaryFile): [description]

    Returns:
        int: [description]
    """

    try:
        # file decode
        csv_byte_literal = await uploaded_file.read()
        data = csv_byte_literal.decode("utf-8").splitlines()

        # consts
        list_of_report_objs = []

        if len(data) > 1:

            # create data in DB + map them up

            for line in data[1:]:
                data_row = line.split(",")
                (day, month, year) = data_row[0].split("/")
                formatted_date = datetime(int(year), int(month), int(day))
                formatted_hrs = Decimal(data_row[1])

                # get or create a job_group or employee dynamically
                db_job_id = await get_job_group(data_row[3])
                db_employee_id = await get_employee(int(data_row[2]), db_job_id)

                list_of_report_objs.append(
                    TimeReport(
                        report_id=file_id,
                        date=formatted_date,
                        hours_worked=formatted_hrs,
                        employee_id=db_employee_id,
                        job_group_id=db_job_id,
                    )
                )

            # upload/commit and bulk create all time_reports
            await TimeReport.bulk_create(list_of_report_objs)

            # process payroll in DB

            await uploaded_file.close()
            print(f"Processing {uploaded_file.filename} complete!")
        else:
            print(f"{uploaded_file.filename} has 0 data rows. Abort processing")

    except Exception as e:
        print(f"Error in proces_file: {e}")


async def generate_report_service() -> tuple:
    """
    Report generator handler, can be extended in the future
    if the GET request supports time_periods to limit querying entire DB

    Returns:
        dict: [description]
    """
    ERRORS = {}
    REPORT = {"payrollReport": {"employeeReports": []}}

    try:
        # check if there are any values in our table
        reports_from_db = await TimeReport.all().order_by("date")
        if len(reports_from_db) > 0:
            print(reports_from_db)
            print("Report Generated!")
        else:
            ERRORS["NO_DATA"] = (
                "Error: There is no data in the database. "
                "Please make sure you upload a time report first via "
                "the APIs `/v1/upload` endpoint!"
            )
    except Exception as e:
        print(f"Error generating generate_report_service: {e}")

    return (REPORT, ERRORS)


async def get_job_group(group_name: str) -> str:
    """To demonstrate job_group modularity

    Args:
        group_name (str): [job group char]
    """
    try:
        JOB_GROUPS = {"A": 20.00, "B": 30.00}
        created_group = (
            group_name in JOB_GROUPS.keys()
            and await JobGroup.get_or_create(
                group=group_name, hourly_rate=Decimal(JOB_GROUPS[group_name])
            )
        )
        return created_group[0].pk
    except Exception as e:
        print(f"Error creating get_job_group: {e}")


async def get_employee(employee_id: int, job_group: str) -> int:
    """To demonstrate employee modularity

    Args:
        employee_id (int): [employee id]
    """
    try:
        created_employee = await Employee.get_or_create(
            id=employee_id, job_group_id=job_group
        )
        return created_employee[0].id
    except Exception as e:
        print(f"Error in get_employee: {e}")


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

    try:
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
        file_in_db = (
            file_id != 0 and await TimeReport.filter(report_id=file_id).exists()
        )
        if file_in_db:
            ERRORS["DUPLICATE_REPORT"] = f"Error: {file_with_ext} already exists in DB."

        print(
            (
                f"Validate file: {content_type}, {name}, {ext}, {is_valid_name}, "
                f"{is_valid_type}, {file_id}, {file_in_db}"
            )
        )
    except Exception as e:
        print(f"Error in validate_file: {e}")

    return (file_id, ERRORS)
